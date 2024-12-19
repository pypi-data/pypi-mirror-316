from __future__ import annotations

__all__ = ["Entity", "MetricBase", "Pool"]

import abc
from collections.abc import Collection, Iterator
from types import MappingProxyType
from typing import (
    Any,
    Generic,
    Self,
    SupportsInt,
    TypeGuard,
    TypeVar,
    overload,
)

import numpy as np
import pandas as pd

from ..session import Session
from .metric_collection import MetricCollection, PoolMetricCollection


class SessionBase(abc.ABC):
    """
    Abstract class for entities session.

    Ensure entities are associated with a session.

    Parameters
    ----------
    session : Session
        The session associated with the entity.

    Attributes
    ----------
    session : Session
        The session associated with the entity.
    """

    __slots__ = ("session",)

    session: Session

    @abc.abstractmethod
    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session


class MetricBase(SessionBase):
    """
    Base class for entities metrics.

    Ensure entities mantain a collection of metrics.

    Parameters
    ----------
    session : Session
        The session associated with the entity.

    Attributes
    ----------
    metrics : MetricCollection
        A collection of metrics associated with the entity.
    registry : MappingProxyType[str, Any]
        Registry configuration specific to the entity class.
    registry_default : MappingProxyType[str, Any]
        Default registry configuration.
    """

    __slots__ = ("metrics", "registry", "registry_default")

    metrics: MetricCollection
    registry: MappingProxyType[str, Any]
    registry_default: MappingProxyType[str, Any]

    @abc.abstractmethod
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)
        self.metrics = MetricCollection(self)
        registry = session.config.registry
        self.registry = registry[self.__class__.__name__.lower()]
        self.registry_default = registry["default"]


class Entity(MetricBase):
    """
    Represent an OpenNebula component.

    Represent an OpenNebula component. An Entity contains a unique ID
    (corresponding to the OpenNebula ID), a collection of metrics,
    and a Session.

    Parameters
    ----------
    session : Session
        The session associated with the entity.

    Attributes
    ----------
    id : int
        The unique identifier for the entity.
    """

    __slots__ = ("id",)

    id: int

    def __init__(self, session: Session, id: int) -> None:
        super().__init__(session=session)
        self.id = id


_T = TypeVar("_T")
_EntityT_co = TypeVar("_EntityT_co", bound=Entity, covariant=True)


class LatestMetricValue(Generic[_T]):
    """
    Descriptor for accessing the latest metric value.

    Retrieve the most recent value of a specified metric for an entity.
    Cast the retrieved value to the specified type.

    Parameters
    ----------
    cast : type[_T]
        The type to which the metric value should be cast.
    """

    __slots__ = ("_name", "_type")

    def __init__(self, cast: type[_T]) -> None:
        self._type = cast

    def __set_name__(self, owner: type[Entity], name: str) -> None:
        # pylint: disable=attribute-defined-outside-init
        self._name = name

    @overload
    def __get__(
        self, instance: None, owner: type[Entity] | None = None
    ) -> Self: ...

    @overload
    def __get__(
        self, instance: Entity, owner: type[Entity] | None = None
    ) -> _T: ...

    def __get__(
        self, instance: Entity | None, owner: type[Entity] | None = None
    ) -> Self | _T:
        # This part is optional and prevents errors in the case `Type.field`.
        if instance is None:
            return self

        try:
            value = instance.metrics[self._name]["0"].to_array(copy=False)[-1]
        except IndexError as err:
            raise RuntimeError(
                f"'instance' {instance.id} does not have any value for the "
                f"metric {self._name}"
            ) from err
        return self._type(value)  # type: ignore [call-arg]


# TODO: This function is defined also in `metric.py`. Put it at one
# place.
def _is_mask(mask: pd.Series) -> bool:
    return mask.dtype is np.dtype(bool) and mask.index.dtype.kind == "i"


