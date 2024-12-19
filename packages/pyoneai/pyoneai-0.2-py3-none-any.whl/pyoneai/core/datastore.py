__all__ = [
    "Datastore",
    "DatastorePool",
]
from typing import Any

from .bases import Entity, LatestMetricValue, Pool
from .group import Group
from .image import ImagePool
from .user import User


class Datastore(Entity):
    """
    Represent an OpenNebula datastore.

    Attributes
    ----------
    free_bytes : LatestMetricValue
        The free bytes in the datastore.
    used_bytes : LatestMetricValue
        The used bytes in the datastore.
    total_bytes : LatestMetricValue
        The total bytes in the datastore.

    """

    __slots__ = ()

    @property
    def user(self) -> User:
        """Return the user that owns the datastore."""
        uid = int(self.get_data(decrypt_secrets=False)["UID"])
        return User(id=uid, session=self.session)

    @property
    def group(self) -> Group:
        """Return the group that owns the datastore."""
        guid = int(self.get_data(decrypt_secrets=False)["GID"])
        return Group(id=guid, session=self.session)

    @property
    def images(self) -> ImagePool:
        """Return the image pool of the datastore."""
        return ImagePool(owner=self)

    free_bytes = LatestMetricValue(float)
    used_bytes = LatestMetricValue(float)
    total_bytes = LatestMetricValue(float)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        """
        Retrieve datastore information as XML string.

        Access the related information for the datastore from
        OpenNebula and return it as an XML string.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        str
            The XML string containing datastore information.
        """
        client = self.session.oned_client
        response = client.request(
            "one.datastore.info", self.id, decrypt_secrets
        )
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        """
        Retrieve datastore information as a Python dict.

        Access the related information for the datastore from
        OpenNebula and return it as a Python dictionary.

        Parameters
        ----------
        decrypt_secrets : bool, default=False
            Whether to decrypt secrets in the response.

        Returns
        -------
        dict[str, Any]
            The dictionary containing datastore information.
        """
        client = self.session.oned_client
        data = client("one.datastore.info", self.id, decrypt_secrets)
        return data["DATASTORE"]


class DatastorePool(Pool):
    """Represent a collection of Datastore entities."""

    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        return self.get_ids_from_datapool(
            client("one.datastorepool.info")["DATASTORE_POOL"], "DATASTORE"
        )

    def _get_entity(self, id: int) -> Datastore:
        return Datastore(session=self.session, id=id)
