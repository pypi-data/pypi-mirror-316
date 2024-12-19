#  See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["StatisticsV2CreateParams"]


class StatisticsV2CreateParams(TypedDict, total=False):
    ad_unit_ids: Annotated[Optional[List[str]], PropertyInfo(alias="adUnitIds")]

    advertiser_domains: Annotated[Optional[List[str]], PropertyInfo(alias="advertiserDomains")]
    """Filter sold statistics on advertiser domain (and name if available)."""

    advertiser_names: Annotated[Optional[List[str]], PropertyInfo(alias="advertiserNames")]

    agencies: Optional[List[str]]

    aggregate_ad_units: Annotated[bool, PropertyInfo(alias="aggregateAdUnits")]

    aggregate_advertiser_domains: Annotated[bool, PropertyInfo(alias="aggregateAdvertiserDomains")]

    aggregate_advertiser_names: Annotated[bool, PropertyInfo(alias="aggregateAdvertiserNames")]

    aggregate_agencies: Annotated[bool, PropertyInfo(alias="aggregateAgencies")]

    aggregate_browser: Annotated[bool, PropertyInfo(alias="aggregateBrowser")]
    """When retrieving browser caps, aggregate browser."""

    aggregate_buyers: Annotated[bool, PropertyInfo(alias="aggregateBuyers")]

    aggregate_cookie_support: Annotated[bool, PropertyInfo(alias="aggregateCookieSupport")]
    """When retrieving browser caps, aggregate cookie support."""

    aggregate_deals: Annotated[bool, PropertyInfo(alias="aggregateDeals")]

    aggregate_livewrapped_deals: Annotated[bool, PropertyInfo(alias="aggregateLivewrappedDeals")]

    aggregate_publishers: Annotated[bool, PropertyInfo(alias="aggregatePublishers")]

    aggregate_resellers: Annotated[bool, PropertyInfo(alias="aggregateResellers")]

    aggregate_seats: Annotated[bool, PropertyInfo(alias="aggregateSeats")]

    aggregate_sites: Annotated[bool, PropertyInfo(alias="aggregateSites")]

    aggregate_time: Annotated[bool, PropertyInfo(alias="aggregateTime")]

    aggregate_topics: Annotated[bool, PropertyInfo(alias="aggregateTopics")]
    """When retrieving browser caps, aggregate Topics information."""

    aggregation_level: Annotated[Literal, PropertyInfo(alias="aggregationLevel")]

    avoid_client_aggregation: Annotated[bool, PropertyInfo(alias="avoidClientAggregation")]
    """
    Do not run operations that require client aggregation and do only database
    aggregations.
    """

    buyer_ids: Annotated[Optional[List[str]], PropertyInfo(alias="buyerIds")]

    currency: Optional[str]

    deal_ids: Annotated[Optional[List[str]], PropertyInfo(alias="dealIds")]
    """List of deal IDs sent from SSPs."""

    experiment: int
    """Read from an experiment database by index. Ignore to read from main database,"""

    from_: Annotated[Union[str, datetime], PropertyInfo(alias="from", format="iso8601")]
    """The From date is inclusive."""

    include_avails: Annotated[bool, PropertyInfo(alias="includeAvails")]

    include_bid_levels: Annotated[bool, PropertyInfo(alias="includeBidLevels")]
    """Will force client aggregation which is resource heavy. Only use if required."""

    include_deal_statistics: Annotated[bool, PropertyInfo(alias="includeDealStatistics")]
    """Include Deal statistics if this is collected.

    This can not be combined with other includes.
    """

    include_errors: Annotated[bool, PropertyInfo(alias="includeErrors")]
    """Include rendering errors.

    Will force client aggregation which is resource heavy. Only use if required.
    """

    include_formats: Annotated[bool, PropertyInfo(alias="includeFormats")]

    include_no_bid_responses: Annotated[bool, PropertyInfo(alias="includeNoBidResponses")]
    """Will force client aggregation which is resource heavy. Only use if required."""

    include_response_times: Annotated[bool, PropertyInfo(alias="includeResponseTimes")]
    """Will force client aggregation which is resource heavy. Only use if required."""

    include_sold_statistics: Annotated[bool, PropertyInfo(alias="includeSoldStatistics")]
    """
    Include Advertiser statistics and collected deals statistics if those are
    collected. This can not be combined with other includes.
    """

    include_stats_buyers: Annotated[bool, PropertyInfo(alias="includeStatsBuyers")]
    """
    Include imported statistics not from the Header Bidding auction such as ad
    server statistics.
    """

    include_sub_set_publishers: Annotated[bool, PropertyInfo(alias="includeSubSetPublishers")]
    """Include publishers not owned by the account but with statistics access."""

    include_user_statistics: Annotated[Literal, PropertyInfo(alias="includeUserStatistics")]

    inverse_ad_units: Annotated[bool, PropertyInfo(alias="inverseAdUnits")]

    livewrapped_deal_ids: Annotated[Optional[List[str]], PropertyInfo(alias="livewrappedDealIds")]
    """List of Livewrapped-defined IDs of deals created in Livewrapped's console/API."""

    master_publisher_id: Annotated[Optional[str], PropertyInfo(alias="masterPublisherId")]

    publisher_ids: Annotated[Optional[List[str]], PropertyInfo(alias="publisherIds")]

    query_hour_resolution: Annotated[bool, PropertyInfo(alias="queryHourResolution")]
    """
    By default, From and To will be adjusted to include full days from midnight to
    midnight. If AggregationLevel is Hour, setting this to true will allow From and
    To to be specified on hour resolution.
    """

    reseller_ids: Annotated[Optional[List[str]], PropertyInfo(alias="resellerIds")]

    seat_names: Annotated[Optional[List[str]], PropertyInfo(alias="seatNames")]

    site_ids: Annotated[Optional[List[str]], PropertyInfo(alias="siteIds")]

    time_zone: Annotated[Optional[str], PropertyInfo(alias="timeZone")]

    to: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """The To date is inclusive."""
