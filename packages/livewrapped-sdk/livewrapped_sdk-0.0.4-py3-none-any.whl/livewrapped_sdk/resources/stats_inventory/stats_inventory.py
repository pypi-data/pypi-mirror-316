#  See CONTRIBUTING.md for details.

from __future__ import annotations

from .sites import (
    SitesResource,
    AsyncSitesResource,
    SitesResourceWithRawResponse,
    AsyncSitesResourceWithRawResponse,
    SitesResourceWithStreamingResponse,
    AsyncSitesResourceWithStreamingResponse,
)
from .buyers import (
    BuyersResource,
    AsyncBuyersResource,
    BuyersResourceWithRawResponse,
    AsyncBuyersResourceWithRawResponse,
    BuyersResourceWithStreamingResponse,
    AsyncBuyersResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .publishers import (
    PublishersResource,
    AsyncPublishersResource,
    PublishersResourceWithRawResponse,
    AsyncPublishersResourceWithRawResponse,
    PublishersResourceWithStreamingResponse,
    AsyncPublishersResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from .sites.sites import SitesResource, AsyncSitesResource
from .account_details import (
    AccountDetailsResource,
    AsyncAccountDetailsResource,
    AccountDetailsResourceWithRawResponse,
    AsyncAccountDetailsResourceWithRawResponse,
    AccountDetailsResourceWithStreamingResponse,
    AsyncAccountDetailsResourceWithStreamingResponse,
)
from .publishers.publishers import PublishersResource, AsyncPublishersResource

__all__ = ["StatsInventoryResource", "AsyncStatsInventoryResource"]


class StatsInventoryResource(SyncAPIResource):
    @cached_property
    def account_details(self) -> AccountDetailsResource:
        return AccountDetailsResource(self._client)

    @cached_property
    def publishers(self) -> PublishersResource:
        return PublishersResource(self._client)

    @cached_property
    def buyers(self) -> BuyersResource:
        return BuyersResource(self._client)

    @cached_property
    def sites(self) -> SitesResource:
        return SitesResource(self._client)

    @cached_property
    def with_raw_response(self) -> StatsInventoryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return StatsInventoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StatsInventoryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return StatsInventoryResourceWithStreamingResponse(self)


class AsyncStatsInventoryResource(AsyncAPIResource):
    @cached_property
    def account_details(self) -> AsyncAccountDetailsResource:
        return AsyncAccountDetailsResource(self._client)

    @cached_property
    def publishers(self) -> AsyncPublishersResource:
        return AsyncPublishersResource(self._client)

    @cached_property
    def buyers(self) -> AsyncBuyersResource:
        return AsyncBuyersResource(self._client)

    @cached_property
    def sites(self) -> AsyncSitesResource:
        return AsyncSitesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncStatsInventoryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncStatsInventoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStatsInventoryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/eivl/livewrapped-sdk-python#with_streaming_response
        """
        return AsyncStatsInventoryResourceWithStreamingResponse(self)


class StatsInventoryResourceWithRawResponse:
    def __init__(self, stats_inventory: StatsInventoryResource) -> None:
        self._stats_inventory = stats_inventory

    @cached_property
    def account_details(self) -> AccountDetailsResourceWithRawResponse:
        return AccountDetailsResourceWithRawResponse(self._stats_inventory.account_details)

    @cached_property
    def publishers(self) -> PublishersResourceWithRawResponse:
        return PublishersResourceWithRawResponse(self._stats_inventory.publishers)

    @cached_property
    def buyers(self) -> BuyersResourceWithRawResponse:
        return BuyersResourceWithRawResponse(self._stats_inventory.buyers)

    @cached_property
    def sites(self) -> SitesResourceWithRawResponse:
        return SitesResourceWithRawResponse(self._stats_inventory.sites)


class AsyncStatsInventoryResourceWithRawResponse:
    def __init__(self, stats_inventory: AsyncStatsInventoryResource) -> None:
        self._stats_inventory = stats_inventory

    @cached_property
    def account_details(self) -> AsyncAccountDetailsResourceWithRawResponse:
        return AsyncAccountDetailsResourceWithRawResponse(self._stats_inventory.account_details)

    @cached_property
    def publishers(self) -> AsyncPublishersResourceWithRawResponse:
        return AsyncPublishersResourceWithRawResponse(self._stats_inventory.publishers)

    @cached_property
    def buyers(self) -> AsyncBuyersResourceWithRawResponse:
        return AsyncBuyersResourceWithRawResponse(self._stats_inventory.buyers)

    @cached_property
    def sites(self) -> AsyncSitesResourceWithRawResponse:
        return AsyncSitesResourceWithRawResponse(self._stats_inventory.sites)


class StatsInventoryResourceWithStreamingResponse:
    def __init__(self, stats_inventory: StatsInventoryResource) -> None:
        self._stats_inventory = stats_inventory

    @cached_property
    def account_details(self) -> AccountDetailsResourceWithStreamingResponse:
        return AccountDetailsResourceWithStreamingResponse(self._stats_inventory.account_details)

    @cached_property
    def publishers(self) -> PublishersResourceWithStreamingResponse:
        return PublishersResourceWithStreamingResponse(self._stats_inventory.publishers)

    @cached_property
    def buyers(self) -> BuyersResourceWithStreamingResponse:
        return BuyersResourceWithStreamingResponse(self._stats_inventory.buyers)

    @cached_property
    def sites(self) -> SitesResourceWithStreamingResponse:
        return SitesResourceWithStreamingResponse(self._stats_inventory.sites)


class AsyncStatsInventoryResourceWithStreamingResponse:
    def __init__(self, stats_inventory: AsyncStatsInventoryResource) -> None:
        self._stats_inventory = stats_inventory

    @cached_property
    def account_details(self) -> AsyncAccountDetailsResourceWithStreamingResponse:
        return AsyncAccountDetailsResourceWithStreamingResponse(self._stats_inventory.account_details)

    @cached_property
    def publishers(self) -> AsyncPublishersResourceWithStreamingResponse:
        return AsyncPublishersResourceWithStreamingResponse(self._stats_inventory.publishers)

    @cached_property
    def buyers(self) -> AsyncBuyersResourceWithStreamingResponse:
        return AsyncBuyersResourceWithStreamingResponse(self._stats_inventory.buyers)

    @cached_property
    def sites(self) -> AsyncSitesResourceWithStreamingResponse:
        return AsyncSitesResourceWithStreamingResponse(self._stats_inventory.sites)
