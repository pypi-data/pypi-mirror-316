from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal, Any

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "StatsResponse",
    "Stat",
    "StatRequest",
    "StatResponse",
    "StatResponseAdBlockerRecoveredGrossRevenueInPublisherCurrency",
    "StatResponseAdBlockerRecoveredNetRevenueInPublisherCurrency",
    "StatResponseBidAmountNativeSold",
    "StatResponseBidAmountSold",
    "StatResponseBidAmountTotal",
    "StatResponseBidAmountVideoSold",
    "StatResponseBidLevelsInPublisherCurrency",
    "StatResponseBidLevelsInPublisherCurrencyBucket",
    "StatResponseGrossRevenue",
    "StatResponseIncrementalRevenue",
    "StatResponseNetRevenue",
    "StatResponseNetRevenueNative",
    "StatResponseNetRevenueVideo",
    "StatResponseResponseTimes",
    "StatResponseS2SAmountWon",
    "StatResponseSiteResponseTimes",
    "StatResponseSoldBidLevelsInPublisherCurrency",
    "StatResponseSoldBidLevelsInPublisherCurrencyBucket",
    "StatSoldDataStats",
    "StatSoldDataStatsAdvertisers",
    "StatSoldDataStatsDeals",
    "StatSoldDataStatsDealsAdvertiserStats",
    "StatUserDataItemCapStats",
    "StatUserDataItemCapStatsBidLevelsInPublisherCurrency",
    "StatUserDataItemCapStatsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataItemCapStatsSoldBidLevelsInPublisherCurrency",
    "StatUserDataItemCapStatsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStats",
    "StatUserDataStatsBrowserAndCapabilitiesRequests",
    "StatUserDataStatsBrowserAndCapabilitiesRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsBrowserAndCapabilitiesRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsBrowserAndCapabilitiesRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsBrowserAndCapabilitiesRequestsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsBrowserAndVersionRequests",
    "StatUserDataStatsBrowserAndVersionRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsBrowserAndVersionRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsBrowserAndVersionRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsBrowserAndVersionRequestsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsBrowserRequests",
    "StatUserDataStatsBrowserRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsBrowserRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsBrowserRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsBrowserRequestsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsCountryCodeRequests",
    "StatUserDataStatsCountryCodeRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsCountryCodeRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsCountryCodeRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsCountryCodeRequestsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsDeviceMakeRequests",
    "StatUserDataStatsDeviceMakeRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsDeviceMakeRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsDeviceMakeRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsDeviceMakeRequestsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsDeviceModelRequests",
    "StatUserDataStatsDeviceModelRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsDeviceModelRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsDeviceModelRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsDeviceModelRequestsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsDeviceTypeRequests",
    "StatUserDataStatsDeviceTypeRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsDeviceTypeRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsDeviceTypeRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsDeviceTypeRequestsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsOsAndVersionRequests",
    "StatUserDataStatsOsAndVersionRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsOsAndVersionRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsOsAndVersionRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsOsAndVersionRequestsSoldBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsOsRequests",
    "StatUserDataStatsOsRequestsBidLevelsInPublisherCurrency",
    "StatUserDataStatsOsRequestsBidLevelsInPublisherCurrencyBucket",
    "StatUserDataStatsOsRequestsSoldBidLevelsInPublisherCurrency",
    "StatUserDataStatsOsRequestsSoldBidLevelsInPublisherCurrencyBucket",
]


