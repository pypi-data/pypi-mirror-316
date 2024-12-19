#  See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.stats_inventory.buyer_minimal import BuyerMinimal

__all__ = ["BuyersResource", "AsyncBuyersResource"]


class BuyersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BuyersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return BuyersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BuyersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return BuyersResourceWithStreamingResponse(self)

    def retrieve(
        self,
        buyer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BuyerMinimal:
        """
        Retrieve extended information about a specific buyer.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not buyer_id:
            raise ValueError(f"Expected a non-empty value for `buyer_id` but received {buyer_id!r}")
        return self._get(
            f"/StatsInventory/buyer/{buyer_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuyerMinimal,
        )


class AsyncBuyersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBuyersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBuyersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBuyersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AsyncBuyersResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        buyer_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BuyerMinimal:
        """
        Retrieve extended information about a specific buyer.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not buyer_id:
            raise ValueError(f"Expected a non-empty value for `buyer_id` but received {buyer_id!r}")
        return await self._get(
            f"/StatsInventory/buyer/{buyer_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuyerMinimal,
        )


class BuyersResourceWithRawResponse:
    def __init__(self, buyers: BuyersResource) -> None:
        self._buyers = buyers

        self.retrieve = to_raw_response_wrapper(
            buyers.retrieve,
        )


class AsyncBuyersResourceWithRawResponse:
    def __init__(self, buyers: AsyncBuyersResource) -> None:
        self._buyers = buyers

        self.retrieve = async_to_raw_response_wrapper(
            buyers.retrieve,
        )


class BuyersResourceWithStreamingResponse:
    def __init__(self, buyers: BuyersResource) -> None:
        self._buyers = buyers

        self.retrieve = to_streamed_response_wrapper(
            buyers.retrieve,
        )


class AsyncBuyersResourceWithStreamingResponse:
    def __init__(self, buyers: AsyncBuyersResource) -> None:
        self._buyers = buyers

        self.retrieve = async_to_streamed_response_wrapper(
            buyers.retrieve,
        )
