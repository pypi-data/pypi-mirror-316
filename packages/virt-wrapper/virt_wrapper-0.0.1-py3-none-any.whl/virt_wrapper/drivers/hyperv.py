import json
import os

import winrm
from jinja2 import Template

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_PATH, "hyperv_utils")

WINRM_CERT_PEM = os.environ.get("WINRM_CERT_PEM", os.path.join(os.path.expanduser("~"), ".winrm", "cert.pem"))
WINRM_CERT_KEY = os.environ.get("WINRM_CERT_KEY", os.path.join(os.path.expanduser("~"), ".winrm", "cert.key"))


class HyperVirtualDriver:
    def __init__(self, host: str) -> None:
        self.host = host
        # https://docs.ansible.com/ansible/latest/os_guide/windows_winrm_certificate.html#certificate-generation
        self.winrm_session = winrm.Session(
            target=f"https://{host}:5986/wsman",
            auth=("", ""),
            transport="certificate",
            server_cert_validation="ignore",
            cert_pem=WINRM_CERT_PEM,
            cert_key_pem=WINRM_CERT_KEY,
        )

    def exec_ps(self, filename: str = "common.ps1", **kwargs) -> str:
        with open(os.path.join(TEMPLATES_DIR, filename), encoding="utf-8") as file:
            template = Template(file.read())

        script = template.render(**kwargs)
        result = self.winrm_session.run_ps(script)
        if result.status_code:
            raise Exception(result.std_err.decode())
        return result.std_out.decode().strip()


class HyperVirtualMachineDriver(HyperVirtualDriver):
    def __init__(self, host: str, uuid: str) -> None:
        self.uuid = uuid
        HyperVirtualDriver.__init__(self, host=host)

    def get_name(self) -> str:
        return self.exec_ps(command=f"Get-VM -Id {self.uuid} | Select -Expand Name")

    def get_state(self) -> str:
        return self.exec_ps(command=f"Get-VM -Id {self.uuid} | Select -Expand State")

    def get_description(self) -> str:
        return self.exec_ps(command=f"Get-VM -Id {self.uuid} | Select -Expand Notes")

    def get_guest_os(self) -> str | None:
        return self.exec_ps(filename="get-vmguestos.ps1", guid=self.uuid) or None

    def get_memory_stat(self) -> dict[str, int]:
        return json.loads(self.exec_ps(filename="get-vmmem.ps1", guid=self.uuid))

    def get_snapshots(self):
        return json.loads(self.exec_ps(filename="get-vmsnapshots.ps1", guid=self.uuid))

    def get_disks(self) -> list:
        return json.loads(self.exec_ps(filename="get-vmdisks.ps1", guid=self.uuid))

    def get_networks(self) -> list:
        return json.loads(self.exec_ps(filename="get-vmnetworks.ps1", guid=self.uuid))

    def run(self) -> None:
        self.exec_ps(command=f"Get-VM -Id {self.uuid} | Start-VM")

    def shutdown(self) -> None:
        self.exec_ps(command=f"Get-VM -Id {self.uuid} | Stop-VM -Force")

    def poweroff(self) -> None:
        self.exec_ps(command=f"Get-VM -Id {self.uuid} | Stop-VM -TurnOff")

    def save(self) -> None:
        self.exec_ps(command=f"Get-VM -Id {self.uuid} | Stop-VM -Save")

    def snapshot_create(self, name: str) -> None:
        self.exec_ps(command=f"Get-VM -Id {self.uuid} | Checkpoint-VM -SnapshotName '{name}'")

    def snapshot_apply(self, identifier: str) -> None:
        self.exec_ps(
            command=f"Get-VM -Id {self.uuid} | Get-VMSnapshot | Where {{$_.Id.Guid -eq '{identifier}'}} | Restore-VMSnapshot -Confirm:$false"
        )

    def snapshot_destroy(self, identifier: str) -> None:
        self.exec_ps(
            command=f"Get-VM -Id {self.uuid} | Get-VMSnapshot | Where {{$_.Id.Guid -eq '{identifier}'}} | Remove-VMSnapshot"
        )


class HyperVirtualHostDriver(HyperVirtualDriver):
    def virtual_machine_drivers(self) -> list[HyperVirtualMachineDriver]:
        return [
            HyperVirtualMachineDriver(host=self.host, uuid=uuid)
            for uuid in json.loads(self.exec_ps(command="ConvertTo-Json (Get-VM).Id.Guid"))
        ]
