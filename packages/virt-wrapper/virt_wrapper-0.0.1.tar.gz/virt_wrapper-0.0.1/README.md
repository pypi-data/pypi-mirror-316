# Description

Python wrapper for managing virtual infrastructure based on Hyper-V or KVM (libvirt)

# Example usage
```python
from virt_wrapper import *

kvm = VirtualMachine(driver=KernelVirtualMachineDriver(host="linux-server.lan", uuid="c7c2f567-064f-464e-9843-1ed55c04f35e"))

hvm = VirtualMachine(driver=HyperVirtualMachineDriver(host="windows-server.lan", uuid="37a6cee8-f6ce-48c4-a635-7145e8770cca"))

print(f"Virtual machine on Linux has name: {kvm.name()}\nVirtual machine on Windows has name: {hvm.name()}")

```

# Requirements
## KVM

- SSH-key must be imported on target server
- User must have full access to libvirt
```sh
usermod <your_user> -aG libvirt
systemctl restart libvirtd
```

## Hyper-V
- WinRM must be enabled with certification based authentication. Keys must be placed in `~/.winrm` (cert.pem and cert.key). Generating keys and setting up cert-based authentication can be done by following this [instruction](https://docs.ansible.com/ansible/latest/os_guide/windows_winrm_certificate.html#certificate-generation)
- User must have full access to Hyper-V
