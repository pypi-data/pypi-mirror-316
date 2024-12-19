__all__ = ["One"]

from ..session import Session
from .bases import MetricBase
from .cluster import ClusterPool
from .datastore import DatastorePool
from .group import GroupPool
from .host import HostPool
from .image import ImagePool
from .user import UserPool
from .virtual_machine import VirtualMachinePool
from .virtual_network import VirtualNetworkPool


class One(MetricBase):
    """
    Represent OpenNebula and serve as the entry point for the SDK.

    Parameters
    ----------
    session : Session, default=None
        The configured OneAIOps session.
    """

    __slots__ = ()

    def __init__(self, session: Session | None = None) -> None:
        if session is None:
            session = Session()
        super().__init__(session=session)

    @property
    def clusters(self) -> ClusterPool:
        """
        Return the cluster pool containing all the clusters from
        OpenNebula.
        """
        return ClusterPool(owner=self)

    @property
    def datastores(self) -> DatastorePool:
        """
        Return the datastore pool containing all the datastores from
        OpenNebula.
        """
        return DatastorePool(owner=self)

    @property
    def groups(self) -> GroupPool:
        """
        Return the group pool containing all the groups from
        OpenNebula.
        """
        return GroupPool(owner=self)

    @property
    def hosts(self) -> HostPool:
        """
        Return the host pool containing all the hosts from OpenNebula.
        """
        return HostPool(owner=self)

    @property
    def images(self) -> ImagePool:
        """
        Return the image pool containing all the images from
        OpenNebula.
        """
        return ImagePool(owner=self)

    @property
    def users(self) -> UserPool:
        """
        Return the user pool containing all the users from OpenNebula.
        """
        return UserPool(owner=self)

    @property
    def vms(self) -> VirtualMachinePool:
        """
        Return the virtual machine pool containing all the VMs from
        OpenNebula.
        """
        return VirtualMachinePool(owner=self)

    @property
    def vnets(self) -> VirtualNetworkPool:
        """
        Return the virtual network pool containing all the VMs from
        OpenNebula.
        """
        return VirtualNetworkPool(owner=self)
