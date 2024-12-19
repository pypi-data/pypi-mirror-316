#  See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from livewrapped_sdk import LivewrappedSDK, AsyncLivewrappedSDK
from livewrapped_sdk.types import StatsResponse
from livewrapped_sdk._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStatisticsV2:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: LivewrappedSDK) -> None:
        statistics_v2 = client.statistics_v2.create()
        assert_matches_type(StatsResponse, statistics_v2, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: LivewrappedSDK) -> None:
        statistics_v2 = client.statistics_v2.create(
            ad_unit_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            advertiser_domains=["string"],
            advertiser_names=["string"],
            agencies=["string"],
            aggregate_ad_units=True,
            aggregate_advertiser_domains=True,
            aggregate_advertiser_names=True,
            aggregate_agencies=True,
            aggregate_browser=True,
            aggregate_buyers=True,
            aggregate_cookie_support=True,
            aggregate_deals=True,
            aggregate_livewrapped_deals=True,
            aggregate_publishers=True,
            aggregate_resellers=True,
            aggregate_seats=True,
            aggregate_sites=True,
            aggregate_time=True,
            aggregate_topics=True,
            aggregation_level=None,
            avoid_client_aggregation=True,
            buyer_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            currency="currency",
            deal_ids=["string"],
            experiment=0,
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_avails=True,
            include_bid_levels=True,
            include_deal_statistics=True,
            include_errors=True,
            include_formats=True,
            include_no_bid_responses=True,
            include_response_times=True,
            include_sold_statistics=True,
            include_stats_buyers=True,
            include_sub_set_publishers=True,
            include_user_statistics=None,
            inverse_ad_units=True,
            livewrapped_deal_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            master_publisher_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            publisher_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            query_hour_resolution=True,
            reseller_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            seat_names=["string"],
            site_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            time_zone="timeZone",
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(StatsResponse, statistics_v2, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: LivewrappedSDK) -> None:
        response = client.statistics_v2.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        statistics_v2 = response.parse()
        assert_matches_type(StatsResponse, statistics_v2, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: LivewrappedSDK) -> None:
        with client.statistics_v2.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            statistics_v2 = response.parse()
            assert_matches_type(StatsResponse, statistics_v2, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStatisticsV2:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncLivewrappedSDK) -> None:
        statistics_v2 = await async_client.statistics_v2.create()
        assert_matches_type(StatsResponse, statistics_v2, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLivewrappedSDK) -> None:
        statistics_v2 = await async_client.statistics_v2.create(
            ad_unit_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            advertiser_domains=["string"],
            advertiser_names=["string"],
            agencies=["string"],
            aggregate_ad_units=True,
            aggregate_advertiser_domains=True,
            aggregate_advertiser_names=True,
            aggregate_agencies=True,
            aggregate_browser=True,
            aggregate_buyers=True,
            aggregate_cookie_support=True,
            aggregate_deals=True,
            aggregate_livewrapped_deals=True,
            aggregate_publishers=True,
            aggregate_resellers=True,
            aggregate_seats=True,
            aggregate_sites=True,
            aggregate_time=True,
            aggregate_topics=True,
            aggregation_level=None,
            avoid_client_aggregation=True,
            buyer_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            currency="currency",
            deal_ids=["string"],
            experiment=0,
            from_=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_avails=True,
            include_bid_levels=True,
            include_deal_statistics=True,
            include_errors=True,
            include_formats=True,
            include_no_bid_responses=True,
            include_response_times=True,
            include_sold_statistics=True,
            include_stats_buyers=True,
            include_sub_set_publishers=True,
            include_user_statistics=None,
            inverse_ad_units=True,
            livewrapped_deal_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            master_publisher_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            publisher_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            query_hour_resolution=True,
            reseller_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            seat_names=["string"],
            site_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            time_zone="timeZone",
            to=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(StatsResponse, statistics_v2, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLivewrappedSDK) -> None:
        response = await async_client.statistics_v2.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        statistics_v2 = await response.parse()
        assert_matches_type(StatsResponse, statistics_v2, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLivewrappedSDK) -> None:
        async with async_client.statistics_v2.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            statistics_v2 = await response.parse()
            assert_matches_type(StatsResponse, statistics_v2, path=["response"])

        assert cast(Any, response.is_closed) is True
