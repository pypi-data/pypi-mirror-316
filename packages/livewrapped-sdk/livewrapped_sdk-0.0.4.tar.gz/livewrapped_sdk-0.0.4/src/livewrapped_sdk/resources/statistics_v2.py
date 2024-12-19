#  See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..types import statistics_v2_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.stats_response import StatsResponse

__all__ = ["StatisticsV2Resource", "AsyncStatisticsV2Resource"]


class StatisticsV2Resource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StatisticsV2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return StatisticsV2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StatisticsV2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return StatisticsV2ResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ad_unit_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        advertiser_domains: Optional[List[str]] | NotGiven = NOT_GIVEN,
        advertiser_names: Optional[List[str]] | NotGiven = NOT_GIVEN,
        agencies: Optional[List[str]] | NotGiven = NOT_GIVEN,
        aggregate_ad_units: bool | NotGiven = NOT_GIVEN,
        aggregate_advertiser_domains: bool | NotGiven = NOT_GIVEN,
        aggregate_advertiser_names: bool | NotGiven = NOT_GIVEN,
        aggregate_agencies: bool | NotGiven = NOT_GIVEN,
        aggregate_browser: bool | NotGiven = NOT_GIVEN,
        aggregate_buyers: bool | NotGiven = NOT_GIVEN,
        aggregate_cookie_support: bool | NotGiven = NOT_GIVEN,
        aggregate_deals: bool | NotGiven = NOT_GIVEN,
        aggregate_livewrapped_deals: bool | NotGiven = NOT_GIVEN,
        aggregate_publishers: bool | NotGiven = NOT_GIVEN,
        aggregate_resellers: bool | NotGiven = NOT_GIVEN,
        aggregate_seats: bool | NotGiven = NOT_GIVEN,
        aggregate_sites: bool | NotGiven = NOT_GIVEN,
        aggregate_time: bool | NotGiven = NOT_GIVEN,
        aggregate_topics: bool | NotGiven = NOT_GIVEN,
        aggregation_level: Literal | NotGiven = NOT_GIVEN,
        avoid_client_aggregation: bool | NotGiven = NOT_GIVEN,
        buyer_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        currency: Optional[str] | NotGiven = NOT_GIVEN,
        deal_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        experiment: int | NotGiven = NOT_GIVEN,
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        include_avails: bool | NotGiven = NOT_GIVEN,
        include_bid_levels: bool | NotGiven = NOT_GIVEN,
        include_deal_statistics: bool | NotGiven = NOT_GIVEN,
        include_errors: bool | NotGiven = NOT_GIVEN,
        include_formats: bool | NotGiven = NOT_GIVEN,
        include_no_bid_responses: bool | NotGiven = NOT_GIVEN,
        include_response_times: bool | NotGiven = NOT_GIVEN,
        include_sold_statistics: bool | NotGiven = NOT_GIVEN,
        include_stats_buyers: bool | NotGiven = NOT_GIVEN,
        include_sub_set_publishers: bool | NotGiven = NOT_GIVEN,
        include_user_statistics: Literal | NotGiven = NOT_GIVEN,
        inverse_ad_units: bool | NotGiven = NOT_GIVEN,
        livewrapped_deal_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        master_publisher_id: Optional[str] | NotGiven = NOT_GIVEN,
        publisher_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        query_hour_resolution: bool | NotGiven = NOT_GIVEN,
        reseller_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        seat_names: Optional[List[str]] | NotGiven = NOT_GIVEN,
        site_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        time_zone: Optional[str] | NotGiven = NOT_GIVEN,
        to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatsResponse:
        """
        Args:
          advertiser_domains: Filter sold statistics on advertiser domain (and name if available).

          aggregate_browser: When retrieving browser caps, aggregate browser.

          aggregate_cookie_support: When retrieving browser caps, aggregate cookie support.

          aggregate_topics: When retrieving browser caps, aggregate Topics information.

          avoid_client_aggregation: Do not run operations that require client aggregation and do only database
              aggregations.

          deal_ids: List of deal IDs sent from SSPs.

          experiment: Read from an experiment database by index. Ignore to read from main database,

          from_: The From date is inclusive.

          include_bid_levels: Will force client aggregation which is resource heavy. Only use if required.

          include_deal_statistics: Include Deal statistics if this is collected. This can not be combined with
              other includes.

          include_errors: Include rendering errors. Will force client aggregation which is resource heavy.
              Only use if required.

          include_no_bid_responses: Will force client aggregation which is resource heavy. Only use if required.

          include_response_times: Will force client aggregation which is resource heavy. Only use if required.

          include_sold_statistics: Include Advertiser statistics and collected deals statistics if those are
              collected. This can not be combined with other includes.

          include_stats_buyers: Include imported statistics not from the Header Bidding auction such as ad
              server statistics.

          include_sub_set_publishers: Include publishers not owned by the account but with statistics access.

          livewrapped_deal_ids: List of Livewrapped-defined IDs of deals created in Livewrapped's console/API.

          query_hour_resolution: By default, From and To will be adjusted to include full days from midnight to
              midnight. If AggregationLevel is Hour, setting this to true will allow From and
              To to be specified on hour resolution.

          to: The To date is inclusive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/Statistics",
            body=maybe_transform(
                {
                    "ad_unit_ids": ad_unit_ids,
                    "advertiser_domains": advertiser_domains,
                    "advertiser_names": advertiser_names,
                    "agencies": agencies,
                    "aggregate_ad_units": aggregate_ad_units,
                    "aggregate_advertiser_domains": aggregate_advertiser_domains,
                    "aggregate_advertiser_names": aggregate_advertiser_names,
                    "aggregate_agencies": aggregate_agencies,
                    "aggregate_browser": aggregate_browser,
                    "aggregate_buyers": aggregate_buyers,
                    "aggregate_cookie_support": aggregate_cookie_support,
                    "aggregate_deals": aggregate_deals,
                    "aggregate_livewrapped_deals": aggregate_livewrapped_deals,
                    "aggregate_publishers": aggregate_publishers,
                    "aggregate_resellers": aggregate_resellers,
                    "aggregate_seats": aggregate_seats,
                    "aggregate_sites": aggregate_sites,
                    "aggregate_time": aggregate_time,
                    "aggregate_topics": aggregate_topics,
                    "aggregation_level": aggregation_level,
                    "avoid_client_aggregation": avoid_client_aggregation,
                    "buyer_ids": buyer_ids,
                    "currency": currency,
                    "deal_ids": deal_ids,
                    "experiment": experiment,
                    "from_": from_,
                    "include_avails": include_avails,
                    "include_bid_levels": include_bid_levels,
                    "include_deal_statistics": include_deal_statistics,
                    "include_errors": include_errors,
                    "include_formats": include_formats,
                    "include_no_bid_responses": include_no_bid_responses,
                    "include_response_times": include_response_times,
                    "include_sold_statistics": include_sold_statistics,
                    "include_stats_buyers": include_stats_buyers,
                    "include_sub_set_publishers": include_sub_set_publishers,
                    "include_user_statistics": include_user_statistics,
                    "inverse_ad_units": inverse_ad_units,
                    "livewrapped_deal_ids": livewrapped_deal_ids,
                    "master_publisher_id": master_publisher_id,
                    "publisher_ids": publisher_ids,
                    "query_hour_resolution": query_hour_resolution,
                    "reseller_ids": reseller_ids,
                    "seat_names": seat_names,
                    "site_ids": site_ids,
                    "time_zone": time_zone,
                    "to": to,
                },
                statistics_v2_create_params.StatisticsV2CreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StatsResponse,
        )


class AsyncStatisticsV2Resource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStatisticsV2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncStatisticsV2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStatisticsV2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AsyncStatisticsV2ResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ad_unit_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        advertiser_domains: Optional[List[str]] | NotGiven = NOT_GIVEN,
        advertiser_names: Optional[List[str]] | NotGiven = NOT_GIVEN,
        agencies: Optional[List[str]] | NotGiven = NOT_GIVEN,
        aggregate_ad_units: bool | NotGiven = NOT_GIVEN,
        aggregate_advertiser_domains: bool | NotGiven = NOT_GIVEN,
        aggregate_advertiser_names: bool | NotGiven = NOT_GIVEN,
        aggregate_agencies: bool | NotGiven = NOT_GIVEN,
        aggregate_browser: bool | NotGiven = NOT_GIVEN,
        aggregate_buyers: bool | NotGiven = NOT_GIVEN,
        aggregate_cookie_support: bool | NotGiven = NOT_GIVEN,
        aggregate_deals: bool | NotGiven = NOT_GIVEN,
        aggregate_livewrapped_deals: bool | NotGiven = NOT_GIVEN,
        aggregate_publishers: bool | NotGiven = NOT_GIVEN,
        aggregate_resellers: bool | NotGiven = NOT_GIVEN,
        aggregate_seats: bool | NotGiven = NOT_GIVEN,
        aggregate_sites: bool | NotGiven = NOT_GIVEN,
        aggregate_time: bool | NotGiven = NOT_GIVEN,
        aggregate_topics: bool | NotGiven = NOT_GIVEN,
        aggregation_level: Literal | NotGiven = NOT_GIVEN,
        avoid_client_aggregation: bool | NotGiven = NOT_GIVEN,
        buyer_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        currency: Optional[str] | NotGiven = NOT_GIVEN,
        deal_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        experiment: int | NotGiven = NOT_GIVEN,
        from_: Union[str, datetime] | NotGiven = NOT_GIVEN,
        include_avails: bool | NotGiven = NOT_GIVEN,
        include_bid_levels: bool | NotGiven = NOT_GIVEN,
        include_deal_statistics: bool | NotGiven = NOT_GIVEN,
        include_errors: bool | NotGiven = NOT_GIVEN,
        include_formats: bool | NotGiven = NOT_GIVEN,
        include_no_bid_responses: bool | NotGiven = NOT_GIVEN,
        include_response_times: bool | NotGiven = NOT_GIVEN,
        include_sold_statistics: bool | NotGiven = NOT_GIVEN,
        include_stats_buyers: bool | NotGiven = NOT_GIVEN,
        include_sub_set_publishers: bool | NotGiven = NOT_GIVEN,
        include_user_statistics: Literal | NotGiven = NOT_GIVEN,
        inverse_ad_units: bool | NotGiven = NOT_GIVEN,
        livewrapped_deal_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        master_publisher_id: Optional[str] | NotGiven = NOT_GIVEN,
        publisher_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        query_hour_resolution: bool | NotGiven = NOT_GIVEN,
        reseller_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        seat_names: Optional[List[str]] | NotGiven = NOT_GIVEN,
        site_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        time_zone: Optional[str] | NotGiven = NOT_GIVEN,
        to: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StatsResponse:
        """
        Args:
          advertiser_domains: Filter sold statistics on advertiser domain (and name if available).

          aggregate_browser: When retrieving browser caps, aggregate browser.

          aggregate_cookie_support: When retrieving browser caps, aggregate cookie support.

          aggregate_topics: When retrieving browser caps, aggregate Topics information.

          avoid_client_aggregation: Do not run operations that require client aggregation and do only database
              aggregations.

          deal_ids: List of deal IDs sent from SSPs.

          experiment: Read from an experiment database by index. Ignore to read from main database,

          from_: The From date is inclusive.

          include_bid_levels: Will force client aggregation which is resource heavy. Only use if required.

          include_deal_statistics: Include Deal statistics if this is collected. This can not be combined with
              other includes.

          include_errors: Include rendering errors. Will force client aggregation which is resource heavy.
              Only use if required.

          include_no_bid_responses: Will force client aggregation which is resource heavy. Only use if required.

          include_response_times: Will force client aggregation which is resource heavy. Only use if required.

          include_sold_statistics: Include Advertiser statistics and collected deals statistics if those are
              collected. This can not be combined with other includes.

          include_stats_buyers: Include imported statistics not from the Header Bidding auction such as ad
              server statistics.

          include_sub_set_publishers: Include publishers not owned by the account but with statistics access.

          livewrapped_deal_ids: List of Livewrapped-defined IDs of deals created in Livewrapped's console/API.

          query_hour_resolution: By default, From and To will be adjusted to include full days from midnight to
              midnight. If AggregationLevel is Hour, setting this to true will allow From and
              To to be specified on hour resolution.

          to: The To date is inclusive.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/Statistics",
            body=await async_maybe_transform(
                {
                    "ad_unit_ids": ad_unit_ids,
                    "advertiser_domains": advertiser_domains,
                    "advertiser_names": advertiser_names,
                    "agencies": agencies,
                    "aggregate_ad_units": aggregate_ad_units,
                    "aggregate_advertiser_domains": aggregate_advertiser_domains,
                    "aggregate_advertiser_names": aggregate_advertiser_names,
                    "aggregate_agencies": aggregate_agencies,
                    "aggregate_browser": aggregate_browser,
                    "aggregate_buyers": aggregate_buyers,
                    "aggregate_cookie_support": aggregate_cookie_support,
                    "aggregate_deals": aggregate_deals,
                    "aggregate_livewrapped_deals": aggregate_livewrapped_deals,
                    "aggregate_publishers": aggregate_publishers,
                    "aggregate_resellers": aggregate_resellers,
                    "aggregate_seats": aggregate_seats,
                    "aggregate_sites": aggregate_sites,
                    "aggregate_time": aggregate_time,
                    "aggregate_topics": aggregate_topics,
                    "aggregation_level": aggregation_level,
                    "avoid_client_aggregation": avoid_client_aggregation,
                    "buyer_ids": buyer_ids,
                    "currency": currency,
                    "deal_ids": deal_ids,
                    "experiment": experiment,
                    "from_": from_,
                    "include_avails": include_avails,
                    "include_bid_levels": include_bid_levels,
                    "include_deal_statistics": include_deal_statistics,
                    "include_errors": include_errors,
                    "include_formats": include_formats,
                    "include_no_bid_responses": include_no_bid_responses,
                    "include_response_times": include_response_times,
                    "include_sold_statistics": include_sold_statistics,
                    "include_stats_buyers": include_stats_buyers,
                    "include_sub_set_publishers": include_sub_set_publishers,
                    "include_user_statistics": include_user_statistics,
                    "inverse_ad_units": inverse_ad_units,
                    "livewrapped_deal_ids": livewrapped_deal_ids,
                    "master_publisher_id": master_publisher_id,
                    "publisher_ids": publisher_ids,
                    "query_hour_resolution": query_hour_resolution,
                    "reseller_ids": reseller_ids,
                    "seat_names": seat_names,
                    "site_ids": site_ids,
                    "time_zone": time_zone,
                    "to": to,
                },
                statistics_v2_create_params.StatisticsV2CreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StatsResponse,
        )


class StatisticsV2ResourceWithRawResponse:
    def __init__(self, statistics_v2: StatisticsV2Resource) -> None:
        self._statistics_v2 = statistics_v2

        self.create = to_raw_response_wrapper(
            statistics_v2.create,
        )


class AsyncStatisticsV2ResourceWithRawResponse:
    def __init__(self, statistics_v2: AsyncStatisticsV2Resource) -> None:
        self._statistics_v2 = statistics_v2

        self.create = async_to_raw_response_wrapper(
            statistics_v2.create,
        )


class StatisticsV2ResourceWithStreamingResponse:
    def __init__(self, statistics_v2: StatisticsV2Resource) -> None:
        self._statistics_v2 = statistics_v2

        self.create = to_streamed_response_wrapper(
            statistics_v2.create,
        )


class AsyncStatisticsV2ResourceWithStreamingResponse:
    def __init__(self, statistics_v2: AsyncStatisticsV2Resource) -> None:
        self._statistics_v2 = statistics_v2

        self.create = async_to_streamed_response_wrapper(
            statistics_v2.create,
        )
