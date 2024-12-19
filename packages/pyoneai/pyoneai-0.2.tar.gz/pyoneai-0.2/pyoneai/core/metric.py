from __future__ import annotations

__all__ = ["Metric", "PoolMetric"]

import enum
from collections.abc import Callable, Collection, Iterator, Mapping, Sequence
from functools import wraps
from numbers import Real
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Self,
    SupportsIndex,
    TypeAlias,
    TypeGuard,
    TypeVar,
    overload,
)

import numpy as np
import numpy.typing as npt
import pandas as pd
import pandas.core.interchange.dataframe_protocol as dfp

if TYPE_CHECKING:
    from .entities import OnedEntity
    from .pool import Pool


# TODO: Modify `Metric` and `PoolMetric` according to `pandas` copy-on-write
# principle: https://pandas.pydata.org/docs/user_guide/copy_on_write.html.
# if pd.__version__ < '3':
#     pd.options.mode.copy_on_write = True


_T = TypeVar("_T")
_IntLikeKeys: TypeAlias = int | Collection[SupportsIndex]
_StrKeys: TypeAlias = str | Collection[str]


@enum.unique
class _FillMethod(enum.StrEnum):
    BACKWARD = enum.auto()
    FORWARD = enum.auto()
    LINEAR = enum.auto()


