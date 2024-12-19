#  See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .sites import (
    SitesResource,
    AsyncSitesResource,
    SitesResourceWithRawResponse,
    AsyncSitesResourceWithRawResponse,
    SitesResourceWithStreamingResponse,
    AsyncSitesResourceWithStreamingResponse,
)
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
from ....types.stats_inventory.publisher_minimal import PublisherMinimal

__all__ = ["PublishersResource", "AsyncPublishersResource"]


class PublishersResource(SyncAPIResource):
    @cached_property
    def sites(self) -> SitesResource:
        return SitesResource(self._client)

    @cached_property
    def with_raw_response(self) -> PublishersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PublishersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PublishersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return PublishersResourceWithStreamingResponse(self)

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
    ) -> PublisherMinimal:
        """
        Retrieve extended information about a specific publisher.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not publisher_id:
            raise ValueError(f"Expected a non-empty value for `publisher_id` but received {publisher_id!r}")
        return self._get(
            f"/StatsInventory/publisher/{publisher_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PublisherMinimal,
        )


class AsyncPublishersResource(AsyncAPIResource):
    @cached_property
    def sites(self) -> AsyncSitesResource:
        return AsyncSitesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPublishersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPublishersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPublishersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AsyncPublishersResourceWithStreamingResponse(self)

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
    ) -> PublisherMinimal:
        """
        Retrieve extended information about a specific publisher.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not publisher_id:
            raise ValueError(f"Expected a non-empty value for `publisher_id` but received {publisher_id!r}")
        return await self._get(
            f"/StatsInventory/publisher/{publisher_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PublisherMinimal,
        )


class PublishersResourceWithRawResponse:
    def __init__(self, publishers: PublishersResource) -> None:
        self._publishers = publishers

        self.retrieve = to_raw_response_wrapper(
            publishers.retrieve,
        )

    @cached_property
    def sites(self) -> SitesResourceWithRawResponse:
        return SitesResourceWithRawResponse(self._publishers.sites)


class AsyncPublishersResourceWithRawResponse:
    def __init__(self, publishers: AsyncPublishersResource) -> None:
        self._publishers = publishers

        self.retrieve = async_to_raw_response_wrapper(
            publishers.retrieve,
        )

    @cached_property
    def sites(self) -> AsyncSitesResourceWithRawResponse:
        return AsyncSitesResourceWithRawResponse(self._publishers.sites)


class PublishersResourceWithStreamingResponse:
    def __init__(self, publishers: PublishersResource) -> None:
        self._publishers = publishers

        self.retrieve = to_streamed_response_wrapper(
            publishers.retrieve,
        )

    @cached_property
    def sites(self) -> SitesResourceWithStreamingResponse:
        return SitesResourceWithStreamingResponse(self._publishers.sites)


class AsyncPublishersResourceWithStreamingResponse:
    def __init__(self, publishers: AsyncPublishersResource) -> None:
        self._publishers = publishers

        self.retrieve = async_to_streamed_response_wrapper(
            publishers.retrieve,
        )

    @cached_property
    def sites(self) -> AsyncSitesResourceWithStreamingResponse:
        return AsyncSitesResourceWithStreamingResponse(self._publishers.sites)
