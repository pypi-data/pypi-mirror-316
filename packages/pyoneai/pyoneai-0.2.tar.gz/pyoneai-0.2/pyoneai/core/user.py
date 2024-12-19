__all__ = [
    "User",
    "UserPool",
]

from typing import Any

from .bases import Entity, Pool


class User(Entity):
    """Represent an OpenNebula user."""

    __slots__ = ()

    def get_info(self, decrypt_secrets: bool = False) -> str:
        """
        Retrieve user information as XML string.

        Access the related information for the user from OpenNebula
        and return it as an XML string.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        str
            The XML string containing user information.
        """
        client = self.session.oned_client
        response = client.request("one.user.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        """
        Retrieve user information as a Python dictionary.

        Access the related information for the user from OpenNebula
        and return it as a Python dictionary.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        dict[str, Any]
            The dictionary containing user information.
        """
        client = self.session.oned_client
        data = client("one.user.info", self.id, decrypt_secrets)
        return data["USER"]


class UserPool(Pool):
    """Represent a collection of User entities."""

    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        return self.get_ids_from_datapool(
            client("one.userpool.info")["USER_POOL"], "USER"
        )

    def _get_entity(self, id: int) -> User:
        return User(session=self.session, id=id)
