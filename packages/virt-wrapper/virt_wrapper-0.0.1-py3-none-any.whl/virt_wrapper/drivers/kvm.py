import getpass
import os
from xml.etree import ElementTree as ET

import libvirt


# Avoid printing error messages
def libvirt_callback(userdata, err):
    pass


libvirt.registerErrorHandler(f=libvirt_callback, ctx=None)


SSH_USER = os.environ.get("SSH_USER", getpass.getuser())
SSH_PRIVATE_KEY = os.environ.get("SSH_PRIVATE_KEY", os.path.join(os.path.expanduser("~"), ".ssh", "id_rsa"))


class KernelVirtualDriver:
    def __init__(self, host: str) -> None:
        self.host = host
        self.conn = libvirt.open(
            f"qemu+libssh2://{SSH_USER}@{host}/system?sshauth=privkey&keyfile={SSH_PRIVATE_KEY}&known_hosts_verify=auto"
        )


class KernelVirtualMachineDriver(KernelVirtualDriver):
    def __init__(self, host: str, uuid: str | None = None) -> None:
        KernelVirtualDriver.__init__(self, host=host)
        self.domain = self.conn.lookupByUUIDString(uuid)
        self.uuid = self.domain.UUIDString()

    def __enter__(self) -> "KernelVirtualMachineDriver":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.close()

    def get_name(self) -> str:
        try:
            return self.domain.metadata(libvirt.VIR_DOMAIN_METADATA_TITLE, None)
        except libvirt.libvirtError:
            return self.domain.name()

    def get_state(self) -> str:
        states = {
            libvirt.VIR_DOMAIN_RUNNING: "Running",
            libvirt.VIR_DOMAIN_BLOCKED: "Blocked",
            libvirt.VIR_DOMAIN_PAUSED: "Paused",
            libvirt.VIR_DOMAIN_SHUTDOWN: "Shutdown",
            libvirt.VIR_DOMAIN_SHUTOFF: "Off",
            libvirt.VIR_DOMAIN_CRASHED: "Crashed",
            libvirt.VIR_DOMAIN_NOSTATE: "No state",
        }
        ret_state, _ = self.domain.state()
        return states[ret_state]

    def get_description(self) -> str | None:
        try:
            return self.domain.metadata(libvirt.VIR_DOMAIN_METADATA_DESCRIPTION, None)
        except libvirt.libvirtError:
            return None

    def get_guest_os(self) -> str | None:
        try:
            return self.domain.guestInfo().get("os.pretty-name")
        except libvirt.libvirtError:
            return None

    def get_memory_stat(self) -> dict[str, int]:
        if self.domain.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
            actual = 0
            demand = 0
        else:
            actual = self.domain.memoryStats().get("actual")
            demand = actual - self.domain.memoryStats().get("unused", actual)

        maximum = self.domain.maxMemory()
        startup = self.domain.info()[2]
        return {
            "startup": startup,
            "maximum": maximum,
            "demand": demand if demand >= 0 else 0,
            "assigned": actual,
        }

    def get_snapshots(self) -> list:
        ret = []
        for snap in self.domain.listAllSnapshots():
            tree_snap = ET.fromstring(snap.getXMLDesc())
            ram = int(tree_snap.find("domain/currentMemory").text)
            cpu = int(tree_snap.find("domain/vcpu").text)
            try:
                parent = snap.getParent().getName()
            except libvirt.libvirtError:
                parent = None
            ret.append(
                {
                    "name": snap.getName(),
                    "identifier": snap.getName(),
                    "parent_name": parent,
                    "creation_time": int(tree_snap.find("creationTime").text),
                    "is_applied": snap.getName() == self.domain.snapshotCurrent().getName(),
                    "cpu": cpu,
                    "ram": ram,
                }
            )

        return ret

    def get_disks(self) -> list[dict]:
        ret = []
        for src in ET.fromstring(self.domain.XMLDesc()).findall("devices/disk/source"):
            try:
                if src.get("pool"):
                    storage_pool = self.conn.storagePoolLookupByName(src.get("pool"))
                    volume = storage_pool.storageVolLookupByName(src.get("volume"))
                else:
                    volume = self.conn.storageVolLookupByPath(src.get("file"))
                    storage_pool = volume.storagePoolLookupByVolume()
                _, size, used = volume.info()
                ret.append(
                    {
                        "name": volume.name(),
                        "path": volume.path(),
                        "storage": storage_pool.name(),
                        "size": size,
                        "used": used,
                    }
                )
            except libvirt.libvirtError:
                continue
        return ret

    def get_networks(self) -> list:
        ret = []
        for interface in ET.fromstring(self.domain.XMLDesc()).findall("devices/interface"):
            mac = interface.find("mac").get("address")
            switch_name = interface.find("source").get("bridge")

            if self.domain.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
                try:
                    nets = self.domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT)
                except libvirt.libvirtError:
                    nets = self.domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_ARP)
                addresses = []
                for net in nets:
                    if nets[net].get("hwaddr") == mac:
                        addrs = nets[net].get("addrs")
                        address = [addr.get("addr") for addr in addrs]
                        addresses.extend(address)
                        break
            else:
                addresses = []

            ret.append({"mac": mac.upper(), "switch": switch_name, "addresses": addresses})
        return ret

    def cpus(self) -> int:
        return self.domain.info()[3]

    def get_displays(self) -> list[dict]:
        ret = []
        for display in ET.fromstring(self.domain.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)).findall("devices/graphics"):
            ret.append({"Type": display.get("type"), "Port": display.get("port"), "Password": display.get("passwd")})
        return ret

    def run(self) -> None:
        if self.domain.state()[0] != libvirt.VIR_DOMAIN_RUNNING:
            self.domain.create()

    def shutdown(self) -> None:
        self.domain.shutdown()

    def poweroff(self) -> None:
        self.domain.destroy()

    def save(self) -> None:
        self.domain.managedSave()

    def suspend(self) -> None:
        self.domain.suspend()

    def resume(self) -> None:
        self.domain.resume()

    def snapshot_create(self, name: str) -> None:
        snapshot_xml_template = f"""<domainsnapshot><name>{name}</name></domainsnapshot>"""
        self.domain.snapshotCreateXML(snapshot_xml_template, libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_ATOMIC)

    def snapshot_apply(self, identifier: str) -> None:
        snap = self.domain.snapshotLookupByName(identifier)
        self.domain.revertToSnapshot(snap)

    def snapshot_destroy(self, identifier: str) -> None:
        snap = self.domain.snapshotLookupByName(identifier)
        snap.delete()


class KernelVirtualHostDriver(KernelVirtualDriver):
    def virtual_machine_drivers(self) -> list[KernelVirtualMachineDriver]:
        return [
            KernelVirtualMachineDriver(host=self.host, uuid=domain.UUIDString())
            for domain in self.conn.listAllDomains()
        ]
