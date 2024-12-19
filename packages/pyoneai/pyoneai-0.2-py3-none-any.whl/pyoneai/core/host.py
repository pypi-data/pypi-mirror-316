__all__ = ["Host", "HostPool", "HostState"]

import enum
from typing import Any

from ..session import Session
from . import virtual_machine
from .bases import Entity, LatestMetricValue, Pool
from .pci_device import PCIDevice, PCIDevicePool

# NOTE: The names, values, and comments are copied from:
# https://github.com/OpenNebula/one-ee/blob/master/share/doc/xsd/host.xsd


@enum.unique
class HostState(enum.IntEnum):
    # For more information see:
    # https://docs.opennebula.io/6.8/integration_and_development/references/host_states.html
    # Initial state for enabled hosts.
    INIT = 0
    # Monitoring the host (from monitored).
    MONITORING_MONITORED = 1
    # The host has been successfully monitored.
    MONITORED = 2
    # An error ocurrer while monitoring the host.
    ERROR = 3
    # The host is disabled.
    DISABLED = 4
    # Monitoring the host (from error).
    MONITORING_ERROR = 5
    # Monitoring the host (from init).
    MONITORING_INIT = 6
    # Monitoring the host (from disabled).
    MONITORING_DISABLED = 7
    # The host is totally offline.
    OFFLINE = 8


class Host(Entity):
    """
    Represent an OpenNebula host.

    Parameters
    ----------
    session : Session
        The session associated with the host.
    id : int
        The unique identifier for the host.

    Attributes
    ----------
    cpu_maximum_ratio : LatestMetricValue
        The latest maximum CPU ratio metric for the host.
    cpu_total_ratio : LatestMetricValue
        The latest total CPU ratio metric for the host.
    cpu_usage_ratio : LatestMetricValue
        The latest CPU usage ratio metric for the host.
    cpu_ratio : LatestMetricValue
        The latest CPU ratio metric for the host.
    cpu_usage : LatestMetricValue
        The latest CPU usage metric for the host.
    cpu_seconds_total : LatestMetricValue
        The latest total CPU seconds metric for the host.
    mem_maximum_bytes : LatestMetricValue
        The latest maximum memory in bytes metric for the host.
    mem_total_bytes : LatestMetricValue
        The latest total memory in bytes metric for the host.
    mem_usage_bytes : LatestMetricValue
        The latest memory usage in bytes metric for the host.
    normalized_memory_usage : LatestMetricValue
        The latest normalized memory usage metric for the host.
    normalized_cpu_usage : LatestMetricValue
        The latest normalized CPU usage metric for the host.
    state : LatestMetricValue
        The latest state metric of the host.
    """

    __slots__ = ("_pci_devices",)

    def __init__(self, session: Session, id: int) -> None:
        super().__init__(session=session, id=id)
        self._pci_devices: PCIDevicePool | None = None

    @property
    def vms(self) -> virtual_machine.VirtualMachinePool:
        """Return the virtual machine pool associated with the host."""
        return virtual_machine.VirtualMachinePool(owner=self)

    @property
    def pci_devices(self) -> PCIDevicePool:
        """Return the PCI device pool associated with the host."""
        if self._pci_devices is None:
            data = self.get_data()["HOST_SHARE"]["PCI_DEVICES"]["PCI"]
            if not isinstance(data, list):
                data = [data]
            devices = [
                PCIDevice(
                    address=device_data["ADDRESS"],
                    short_address=device_data["SHORT_ADDRESS"],
                    vendor_id=device_data["VENDOR"],
                    vendor_name=device_data["VENDOR_NAME"],
                    device_id=device_data["DEVICE"],
                    device_name=device_data["DEVICE_NAME"],
                    class_id=device_data["CLASS"],
                    class_name=device_data["CLASS_NAME"],
                    type_label=device_data["TYPE"],
                    bus=device_data["BUS"],
                    slot=device_data["SLOT"],
                    numa_node=device_data["NUMA_NODE"],
                    domain=device_data["DOMAIN"],
                    function=device_data["FUNCTION"],
                    profiles=device_data.get("PROFILES"),
                    uu_id=device_data.get("UUID"),
                    vm_id=int(device_data["VMID"]),
                )
                for device_data in data
            ]
            self._pci_devices = PCIDevicePool(devices)
        return self._pci_devices

    cpu_maximum_ratio = LatestMetricValue(float)
    cpu_total_ratio = LatestMetricValue(float)
    cpu_usage_ratio = LatestMetricValue(float)
    cpu_ratio = LatestMetricValue(float)
    cpu_usage = LatestMetricValue(float)
    cpu_seconds_total = LatestMetricValue(float)
    mem_maximum_bytes = LatestMetricValue(float)
    mem_total_bytes = LatestMetricValue(float)
    mem_usage_bytes = LatestMetricValue(float)
    normalized_memory_usage = LatestMetricValue(float)
    normalized_cpu_usage = LatestMetricValue(float)
    state = LatestMetricValue(HostState)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        """
        Retrieve host information as XML string.

        Access the related information for the host from OpenNebula and
        return it as an XML string.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        str
            The XML string containing host information.
        """
        client = self.session.oned_client
        response = client.request("one.host.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        """
        Retrieve host information as a Python dictionary.

        Access the related information for the host from OpenNebula and
        return it as a Python dictionary.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        dict[str, Any]
            The dictionary containing host information.
        """
        client = self.session.oned_client
        data = client("one.host.info", self.id, decrypt_secrets)
        return data["HOST"]


class HostPool(Pool[Host]):
    """Represent a collection of Host entities."""

    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        return self.get_ids_from_datapool(
            client("one.hostpool.info")["HOST_POOL"], "HOST"
        )

    def _get_entity(self, id: int) -> Host:
        return Host(session=self.session, id=id)