class Metric:
    """
    Represent a metric with associated time index and data.

    Provide functionalities to handle time-indexed data, perform
    arithmetic operations, and convert data to various formats.

    Parameters
    ----------
    time_index : npt.ArrayLike
        The time index associated with the metric.
    data : Mapping[str, npt.ArrayLike]
        The data associated with the metric.
    copy : bool, default=False
        If True, a copy of the data is made.
    """

    __slots__ = ("_df",)

    if TYPE_CHECKING:
        _df: pd.DataFrame

    _ROW_INDEX_NAME = "time"
    _COL_INDEX_NAME = "metric"

    def __init__(
        self,
        time_index: npt.ArrayLike,
        data: Mapping[str, npt.ArrayLike],
        copy: bool = False,
    ) -> None:
        df_index = self._create_index(time_index=time_index)
        df_data = self._create_data(data=data, copy=copy)
        self._df = pd.DataFrame(data=df_data, index=df_index, copy=False)
        self._df.columns.name = self._COL_INDEX_NAME

    @staticmethod
    def _check_time_index(time_index: pd.DatetimeIndex) -> None:
        if time_index.tz is None:
            raise ValueError("'time_index' does not have a time zone")
        if time_index.size > 0:
            if time_index.freq is None:
                raise ValueError("'time_index' cannot infer a frequency")
            # NOTE: It is possible to use `time_index.unique` and
            # `time_index.is_monotonically_increasing` here.
            if time_index.size > 1 and time_index[0] >= time_index[-1]:
                raise ValueError("'time_index' is not increasing")

    @classmethod
    def _create_index(cls, time_index: npt.ArrayLike) -> pd.DatetimeIndex:
        df_index = pd.DatetimeIndex(
            time_index, freq="infer", name=cls._ROW_INDEX_NAME
        )
        if df_index.size == 0 and df_index.tz is None:
            df_index = df_index.tz_localize("UTC")
        cls._check_time_index(time_index=df_index)
        return df_index

    @staticmethod
    def _check_data(data: dict[str, np.ndarray]) -> None:
        if not data:
            raise ValueError("'data' cannot be a zero-length collection")

    @classmethod
    def _create_data(
        cls, data: Mapping[str, npt.ArrayLike], copy: bool
    ) -> dict[str, np.ndarray]:
        df_data = {
            str(name): np.array(arr, copy=copy, ndmin=1)
            for name, arr in data.items()
        }
        cls._check_data(data=df_data)
        return df_data

    @property
    def time_index(self) -> pd.DatetimeIndex:
        """Return the time index associated with the metric."""
        return self._df.index

    @property
    def frequency(self) -> pd.Timedelta:
        """Return the frequency of the time index."""
        return pd.Timedelta(self._df.index.freq)

    @property
    def time_zone(self) -> str:
        """Return the time zone of the time index."""
        return str(self._df.index.tz)

    @property
    def names(self) -> pd.Index:
        """Return the names of the metrics."""
        return self._df.columns

    # @property
    # def __array_interface__(self) -> dict[str, Any]:
    #     return self._df.to_numpy(copy=False).__array_interface__

    def __array__(
        self, dtype: npt.DTypeLike | None = None, copy: bool | None = None
    ) -> np.ndarray:
        return self._df.__array__(dtype=dtype, copy=copy)

    def __dataframe__(
        self, nan_as_null: bool = False, allow_copy: bool = True
    ) -> dfp.DataFrame:
        return self._df.__dataframe__(allow_copy=allow_copy)

    def __len__(self) -> int:
        return len(self._df)

    def __getitem__(self, key: str) -> Self:
        name = str(key)
        new_df = self._df[name].to_frame(name=name)
        new_df.columns.name = self._COL_INDEX_NAME
        return self._new(new_df)

    def get(self, key: str, default: Any) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def item(self, index: SupportsIndex = 0) -> Any:
        return self.to_array(copy=False).item(index)

    def _can_compare_all(self, other: Self) -> bool:
        # Whether the expression ``np.all(x <op> y)`` can return `True`, where
        # `x` and `y` are instances of `Metric` and `<op>` is any comparison
        # operator.
        # pylint: disable=protected-access
        ldf = self._df
        rdf = other._df
        return (
            ldf.columns.size == rdf.columns.size
            and ldf.index.size == rdf.index.size
            and ldf.index.size > 0
            and bool(np.all(ldf.index == rdf.index))
        )

    def compare_all(
        self, other: Self, operator: Callable[[Self, Self], Self]
    ) -> bool:
        """
        Compare two Metric instances using a comparison operator.

        Parameters
        ----------
        other : Metric
            The other Metric instance to compare.
        operator : Callable[[Metric, Metric], Metric]
            The comparison operator to use.

        Returns
        -------
        bool
            `True` if all comparisons are `True`, `False` otherwise.
        """
        if not isinstance(other, self.__class__):
            raise TypeError(
                "'other' must be an instance of '{self.__class__.__name__}'"
            )
        if not self._can_compare_all(other):
            return False
        comp_result = operator(self, other)
        return bool(np.all(comp_result))

    def _apply(
        self, call: Callable[[np.ndarray, np.ndarray], np.ndarray], other: Self
    ) -> pd.DataFrame:
        # pylint: disable=protected-access
        ldf = self._df
        rdf = other._df
        if ldf.columns.size != rdf.columns.size:
            raise ValueError(f"'other' must have {ldf.columns.size} variables")
        ldf, rdf = ldf.align(rdf, join="outer", axis=0, copy=False)
        df_index = self._create_index(time_index=ldf.index)
        df_data = call(ldf.to_numpy(copy=False), rdf.to_numpy(copy=False))
        df_columns = ldf.columns
        return pd.DataFrame(data=df_data, index=df_index, columns=df_columns)

    @staticmethod
    def _operator(method: Callable) -> Callable:
        method_name = method.__name__
        np_method = getattr(np.ndarray, method_name)
        df_method = getattr(pd.DataFrame, method_name)

        @wraps(method)
        def result(self, other):
            # pylint: disable=protected-access
            match other:
                case self.__class__():
                    return self._new(self._apply(call=np_method, other=other))
                case Real():
                    return self._new(df_method(self._df, other))
                case _:
                    return NotImplemented

        return result

    @_operator
    def __eq__(self, other):
        """Return ``self == other``."""

    @_operator
    def __ne__(self, other):
        """Return ``self != other``."""

    @_operator
    def __lt__(self, other):
        """Return ``self < other``."""

    @_operator
    def __le__(self, other):
        """Return ``self <= other``."""

    @_operator
    def __gt__(self, other):
        """Return ``self > other``."""

    @_operator
    def __ge__(self, other):
        """Return ``self >= other``."""

    @_operator
    def __add__(self, other):
        """Return ``self + other``."""

    @_operator
    def __sub__(self, other):
        """Return ``self - other``."""

    @_operator
    def __mul__(self, other):
        """Return ``self * other``."""

    @_operator
    def __radd__(self, other):
        pass

    @_operator
    def __rsub__(self, other):
        pass

    @_operator
    def __rmul__(self, other):
        pass

    def __str__(self) -> str:
        return str(self._df)

    def __repr__(self) -> str:
        return repr(self._df)

    def _repr_html_(self) -> str | None:
        return self._df._repr_html_()

    def _repr_latex_(self) -> str | None:
        return self._df._repr_latex_()

    @classmethod
    def _new(cls, data: pd.DataFrame) -> Self:
        # Fast path to create a `Metric` instance without calling `__init__`.
        metric = object.__new__(cls)
        metric._df = data
        return metric

    @classmethod
    def from_dataframe(cls, data: pd.DataFrame, copy: bool = False) -> Self:
        """
        Create a Metric instance from a pandas DataFrame.

        Parameters
        ----------
        data : pd.DataFrame
            The DataFrame containing the metric data.
        copy : bool, default=False
            If True, a copy of the data is made.

        Returns
        -------
        Metric
            A new Metric instance.
        """
        df_index = data.index
        df_data = {
            name: data[name].to_numpy(copy=False)
            for name in data.columns.to_numpy(copy=False).flat
        }
        return cls(time_index=df_index, data=df_data, copy=copy)

    @classmethod
    def from_series(cls, data: pd.Series, copy: bool = False) -> Self:
        """
        Create a Metric instance from a pandas Series.

        Parameters
        ----------
        data : pd.Series
            The Series containing the metric data.
        copy : bool, default=False
            If True, a copy of the data is made.

        Returns
        -------
        Metric
            A new Metric instance.
        """
        df_index = data.index
        df_data = {data.name: data.to_numpy(copy=False)}
        return cls(time_index=df_index, data=df_data, copy=copy)

    @classmethod
    def multivariate(cls, data: Collection[Self], copy: bool = False) -> Self:
        """
        Combine multiple metrics into a multivariate Metric.

        Create a multivariate Metric instance by combining multiple
        Metric instances into one multivariate Metric.

        Parameters
        ----------
        data : Collection[Metric]
            A collection of Metric instances to combine.
        copy : bool, optional
            If True, a copy of the data is made.

        Returns
        -------
        Metric
            A new multivariate Metric instance.
        """
        metrics = []
        for metric in data:
            if not isinstance(metric, cls):
                raise TypeError(
                    f"'data' must be a collection of '{cls.__name__}' "
                    "instances"
                )
            metrics.append(metric._df)

        new_df = pd.concat(
            metrics,
            axis=1,
            join="outer",
            ignore_index=False,
            verify_integrity=False,
            sort=False,
            copy=copy,
        )
        cls._check_time_index(time_index=new_df.index)
        return cls._new(data=new_df)

    def to_dataframe(self, copy: bool = False) -> pd.DataFrame:
        """
        Convert the Metric instance to a pandas DataFrame.

        Parameters
        ----------
        copy : bool, default=False
            If True, a copy of the DataFrame is returned.

        Returns
        -------
        pd.DataFrame
            The metric data as a DataFrame.
        """
        return self._df.copy(deep=True) if copy else self._df

    def to_series(self, copy: bool = False) -> list[pd.Series]:
        """
        Convert the Metric instance to a list of pandas Series.

        Parameters
        ----------
        copy : bool, default=False
            If True, copies of the Series are returned.

        Returns
        -------
        list[pd.Series]
            The metric data as a list of Series.
        """
        data = self._df
        return [
            data[name].copy(deep=True) if copy else data[name]
            for name in data.columns.to_numpy(copy=False).flat
        ]

    def to_array(
        self, dtype: npt.DTypeLike | None = None, copy: bool = False
    ) -> np.ndarray:
        """
        Convert the Metric instance to a NumPy array.

        Parameters
        ----------
        dtype : npt.DTypeLike, optional
            Desired data type of the array.
        copy : bool, optional
            If True, a copy of the array is made.

        Returns
        -------
        np.ndarray
            The metric data as a NumPy array.
        """
        return self._df.to_numpy(dtype=dtype, copy=copy)

    def univariate(self, copy: bool = False) -> list[Self]:
        """
        Split multivariate Metric into a list of univariate Metrics.

        Parameters
        ----------
        copy : bool, default=False
            If True, copies of the data are made.

        Returns
        -------
        list[Metric]
            A list of univariate Metric instances.
        """
        cls = self.__class__  # Or type(self).
        return [
            cls.from_series(data=ser, copy=copy)
            for ser in self.to_series(copy=False)
        ]

    def append(self, other: Self) -> Self:
        """
        Append another Metric instance to the current one.

        Parameters
        ----------
        other : Metric
            The Metric instance to append.

        Returns
        -------
        Metric
            A new Metric instance with the appended data.
        """
        cls = self.__class__  # Or type(self).
        if not isinstance(other, cls):
            raise TypeError(f"'other' must be an instance of '{cls.__name__}'")
        new_df = pd.concat(
            [self._df, other._df],
            axis=0,
            join="outer",
            ignore_index=False,
            verify_integrity=False,
            sort=False,
            copy=True,
        )
        self._check_time_index(time_index=new_df.index)
        return self._new(data=new_df)

    def fill_missing_values(
        self, method: Literal["backward", "forward", "linear"] = "linear"
    ) -> Self:
        """
        Fill missing values in the Metric using the declared method.

        Parameters
        ----------
        method : {'backward', 'forward', 'linear'}, default='linear'
            The method to use for filling missing values.

        Returns
        -------
        Metric
            A new Metric instance with filled missing values.
        """
        new_df: pd.DataFrame
        match _FillMethod(method):
            case _FillMethod.BACKWARD:
                new_df = self._df.bfill(axis=0)
            case _FillMethod.FORWARD:
                new_df = self._df.ffill(axis=0)
            case _FillMethod.LINEAR:
                new_df = self._df.interpolate(
                    method="linear", axis=0, limit_direction="both"
                )
        return self._new(data=new_df)

    def rename(self, names: Mapping[str, str], copy: bool = False) -> Self:
        """
        Rename the data series in the Metric.

        Rename the data series in the Metric instance according to the
        provided mapping.

        Parameters
        ----------
        names : Mapping[str, str]
            A dictionary mapping old column names to new ones.
        copy : bool, default=False
            If True, a copy of the data is made.

        Returns
        -------
        Metric
            A new Metric instance with renamed data series.
        """
        names = {str(old): str(new) for old, new in names.items()}
        new_df = self._df.rename(columns=names, inplace=False, copy=copy)
        return self._new(data=new_df)