# TODO: This function is defined also in `metric.py`. Put it at one
# place.
def _check_item_type(
    items: Collection[Any], item_type: type[_T]
) -> TypeGuard[Collection[_T]]:
    return all(isinstance(item, item_type) for item in items)


class Pool(Generic[_EntityT_co]):
    """
    Represent a collection of entities.

    Manage a collection of entities, allowing operations against them.
    Static pools store the IDs of the entities, while dynamic pools
    query OpenNebula each time to retrieve the IDs of the entities.

    Parameters
    ----------
    owner : Entity or One
        The owner of the pool.
    ids : Collection[int] or None, default=None
        A collection of entity identifiers, by default None.

    Attributes
    ----------
    metrics : PoolMetricCollection
        A collection of metrics associated with the pool.
    owner : Entity or One
        The owner of the pool.
    """

    __slots__ = ("_ids", "metrics", "owner")

    metrics: PoolMetricCollection

    def __init__(
        self, owner: Entity | One, ids: Collection[int] | None = None
    ) -> None:
        # TODO: Decide if it is better to keep IDs in a set or sequence.
        # TODO: Reconsider using an immutable collection (`frozenset`).
        if not (ids is None or isinstance(ids, set)):
            ids = set(ids)
        self._ids: set[int] | None = ids
        self.metrics = PoolMetricCollection(self)
        self.owner = owner

    @property
    def session(self) -> Session:
        """Return the session associated with the pool."""
        return self.owner.session

    @property
    def owner_id(self) -> int | None:
        """Return the ID of the owner of the pool."""
        return self.owner.id if isinstance(self.owner, Entity) else None

    # TODO: Consider making this a method. PEP 8 says: "Avoid using
    # properties for computationally expensive operations; the attribute
    # notation makes the caller believe that access is (relatively)
    # cheap".
    # See: https://peps.python.org/pep-0008/#designing-for-inheritance
    @property
    def ids(self) -> set[int]:
        """Return the IDs of the entities in the pool."""
        return self._get_system_ids() if self._ids is None else self._ids

    @abc.abstractmethod
    def _get_system_ids(self) -> set[int]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_entity(self, id: int) -> _EntityT_co:
        raise NotImplementedError()

    def __len__(self) -> int:
        return len(self.ids)

    def __iter__(self) -> Iterator[_EntityT_co]:
        return iter(self._get_entity(id) for id in self.ids)

    def __contains__(self, id: int) -> bool:
        return id in self.ids

    @staticmethod
    def get_ids_from_datapool(data_pool, attribute: str) -> set[int]:
        if data_pool:
            assert attribute in data_pool
            data = data_pool[attribute]
            if not isinstance(data, list):
                return {int(data["ID"])}
            return {int(entity_data["ID"]) for entity_data in data}
        else:
            return set()

    @overload
    def __getitem__(self, key: SupportsInt) -> _EntityT_co: ...

    @overload
    def __getitem__(
        self, key: Collection[SupportsInt] | pd.Series
    ) -> Self: ...

    def __getitem__(
        self, key: SupportsInt | Collection[SupportsInt] | pd.Series
    ) -> _EntityT_co | Self:
        match key:
            case int():
                if key in self.ids:
                    return self._get_entity(key)
                raise KeyError(f"'key' {key} not in the pool")
            case pd.Series() if _is_mask(key):
                return self[set(key[key].index)]
            case Collection() if _check_item_type(key, int):
                key_ids = key if isinstance(key, set) else set(key)
                own_ids = self.ids
                if not key_ids <= own_ids:
                    raise KeyError(
                        "'key' contains ids that are not in the pool: "
                        f"{sorted(key_ids - own_ids)}"
                    )
                return self.__class__(owner=self.owner, ids=key_ids)
            case Collection() if _check_item_type(key, SupportsInt):
                return self[set(map(int, key))]
            case SupportsInt():
                return self[int(key)]
            case _:
                raise TypeError(
                    "'key' must be int-like, collection, or series mask"
                )

    def get(self, key: int | Collection[int] | pd.Series, default=None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
