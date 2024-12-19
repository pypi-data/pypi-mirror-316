import pytest

from src.virt_wrapper import Host


@pytest.mark.parametrize("host", ["kvm_host", "hv_host"])
def test(host: Host, request):
    host = request.getfixturevalue(host)
    for vm in host.virtual_machines():
        if vm.name().startswith("pytest-"):
            break
    else:
        raise Exception("Virtual machine for tests wasn't found")

    # vm.run()
    # assert vm.state() == "Running"
    # vm.poweroff()
    # assert vm.state() == "Off"

    print(vm.snapshots())
    print(vm.disks())
    print(vm.networks())
