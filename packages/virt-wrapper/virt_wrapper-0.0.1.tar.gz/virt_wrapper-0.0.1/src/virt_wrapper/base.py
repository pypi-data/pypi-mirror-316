from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .drivers.hyperv import HyperVirtualHostDriver, HyperVirtualMachineDriver
from .drivers.kvm import KernelVirtualHostDriver, KernelVirtualMachineDriver


@dataclass
class MemoryStat:
    startup: int
    maximum: int
    demand: int
    assigned: int


@dataclass
class Snapshot:
    vm: "VirtualMachine"
    name: str
    identifier: str
    parent_name: str
    creation_time: int
    is_applied: bool
    cpu: int
    ram: int

    def apply(self) -> None:
        self.vm.driver.snapshot_apply(identifier=self.identifier)

    def destroy(self) -> None:
        self.vm.driver.snapshot_destroy(identifier=self.identifier)


@dataclass
class VirtualDisk:
    name: str
    path: Path
    storage: str
    size: int
    used: int


@dataclass
class VirtualNetwork:
    mac: str
    switch: str
    addresses: list[str]


class VirtualMachine:
    def __init__(self, driver: KernelVirtualMachineDriver | HyperVirtualMachineDriver) -> None:
        self.driver = driver

    def uuid(self) -> str:
        return self.driver.uuid

    def name(self) -> str:
        return self.driver.get_name()

    def description(self) -> str | None:
        return self.driver.get_description()

    def guest_os(self) -> str | None:
        return self.driver.get_guest_os()

    def state(self) -> str:
        return self.driver.get_state()

    def memory_stat(self) -> MemoryStat:
        data = self.driver.get_memory_stat()
        return MemoryStat(
            startup=data["startup"], maximum=data["maximum"], demand=data["demand"], assigned=data["assigned"]
        )

    def snapshots(self) -> list[Snapshot]:
        result = []
        for s in self.driver.get_snapshots():
            result.append(
                Snapshot(
                    vm=self,
                    name=s["name"],
                    identifier=s["identifier"],
                    parent_name=s["parent_name"],
                    creation_time=datetime.fromtimestamp(s["creation_time"]),
                    is_applied=s["is_applied"],
                    cpu=s["cpu"],
                    ram=s["ram"],
                )
            )
        return result

    def disks(self) -> list[VirtualDisk]:
        result = []
        for d in self.driver.get_disks():
            result.append(
                VirtualDisk(name=d["name"], path=Path(d["path"]), storage=d["storage"], size=d["size"], used=d["used"])
            )
        return result

    def networks(self) -> list[VirtualNetwork]:
        networks = self.driver.get_networks()
        return [VirtualNetwork(mac=net["mac"], switch=net["switch"], addresses=net["addresses"]) for net in networks]

    def run(self) -> None:
        self.driver.run()

    def shutdown(self) -> None:
        self.driver.shutdown()

    def poweroff(self) -> None:
        self.driver.poweroff()

    def save(self) -> None:
        self.driver.save()

    def snap_create(self, name: str) -> None:
        self.driver.snapshot_create(name=name)


class Host:
    def __init__(self, driver: KernelVirtualHostDriver | HyperVirtualHostDriver):
        self.driver = driver

    def virtual_machines(self) -> list[VirtualMachine]:
        return [VirtualMachine(driver=driver) for driver in self.driver.virtual_machine_drivers()]