def _is_mask(mask: pd.Series) -> bool:
    return mask.dtype is np.dtype(bool) and mask.index.dtype.kind == "i"


def _check_item_type(
    items: Collection[Any], item_type: type[_T]
) -> TypeGuard[Collection[_T]]:
    return all(isinstance(item, item_type) for item in items)


class PoolMetric:
    """
    Represent a collection of metrics associated with a pool.

    Provide functionalities to manage and manipulate multiple metrics
    associated with a pool of entities.

    Parameters
    ----------
    pool : Pool
        The pool associated with the metrics.
    metrics : Sequence[Metric] or Mapping[int, Metric]
        The metrics to associate with the pool.
    """

    __slots__ = ("_pool", "_metrics")

    if TYPE_CHECKING:
        _pool: Pool
        _metrics: dict[int, Metric]

    def __init__(
        self, pool: Pool, metrics: Sequence[Metric] | Mapping[int, Metric]
    ) -> None:
        self._pool = pool
        match metrics:
            case Sequence():
                pairs = zip(pool, metrics, strict=True)
                self._metrics = {entity.id: metric for entity, metric in pairs}
            case Mapping():
                self._metrics = {id_: metrics[id_] for id_ in pool.ids}
            case _:
                raise TypeError("'metrics' must be a sequence or mapping")

    @classmethod
    def _new(cls, pool: Pool, metrics: dict[int, Metric]) -> Self:
        # Fast path to instantiate `PoolMetric` without calling `__init__`.
        pool_metric = object.__new__(cls)
        pool_metric._pool = pool
        pool_metric._metrics = metrics
        return pool_metric

    @property
    def ids(self) -> list[int]:
        """Return the IDs of the entities in the pool."""
        return self._pool.ids

    @property
    def pool(self) -> Pool:
        """Return the pool associated with the metrics."""
        return self._pool

    @property
    def metrics(self) -> dict[int, Metric]:
        """Return the metrics associated with the pool."""
        return self._metrics

    @staticmethod
    def _comparison_operator(method: Callable) -> Callable:
        metric_method = getattr(Metric, method.__name__)

        @wraps(method)
        def result(self, other):
            # pylint: disable=protected-access
            match other:
                case Metric():
                    mask = {}
                    for id_, metric in self._metrics.items():
                        mask[id_] = metric.compare_all(other, metric_method)
                    return pd.Series(data=mask, dtype=bool)
                case Real():
                    mask = {}
                    for id_, metric in self._metrics.items():
                        mask[id_] = len(metric) and np.all(
                            metric_method(metric, other)
                        )
                    return pd.Series(data=mask, dtype=bool)
                case self.__class__():
                    raise NotImplementedError()
                case _:
                    return NotImplemented

        return result

    @staticmethod
    def _arithmetic_operator(method: Callable) -> Callable:
        metric_method = getattr(Metric, method.__name__)

        @wraps(method)
        def result(self, other):
            # pylint: disable=protected-access
            match other:
                case Metric() | Real():
                    new_metrics = {
                        id_: metric_method(metric, other)
                        for id_, metric in self._metrics.items()
                    }
                case self.__class__():
                    if self._pool is not other._pool:
                        raise ValueError("'other' does not have the same pool")
                    new_metrics = {
                        id_: metric_method(left_metric, right_metric)
                        for (id_, left_metric), right_metric in zip(
                            self._metrics.items(), other.metrics.values()
                        )
                    }
                case _:
                    return NotImplemented
            return self._new(pool=self._pool, metrics=new_metrics)

        return result

    @_comparison_operator
    def __eq__(self, other):
        """Return ``self == other``."""

    @_comparison_operator
    def __ne__(self, other):
        """Return ``self != other``."""

    @_comparison_operator
    def __lt__(self, other):
        """Return ``self < other``."""

    @_comparison_operator
    def __le__(self, other):
        """Return ``self <= other``."""

    @_comparison_operator
    def __gt__(self, other):
        """Return ``self > other``."""

    @_comparison_operator
    def __ge__(self, other):
        """Return ``self >= other``."""

    @_arithmetic_operator
    def __add__(self, other):
        """Return ``self + other``."""

    @_arithmetic_operator
    def __sub__(self, other):
        """Return ``self - other``."""

    @_arithmetic_operator
    def __mul__(self, other):
        """Return ``self * other``."""

    @_arithmetic_operator
    def __radd__(self, other):
        pass

    @_arithmetic_operator
    def __rsub__(self, other):
        pass

    @_arithmetic_operator
    def __rmul__(self, other):
        pass

    def __len__(self) -> int:
        return len(self._metrics)

    def __iter__(self) -> Iterator[tuple[OnedEntity, Metric]]:
        return iter(zip(self._pool, self._metrics.values()))

    def _get(self, ids: Collection[int]) -> Self:
        new_pool = self._pool[ids]
        old_metrics = self._metrics
        new_metrics = {id_: old_metrics[id_] for id_ in new_pool.ids}
        return self._new(pool=new_pool, metrics=new_metrics)

    @overload
    def __getitem__(self, key: _StrKeys | Collection | pd.Series) -> Self: ...

    @overload
    def __getitem__(self, key: int) -> Metric: ...

    def __getitem__(
        self, key: tuple | _StrKeys | _IntLikeKeys | pd.Series
    ) -> Self | Metric:
        match key:
            case str():
                # Indexing with a string metric name.
                new_metrics = {
                    id_: metric[key] for id_, metric in self._metrics.items()
                }
                return self._new(pool=self._pool, metrics=new_metrics)
            case pd.Series() if _is_mask(key):
                # Indexing with a mask given as `pandas.Series` instance.
                return self._get(ids=list(key[key].index))
            case int():
                # Indexing with an int ID.
                return self._metrics[key]
            case tuple():
                # Indexing with a tuple in a recursive way.
                # NOTE: It is more efficient to index by ID(s)/mask first and
                # then by metric name(s).
                result = self
                for criterion in key:
                    result = result[criterion]
                return result
            case Collection() if _check_item_type(key, str):
                # Indexing with a collection of string metric names.
                new_metrics = {
                    id_: Metric.multivariate(
                        data=[metric[name] for name in key], copy=False
                    )
                    for id_, metric in self._metrics.items()
                }
                return self._new(pool=self._pool, metrics=new_metrics)
            case Collection() if _check_item_type(key, int):
                # Indexing with a collection of int IDs.
                return self._get(ids=key)
            case Collection() if _check_item_type(key, SupportsIndex):
                # Indexing with a collection of int-like IDs.
                # NOTE: NumPy integer and float arrays should work.
                return self._get(ids=[id_.__index__() for id_ in key])
            case _:
                raise KeyError("'key' cannot be used")

    def get(
        self,
        key: tuple | _StrKeys | _IntLikeKeys | pd.Series,
        default: Any = None,
    ) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def rename(self, names: Mapping[str, str], copy: bool = False) -> Self:
        """
        Rename the data series in the Metrics.

        Rename the variables for all Metric instances in the pool,
        according to the provided mapping.

        Parameters
        ----------
        names : Mapping[str, str]
            A dictionary mapping old column names to new ones.
        copy : bool, default=False
            If True, a copy of the data is made.

        Returns
        -------
        PoolMetric
            A new PoolMetric instance with renamed data series.
        """
        new_metrics = {
            id_: metric.rename(names=names, copy=copy)
            for id_, metric in self._metrics.items()
        }
        return type(self)(pool=self._pool, metrics=new_metrics)