class StatRequest(BaseModel):
    ad_blocker_recovered_ad_unit_requests: Optional[int] = FieldInfo(
        alias="adBlockerRecoveredAdUnitRequests", default=None
    )

    ad_server_ad_unit_viewable_requests: Optional[int] = FieldInfo(alias="adServerAdUnitViewableRequests", default=None)

    ad_unit_ad_blocked_requests: Optional[int] = FieldInfo(alias="adUnitAdBlockedRequests", default=None)

    ad_unit_data_requests: Optional[int] = FieldInfo(alias="adUnitDataRequests", default=None)

    ad_unit_requests: Optional[int] = FieldInfo(alias="adUnitRequests", default=None)

    ad_unit_viewable_requests: Optional[int] = FieldInfo(alias="adUnitViewableRequests", default=None)

    analytics_only_chargeable_requests_by_hour: Optional[int] = FieldInfo(
        alias="analyticsOnlyChargeableRequestsByHour", default=None
    )

    buyer_requests: Optional[int] = FieldInfo(alias="buyerRequests", default=None)

    gdpr: Optional[int] = None

    gdpr_consent: Optional[int] = FieldInfo(alias="gdprConsent", default=None)

    gdpr_requests: Optional[int] = FieldInfo(alias="gdprRequests", default=None)

    reloads: Optional[int] = None

    user_matchable_requests: Optional[int] = FieldInfo(alias="userMatchableRequests", default=None)

    user_matched: Optional[int] = FieldInfo(alias="userMatched", default=None)

    wrapper_bidders_chargeable_requests_by_hour: Optional[int] = FieldInfo(
        alias="wrapperBiddersChargeableRequestsByHour", default=None
    )

    wrapper_no_bidders_chargeable_requests_by_hour: Optional[int] = FieldInfo(
        alias="wrapperNoBiddersChargeableRequestsByHour", default=None
    )


