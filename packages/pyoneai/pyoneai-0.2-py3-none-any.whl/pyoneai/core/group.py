__all__ = [
    "Group",
    "GroupPool",
]

from typing import Any

from .bases import Entity, Pool
from .user import UserPool


class Group(Entity):
    """Represent an OpenNebula user group."""

    __slots__ = ()

    @property
    def users(self) -> UserPool:
        """Return the user pool of the group."""
        return UserPool(owner=self)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        """
        Retrieve group information as XML string.

        Access the related information for the group from OpenNebula
        and return it as an XML string.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        str
            The XML string containing group information.
        """
        client = self.session.oned_client
        response = client.request("one.group.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        """
        Retrieve group information as a Python dictionary.

        Access the related information for the group from OpenNebula
        and return it as a Python dictionary.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        dict[str, Any]
            The dictionary containing group information.
        """
        client = self.session.oned_client
        data = client("one.group.info", self.id, decrypt_secrets)
        return data["GROUP"]


class GroupPool(Pool):
    """Represent a collection of Group entities."""

    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        return self.get_ids_from_datapool(
            client("one.grouppool.info")["GROUP_POOL"], "GROUP"
        )

    def _get_entity(self, id: int) -> Group:
        return Group(session=self.session, id=id)
