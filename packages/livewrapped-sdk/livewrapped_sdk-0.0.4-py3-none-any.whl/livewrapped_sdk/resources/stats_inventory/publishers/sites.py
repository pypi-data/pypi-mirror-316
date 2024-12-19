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
from ....types.stats_inventory.publishers.site_list_response import SiteListResponse
from ....types.stats_inventory.publishers.site_retrieve_response import SiteRetrieveResponse

__all__ = ["SitesResource", "AsyncSitesResource"]


class SitesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SitesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SitesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SitesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return SitesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        publisher_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SiteRetrieveResponse:
        """
        Retrieve all sites connected to a publisher.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not publisher_id:
            raise ValueError(f"Expected a non-empty value for `publisher_id` but received {publisher_id!r}")
        return self._get(
            f"/StatsInventory/publisher/{publisher_id}/site",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SiteRetrieveResponse,
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
    ) -> SiteListResponse:
        """Retrieve all sites the logged in user has access to.

        Information about each site
        is abbreviated.
        """
        return self._get(
            "/StatsInventory/publisher/site",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SiteListResponse,
        )


class AsyncSitesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSitesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSitesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSitesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AsyncSitesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        publisher_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SiteRetrieveResponse:
        """
        Retrieve all sites connected to a publisher.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not publisher_id:
            raise ValueError(f"Expected a non-empty value for `publisher_id` but received {publisher_id!r}")
        return await self._get(
            f"/StatsInventory/publisher/{publisher_id}/site",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SiteRetrieveResponse,
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
    ) -> SiteListResponse:
        """Retrieve all sites the logged in user has access to.

        Information about each site
        is abbreviated.
        """
        return await self._get(
            "/StatsInventory/publisher/site",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SiteListResponse,
        )


class SitesResourceWithRawResponse:
    def __init__(self, sites: SitesResource) -> None:
        self._sites = sites

        self.retrieve = to_raw_response_wrapper(
            sites.retrieve,
        )
        self.list = to_raw_response_wrapper(
            sites.list,
        )


class AsyncSitesResourceWithRawResponse:
    def __init__(self, sites: AsyncSitesResource) -> None:
        self._sites = sites

        self.retrieve = async_to_raw_response_wrapper(
            sites.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            sites.list,
        )


class SitesResourceWithStreamingResponse:
    def __init__(self, sites: SitesResource) -> None:
        self._sites = sites

        self.retrieve = to_streamed_response_wrapper(
            sites.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            sites.list,
        )


class AsyncSitesResourceWithStreamingResponse:
    def __init__(self, sites: AsyncSitesResource) -> None:
        self._sites = sites

        self.retrieve = async_to_streamed_response_wrapper(
            sites.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            sites.list,
        )
