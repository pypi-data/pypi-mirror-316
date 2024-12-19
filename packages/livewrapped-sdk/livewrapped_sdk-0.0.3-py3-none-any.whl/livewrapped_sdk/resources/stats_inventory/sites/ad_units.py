#  See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.stats_inventory.sites.ad_unit_list_response import AdUnitListResponse
from ....types.stats_inventory.sites.ad_unit_retrieve_response import AdUnitRetrieveResponse

__all__ = ["AdUnitsResource", "AsyncAdUnitsResource"]


class AdUnitsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AdUnitsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AdUnitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AdUnitsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AdUnitsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        site_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdUnitRetrieveResponse:
        """
        Retrieve all ad units connected to a specific site.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not site_id:
            raise ValueError(f"Expected a non-empty value for `site_id` but received {site_id!r}")
        return self._get(
            f"/StatsInventory/site/{site_id}/adunit",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdUnitRetrieveResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdUnitListResponse:
        """Retrieve all ad units the logged in user has access to."""
        return self._get(
            "/StatsInventory/site/adunit",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdUnitListResponse,
        )


class AsyncAdUnitsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAdUnitsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAdUnitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAdUnitsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AsyncAdUnitsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        site_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdUnitRetrieveResponse:
        """
        Retrieve all ad units connected to a specific site.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not site_id:
            raise ValueError(f"Expected a non-empty value for `site_id` but received {site_id!r}")
        return await self._get(
            f"/StatsInventory/site/{site_id}/adunit",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdUnitRetrieveResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdUnitListResponse:
        """Retrieve all ad units the logged in user has access to."""
        return await self._get(
            "/StatsInventory/site/adunit",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdUnitListResponse,
        )


class AdUnitsResourceWithRawResponse:
    def __init__(self, ad_units: AdUnitsResource) -> None:
        self._ad_units = ad_units

        self.retrieve = to_raw_response_wrapper(
            ad_units.retrieve,
        )
        self.list = to_raw_response_wrapper(
            ad_units.list,
        )


class AsyncAdUnitsResourceWithRawResponse:
    def __init__(self, ad_units: AsyncAdUnitsResource) -> None:
        self._ad_units = ad_units

        self.retrieve = async_to_raw_response_wrapper(
            ad_units.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            ad_units.list,
        )


class AdUnitsResourceWithStreamingResponse:
    def __init__(self, ad_units: AdUnitsResource) -> None:
        self._ad_units = ad_units

        self.retrieve = to_streamed_response_wrapper(
            ad_units.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            ad_units.list,
        )


class AsyncAdUnitsResourceWithStreamingResponse:
    def __init__(self, ad_units: AsyncAdUnitsResource) -> None:
        self._ad_units = ad_units

        self.retrieve = async_to_streamed_response_wrapper(
            ad_units.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            ad_units.list,
        )
