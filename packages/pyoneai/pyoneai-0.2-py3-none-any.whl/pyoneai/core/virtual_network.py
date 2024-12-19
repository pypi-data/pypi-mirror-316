__all__ = [
    "VirtualNetwork",
    "VirtualNetworkPool",
]

from typing import Any

from .bases import Entity, Pool
from .group import Group
from .user import User


class VirtualNetwork(Entity):
    """Represent an OpenNebula virtual network."""

    __slots__ = ()

    @property
    def user(self) -> User:
        """Return the user that owns the virtual network."""
        uid = int(self.get_data(decrypt_secrets=False)["UID"])
        return User(id=uid, session=self.session)

    @property
    def group(self) -> Group:
        """Return the group that owns the virtual network."""
        guid = int(self.get_data(decrypt_secrets=False)["GID"])
        return Group(id=guid, session=self.session)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        """
        Retrieve virtual network information as XML string.

        Access the related information for the virtual network from
        OpenNebula and return it as an XML string.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        str
            The XML string containing virtual network information.
        """
        client = self.session.oned_client
        response = client.request("one.vn.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        """
        Retrieve virtual network information as a Python dictionary.

        Access the related information for the virtual network from
        OpenNebula and return it as a Python dictionary.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        dict[str, Any]
            The dictionary containing virtual network information.
        """
        client = self.session.oned_client
        data = client("one.vn.info", self.id, decrypt_secrets)
        return data["VNET"]


class VirtualNetworkPool(Pool):
    """Represent a collection of OpenNebula virtual networks."""

    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        return self.get_ids_from_datapool(
            client("one.vnpool.info", -2, -1, -1)["VNET_POOL"], "VNET"
        )

    def _get_entity(self, id: int) -> VirtualNetwork:
        return VirtualNetwork(session=self.session, id=id)
