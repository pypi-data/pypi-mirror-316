from typing import Any

from .bases import Entity, Pool
from .group import Group
from .user import User


class Image(Entity):
    """Represent an OpenNebula image."""

    __slots__ = ()

    @property
    def user(self) -> User:
        """Return the user that owns the image."""
        uid = int(self.get_data(decrypt_secrets=False)["UID"])
        return User(id=uid, session=self.session)

    @property
    def group(self) -> Group:
        """Return the group that owns the image."""
        guid = int(self.get_data(decrypt_secrets=False)["GID"])
        return Group(id=guid, session=self.session)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        """
        Retrieve image information as XML string.

        Access the related information for the image from OpenNebula
        and return it as an XML string.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        str
            The XML string containing image information.
        """
        client = self.session.oned_client
        response = client.request("one.image.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        """
        Retrieve image information as a Python dictionary.

        Access the related information for the image from OpenNebula
        and return it as a Python dictionary.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        dict[str, Any]
            The dictionary containing image information.
        """
        client = self.session.oned_client
        data = client("one.image.info", self.id, decrypt_secrets)
        return data["IMAGE"]


class ImagePool(Pool):
    """Represent a collection of Image entities."""

    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        from .datastore import Datastore

        client = self.session.oned_client
        # Get Images from the owner datastore
        if isinstance(self.owner, Datastore):
            data = client("one.datastore.info", self.owner_id)["DATASTORE"][
                "IMAGES"
            ]
            if data is None:
                return set()
            return {int(id_) for id_ in data["ID"]}
        # Get all system Images
        else:
            return self.get_ids_from_datapool(
                client("one.imagepool.info", -2, -1, -1)["IMAGE_POOL"], "IMAGE"
            )

    def _get_entity(self, id: int) -> Image:
        return Image(session=self.session, id=id)