class StatResponseAdBlockerRecoveredGrossRevenueInPublisherCurrency(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseAdBlockerRecoveredNetRevenueInPublisherCurrency(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseBidAmountNativeSold(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseBidAmountSold(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseBidAmountTotal(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseBidAmountVideoSold(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatResponseBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatResponseBidLevelsInPublisherCurrencyBucket]] = None


class StatResponseGrossRevenue(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseIncrementalRevenue(BaseModel):
    gross_revenue: Optional[float] = FieldInfo(alias="grossRevenue", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None


class StatResponseNetRevenue(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseNetRevenueNative(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseNetRevenueVideo(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseResponseTimes(BaseModel):
    are_buckets: Optional[bool] = FieldInfo(alias="areBuckets", default=None)

    buckets: Optional[Dict[str, int]] = None

    bucket_size: Optional[int] = FieldInfo(alias="bucketSize", default=None)

    max_buckets: Optional[int] = FieldInfo(alias="maxBuckets", default=None)

    min_value: Optional[int] = FieldInfo(alias="minValue", default=None)


class StatResponseS2SAmountWon(BaseModel):
    amount_in_buyer_currency: Optional[float] = FieldInfo(alias="amountInBuyerCurrency", default=None)

    amount_in_publisher_currency: Optional[float] = FieldInfo(alias="amountInPublisherCurrency", default=None)


class StatResponseSiteResponseTimes(BaseModel):
    are_buckets: Optional[bool] = FieldInfo(alias="areBuckets", default=None)

    buckets: Optional[Dict[str, int]] = None

    bucket_size: Optional[int] = FieldInfo(alias="bucketSize", default=None)

    max_buckets: Optional[int] = FieldInfo(alias="maxBuckets", default=None)

    min_value: Optional[int] = FieldInfo(alias="minValue", default=None)


class StatResponseSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatResponseSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatResponseSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatResponse(BaseModel):
    ad_blocker_recovered_gross_revenue_in_publisher_currency: Optional[
        StatResponseAdBlockerRecoveredGrossRevenueInPublisherCurrency
    ] = FieldInfo(alias="adBlockerRecoveredGrossRevenueInPublisherCurrency", default=None)

    ad_blocker_recovered_net_revenue_in_publisher_currency: Optional[
        StatResponseAdBlockerRecoveredNetRevenueInPublisherCurrency
    ] = FieldInfo(alias="adBlockerRecoveredNetRevenueInPublisherCurrency", default=None)

    ad_blocker_recovered_sold_impressions: Optional[int] = FieldInfo(
        alias="adBlockerRecoveredSoldImpressions", default=None
    )

    ad_blocker_recovered_valid_bids: Optional[int] = FieldInfo(alias="adBlockerRecoveredValidBids", default=None)

    ad_render_fails: Optional[int] = FieldInfo(alias="adRenderFails", default=None)

    average_response_time: Optional[int] = FieldInfo(alias="averageResponseTime", default=None)

    bid_amount_native_sold: Optional[StatResponseBidAmountNativeSold] = FieldInfo(
        alias="bidAmountNativeSold", default=None
    )

    bid_amount_sold: Optional[StatResponseBidAmountSold] = FieldInfo(alias="bidAmountSold", default=None)

    bid_amount_total: Optional[StatResponseBidAmountTotal] = FieldInfo(alias="bidAmountTotal", default=None)

    bid_amount_video_sold: Optional[StatResponseBidAmountVideoSold] = FieldInfo(
        alias="bidAmountVideoSold", default=None
    )

    bid_levels_in_publisher_currency: Optional[StatResponseBidLevelsInPublisherCurrency] = FieldInfo(
        alias="bidLevelsInPublisherCurrency", default=None
    )

    chargeable_impressions: Optional[int] = FieldInfo(alias="chargeableImpressions", default=None)

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    error_responses: Optional[Dict[str, Optional[int]]] = FieldInfo(alias="errorResponses", default=None)

    format: Optional[str] = None

    gross_revenue: Optional[StatResponseGrossRevenue] = FieldInfo(alias="grossRevenue", default=None)

    incremental_revenue: Optional[StatResponseIncrementalRevenue] = FieldInfo(alias="incrementalRevenue", default=None)

    invalid_bids: Optional[int] = FieldInfo(alias="invalidBids", default=None)

    net_revenue: Optional[StatResponseNetRevenue] = FieldInfo(alias="netRevenue", default=None)

    net_revenue_native: Optional[StatResponseNetRevenueNative] = FieldInfo(alias="netRevenueNative", default=None)

    net_revenue_video: Optional[StatResponseNetRevenueVideo] = FieldInfo(alias="netRevenueVideo", default=None)

    no_bid_responses: Optional[Dict[str, Optional[int]]] = FieldInfo(alias="noBidResponses", default=None)

    no_bids: Optional[int] = FieldInfo(alias="noBids", default=None)

    passbacks: Optional[int] = None

    percentage_in_view: Optional[float] = FieldInfo(alias="percentageInView", default=None)

    requests_with_bid: Optional[int] = FieldInfo(alias="requestsWithBid", default=None)

    response_times: Optional[StatResponseResponseTimes] = FieldInfo(alias="responseTimes", default=None)

    s2_s_amount_won: Optional[StatResponseS2SAmountWon] = FieldInfo(alias="s2SAmountWon", default=None)

    seat: Optional[str] = None

    seat_full_name: Optional[str] = FieldInfo(alias="seatFullName", default=None)

    server_side_native_wins: Optional[int] = FieldInfo(alias="serverSideNativeWins", default=None)

    server_side_video_wins: Optional[int] = FieldInfo(alias="serverSideVideoWins", default=None)

    server_side_wins: Optional[int] = FieldInfo(alias="serverSideWins", default=None)

    site_response_times: Optional[Dict[str, StatResponseSiteResponseTimes]] = FieldInfo(
        alias="siteResponseTimes", default=None
    )

    sold_bid_levels_in_publisher_currency: Optional[StatResponseSoldBidLevelsInPublisherCurrency] = FieldInfo(
        alias="soldBidLevelsInPublisherCurrency", default=None
    )

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    sold_native_impressions: Optional[int] = FieldInfo(alias="soldNativeImpressions", default=None)

    sold_video_impressions: Optional[int] = FieldInfo(alias="soldVideoImpressions", default=None)

    timeouts: Optional[int] = None

    total_sold_impressions: Optional[int] = FieldInfo(alias="totalSoldImpressions", default=None)

    total_time_viewed: Optional[int] = FieldInfo(alias="totalTimeViewed", default=None)

    valid_bids: Optional[int] = FieldInfo(alias="validBids", default=None)

    views: Optional[int] = None


class StatSoldDataStatsAdvertisers(BaseModel):
    advertiser_name: Optional[str] = FieldInfo(alias="advertiserName", default=None)

    blocked_impressions: Optional[int] = FieldInfo(alias="blockedImpressions", default=None)

    blocked_net_revenue: Optional[float] = FieldInfo(alias="blockedNetRevenue", default=None)

    blocked_revenue: Optional[float] = FieldInfo(alias="blockedRevenue", default=None)

    gross_revenue: Optional[float] = FieldInfo(alias="grossRevenue", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)


class StatSoldDataStatsDealsAdvertiserStats(BaseModel):
    advertiser_name: Optional[str] = FieldInfo(alias="advertiserName", default=None)

    blocked_impressions: Optional[int] = FieldInfo(alias="blockedImpressions", default=None)

    blocked_net_revenue: Optional[float] = FieldInfo(alias="blockedNetRevenue", default=None)

    blocked_revenue: Optional[float] = FieldInfo(alias="blockedRevenue", default=None)

    gross_revenue: Optional[float] = FieldInfo(alias="grossRevenue", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)


class StatSoldDataStatsDeals(BaseModel):
    advertiser_stats: Optional[Dict[str, StatSoldDataStatsDealsAdvertiserStats]] = FieldInfo(
        alias="advertiserStats", default=None
    )

    blocked_impressions: Optional[int] = FieldInfo(alias="blockedImpressions", default=None)

    blocked_net_revenue: Optional[float] = FieldInfo(alias="blockedNetRevenue", default=None)

    blocked_revenue: Optional[float] = FieldInfo(alias="blockedRevenue", default=None)

    gross_revenue: Optional[float] = FieldInfo(alias="grossRevenue", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)


class StatSoldDataStats(BaseModel):
    advertisers: Optional[Dict[str, StatSoldDataStatsAdvertisers]] = None

    deals: Optional[Dict[str, StatSoldDataStatsDeals]] = None


class StatUserDataItemCapStatsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataItemCapStatsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataItemCapStatsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataItemCapStatsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataItemCapStatsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataItemCapStatsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataItemCapStats(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[StatUserDataItemCapStatsBidLevelsInPublisherCurrency] = FieldInfo(
        alias="bidLevelsInPublisherCurrency", default=None
    )

    browser_name: Optional[str] = FieldInfo(alias="browserName", default=None)

    cookies_supported: Optional[bool] = FieldInfo(alias="cookiesSupported", default=None)

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    responses: Optional[int] = None

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[StatUserDataItemCapStatsSoldBidLevelsInPublisherCurrency] = (
        FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)
    )

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)
    topics_support: Optional[Any] = FieldInfo(alias="topicsSupport", default=None)
    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsBrowserAndCapabilitiesRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsBrowserAndCapabilitiesRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsBrowserAndCapabilitiesRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsBrowserAndCapabilitiesRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsBrowserAndCapabilitiesRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsBrowserAndCapabilitiesRequestsSoldBidLevelsInPublisherCurrencyBucket]] = (
        None
    )


class StatUserDataStatsBrowserAndCapabilitiesRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsBrowserAndCapabilitiesRequestsBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="bidLevelsInPublisherCurrency", default=None)

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsBrowserAndCapabilitiesRequestsSoldBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsBrowserAndVersionRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsBrowserAndVersionRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsBrowserAndVersionRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsBrowserAndVersionRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsBrowserAndVersionRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsBrowserAndVersionRequestsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsBrowserAndVersionRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsBrowserAndVersionRequestsBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="bidLevelsInPublisherCurrency", default=None)

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsBrowserAndVersionRequestsSoldBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsBrowserRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsBrowserRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsBrowserRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsBrowserRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsBrowserRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsBrowserRequestsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsBrowserRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[StatUserDataStatsBrowserRequestsBidLevelsInPublisherCurrency] = (
        FieldInfo(alias="bidLevelsInPublisherCurrency", default=None)
    )

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsBrowserRequestsSoldBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsCountryCodeRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsCountryCodeRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsCountryCodeRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsCountryCodeRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsCountryCodeRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsCountryCodeRequestsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsCountryCodeRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[StatUserDataStatsCountryCodeRequestsBidLevelsInPublisherCurrency] = (
        FieldInfo(alias="bidLevelsInPublisherCurrency", default=None)
    )

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsCountryCodeRequestsSoldBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsDeviceMakeRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsDeviceMakeRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsDeviceMakeRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsDeviceMakeRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsDeviceMakeRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsDeviceMakeRequestsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsDeviceMakeRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[StatUserDataStatsDeviceMakeRequestsBidLevelsInPublisherCurrency] = (
        FieldInfo(alias="bidLevelsInPublisherCurrency", default=None)
    )

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsDeviceMakeRequestsSoldBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsDeviceModelRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsDeviceModelRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsDeviceModelRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsDeviceModelRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsDeviceModelRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsDeviceModelRequestsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsDeviceModelRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[StatUserDataStatsDeviceModelRequestsBidLevelsInPublisherCurrency] = (
        FieldInfo(alias="bidLevelsInPublisherCurrency", default=None)
    )

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsDeviceModelRequestsSoldBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsDeviceTypeRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsDeviceTypeRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsDeviceTypeRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsDeviceTypeRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsDeviceTypeRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsDeviceTypeRequestsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsDeviceTypeRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[StatUserDataStatsDeviceTypeRequestsBidLevelsInPublisherCurrency] = (
        FieldInfo(alias="bidLevelsInPublisherCurrency", default=None)
    )

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsDeviceTypeRequestsSoldBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsOsAndVersionRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsOsAndVersionRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsOsAndVersionRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsOsAndVersionRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsOsAndVersionRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsOsAndVersionRequestsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsOsAndVersionRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[StatUserDataStatsOsAndVersionRequestsBidLevelsInPublisherCurrency] = (
        FieldInfo(alias="bidLevelsInPublisherCurrency", default=None)
    )

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[
        StatUserDataStatsOsAndVersionRequestsSoldBidLevelsInPublisherCurrency
    ] = FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStatsOsRequestsBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsOsRequestsBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsOsRequestsBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsOsRequestsSoldBidLevelsInPublisherCurrencyBucket(BaseModel):
    count: Optional[int] = None

    extend: Optional[float] = None

    value: Optional[float] = None


class StatUserDataStatsOsRequestsSoldBidLevelsInPublisherCurrency(BaseModel):
    buckets: Optional[List[StatUserDataStatsOsRequestsSoldBidLevelsInPublisherCurrencyBucket]] = None


class StatUserDataStatsOsRequests(BaseModel):
    available_impressions: Optional[int] = FieldInfo(alias="availableImpressions", default=None)

    bid_levels_in_publisher_currency: Optional[StatUserDataStatsOsRequestsBidLevelsInPublisherCurrency] = FieldInfo(
        alias="bidLevelsInPublisherCurrency", default=None
    )

    ecpm_squared: Optional[float] = FieldInfo(alias="ecpmSquared", default=None)

    in_views: Optional[int] = FieldInfo(alias="inViews", default=None)

    net_revenue: Optional[float] = FieldInfo(alias="netRevenue", default=None)

    revenue: Optional[float] = None

    sold_bid_levels_in_publisher_currency: Optional[StatUserDataStatsOsRequestsSoldBidLevelsInPublisherCurrency] = (
        FieldInfo(alias="soldBidLevelsInPublisherCurrency", default=None)
    )

    sold_impressions: Optional[int] = FieldInfo(alias="soldImpressions", default=None)

    viewable_impressions: Optional[int] = FieldInfo(alias="viewableImpressions", default=None)


class StatUserDataStats(BaseModel):
    browser_and_capabilities_requests: Optional[Dict[str, StatUserDataStatsBrowserAndCapabilitiesRequests]] = FieldInfo(
        alias="browserAndCapabilitiesRequests", default=None
    )

    browser_and_capabilities_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(
        alias="browserAndCapabilitiesRequestsPercentage", default=None
    )

    browser_and_version_requests: Optional[Dict[str, StatUserDataStatsBrowserAndVersionRequests]] = FieldInfo(
        alias="browserAndVersionRequests", default=None
    )

    browser_and_version_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(
        alias="browserAndVersionRequestsPercentage", default=None
    )

    browser_requests: Optional[Dict[str, StatUserDataStatsBrowserRequests]] = FieldInfo(
        alias="browserRequests", default=None
    )

    browser_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(
        alias="browserRequestsPercentage", default=None
    )

    country_code_requests: Optional[Dict[str, StatUserDataStatsCountryCodeRequests]] = FieldInfo(
        alias="countryCodeRequests", default=None
    )

    country_code_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(
        alias="countryCodeRequestsPercentage", default=None
    )

    device_make_requests: Optional[Dict[str, StatUserDataStatsDeviceMakeRequests]] = FieldInfo(
        alias="deviceMakeRequests", default=None
    )

    device_make_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(
        alias="deviceMakeRequestsPercentage", default=None
    )

    device_model_requests: Optional[Dict[str, StatUserDataStatsDeviceModelRequests]] = FieldInfo(
        alias="deviceModelRequests", default=None
    )

    device_model_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(
        alias="deviceModelRequestsPercentage", default=None
    )

    device_type_requests: Optional[Dict[str, StatUserDataStatsDeviceTypeRequests]] = FieldInfo(
        alias="deviceTypeRequests", default=None
    )

    device_type_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(
        alias="deviceTypeRequestsPercentage", default=None
    )

    os_and_version_requests: Optional[Dict[str, StatUserDataStatsOsAndVersionRequests]] = FieldInfo(
        alias="osAndVersionRequests", default=None
    )

    os_and_version_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(
        alias="osAndVersionRequestsPercentage", default=None
    )

    os_requests: Optional[Dict[str, StatUserDataStatsOsRequests]] = FieldInfo(alias="osRequests", default=None)

    os_requests_percentage: Optional[Dict[str, Optional[float]]] = FieldInfo(alias="osRequestsPercentage", default=None)


class Stat(BaseModel):
    ad_unit_id: Optional[str] = FieldInfo(alias="adUnitId", default=None)

    advertiser_domain: Optional[str] = FieldInfo(alias="advertiserDomain", default=None)

    advertiser_name: Optional[str] = FieldInfo(alias="advertiserName", default=None)

    agency: Optional[str] = None

    buyer_id: Optional[str] = FieldInfo(alias="buyerId", default=None)

    cookies_supported: Optional[bool] = FieldInfo(alias="cookiesSupported", default=None)

    deal_id: Optional[str] = FieldInfo(alias="dealId", default=None)

    deal_name: Optional[str] = FieldInfo(alias="dealName", default=None)

    from_: Optional[datetime] = FieldInfo(alias="from", default=None)

    livewrapped_deal_id: Optional[str] = FieldInfo(alias="livewrappedDealId", default=None)

    publisher_id: Optional[str] = FieldInfo(alias="publisherId", default=None)

    request: Optional[StatRequest] = None

    reseller_id: Optional[str] = FieldInfo(alias="resellerId", default=None)

    response: Optional[StatResponse] = None

    seat_name: Optional[str] = FieldInfo(alias="seatName", default=None)

    site_id: Optional[str] = FieldInfo(alias="siteId", default=None)

    sold_data_stats: Optional[StatSoldDataStats] = FieldInfo(alias="soldDataStats", default=None)

    to: Optional[datetime] = None

    topics_support: Optional[Any] = FieldInfo(alias="topicsSupport", default=None)

    user_data_item_cap_stats: Optional[StatUserDataItemCapStats] = FieldInfo(alias="userDataItemCapStats", default=None)

    user_data_stats: Optional[StatUserDataStats] = FieldInfo(alias="userDataStats", default=None)


class StatsResponse(BaseModel):
    stats: Optional[List[Stat]] = None
