# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_vellum_value_request import ArrayVellumValueRequest
from .metadata_filter_rule_request import MetadataFilterRuleRequest
from .vellum_value_logical_condition_group_request import VellumValueLogicalConditionGroupRequest
import typing
import pydantic
from .metadata_filters_request import MetadataFiltersRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.pydantic_utilities import update_forward_refs


class SearchFiltersRequest(UniversalBaseModel):
    external_ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    The document external IDs to filter by
    """

    metadata: typing.Optional[MetadataFiltersRequest] = pydantic.Field(default=None)
    """
    The metadata filters to apply to the search
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVellumValueRequest, SearchFiltersRequest=SearchFiltersRequest)
update_forward_refs(MetadataFilterRuleRequest, SearchFiltersRequest=SearchFiltersRequest)
update_forward_refs(VellumValueLogicalConditionGroupRequest, SearchFiltersRequest=SearchFiltersRequest)
