# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_vellum_value_request import ArrayVellumValueRequest
from .metadata_filter_rule_request import MetadataFilterRuleRequest
from .vellum_value_logical_condition_group_request import VellumValueLogicalConditionGroupRequest
import typing
import pydantic
from .search_weights_request import SearchWeightsRequest
from .search_result_merging_request import SearchResultMergingRequest
from .search_filters_request import SearchFiltersRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.pydantic_utilities import update_forward_refs


class SearchRequestOptionsRequest(UniversalBaseModel):
    limit: typing.Optional[int] = pydantic.Field(default=None)
    """
    The maximum number of results to return.
    """

    weights: typing.Optional[SearchWeightsRequest] = pydantic.Field(default=None)
    """
    The weights to use for the search. Must add up to 1.0.
    """

    result_merging: typing.Optional[SearchResultMergingRequest] = pydantic.Field(default=None)
    """
    The configuration for merging results.
    """

    filters: typing.Optional[SearchFiltersRequest] = pydantic.Field(default=None)
    """
    The filters to apply to the search.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVellumValueRequest, SearchRequestOptionsRequest=SearchRequestOptionsRequest)
update_forward_refs(MetadataFilterRuleRequest, SearchRequestOptionsRequest=SearchRequestOptionsRequest)
update_forward_refs(VellumValueLogicalConditionGroupRequest, SearchRequestOptionsRequest=SearchRequestOptionsRequest)
