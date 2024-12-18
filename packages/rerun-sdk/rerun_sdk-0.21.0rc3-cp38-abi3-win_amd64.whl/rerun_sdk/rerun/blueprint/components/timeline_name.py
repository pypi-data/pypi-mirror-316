# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/blueprint/components/timeline_name.fbs".

# You can extend this class by creating a "TimelineNameExt" class in "timeline_name_ext.py".

from __future__ import annotations

from ... import datatypes
from ..._baseclasses import (
    ComponentBatchMixin,
    ComponentDescriptor,
    ComponentMixin,
)

__all__ = ["TimelineName", "TimelineNameBatch"]


class TimelineName(datatypes.Utf8, ComponentMixin):
    """**Component**: A timeline identified by its name."""

    _BATCH_TYPE = None
    # You can define your own __init__ function as a member of TimelineNameExt in timeline_name_ext.py

    # Note: there are no fields here because TimelineName delegates to datatypes.Utf8
    pass


class TimelineNameBatch(datatypes.Utf8Batch, ComponentBatchMixin):
    _COMPONENT_DESCRIPTOR: ComponentDescriptor = ComponentDescriptor("rerun.blueprint.components.TimelineName")


# This is patched in late to avoid circular dependencies.
TimelineName._BATCH_TYPE = TimelineNameBatch  # type: ignore[assignment]
