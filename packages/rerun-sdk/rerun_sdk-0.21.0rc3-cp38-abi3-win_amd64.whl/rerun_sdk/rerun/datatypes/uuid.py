# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/datatypes/uuid.fbs".

# You can extend this class by creating a "UuidExt" class in "uuid_ext.py".

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Union

import numpy as np
import numpy.typing as npt
import pyarrow as pa
from attrs import define, field

from .._baseclasses import (
    BaseBatch,
)
from .._converters import (
    to_np_uint8,
)
from .uuid_ext import UuidExt

__all__ = ["Uuid", "UuidArrayLike", "UuidBatch", "UuidLike"]


@define(init=False)
class Uuid(UuidExt):
    """**Datatype**: A 16-byte UUID."""

    def __init__(self: Any, bytes: UuidLike):
        """
        Create a new instance of the Uuid datatype.

        Parameters
        ----------
        bytes:
            The raw bytes representing the UUID.

        """

        # You can define your own __init__ function as a member of UuidExt in uuid_ext.py
        self.__attrs_init__(bytes=bytes)

    bytes: npt.NDArray[np.uint8] = field(converter=to_np_uint8)
    # The raw bytes representing the UUID.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    def __array__(self, dtype: npt.DTypeLike = None) -> npt.NDArray[Any]:
        # You can define your own __array__ function as a member of UuidExt in uuid_ext.py
        return np.asarray(self.bytes, dtype=dtype)


if TYPE_CHECKING:
    UuidLike = Union[Uuid, npt.NDArray[Any], npt.ArrayLike, Sequence[int], bytes]
else:
    UuidLike = Any

UuidArrayLike = Union[
    Uuid, Sequence[UuidLike], npt.NDArray[Any], npt.ArrayLike, Sequence[Sequence[int]], Sequence[int], Sequence[bytes]
]


class UuidBatch(BaseBatch[UuidArrayLike]):
    _ARROW_DATATYPE = pa.list_(pa.field("item", pa.uint8(), nullable=False, metadata={}), 16)

    @staticmethod
    def _native_to_pa_array(data: UuidArrayLike, data_type: pa.DataType) -> pa.Array:
        return UuidExt.native_to_pa_array_override(data, data_type)
