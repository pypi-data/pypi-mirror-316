#  See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal, Any

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["PublisherMinimal", "BuyerMapping"]


class BuyerMapping(BaseModel):
    id: Optional[int] = None

    alias: Optional[str] = None

    bid_cpm_adjustment_code: Optional[str] = FieldInfo(alias="bidCpmAdjustmentCode", default=None)

    buyer_id: Optional[str] = FieldInfo(alias="buyerId", default=None)

    commission: Optional[float] = None

    enable_auction: Optional[bool] = FieldInfo(alias="enableAuction", default=None)

    exclude_from_total_revenue: Optional[bool] = FieldInfo(alias="excludeFromTotalRevenue", default=None)

    is_visible: Optional[bool] = FieldInfo(alias="isVisible", default=None)

    net_revenue_percentage: Optional[float] = FieldInfo(alias="netRevenuePercentage", default=None)

    use_commission_on_net_bids: Optional[bool] = FieldInfo(alias="useCommissionOnNetBids", default=None)


class PublisherMinimal(BaseModel):
    id: Optional[str] = None

    adserver_integration: Optional[Any] = FieldInfo(alias="adserverIntegration", default=None)

    auction_enabled: Optional[bool] = FieldInfo(alias="auctionEnabled", default=None)

    buyer_mappings: Optional[List[BuyerMapping]] = FieldInfo(alias="buyerMappings", default=None)

    cmp_api: Optional[str] = FieldInfo(alias="cmpApi", default=None)

    culture: Optional[str] = None

    currency: Optional[str] = None

    domain: Optional[str] = None

    enable_floor_price_optimization: Optional[bool] = FieldInfo(alias="enableFloorPriceOptimization", default=None)

    is_active: Optional[bool] = FieldInfo(alias="isActive", default=None)

    name: Optional[str] = None

    pb_js_time_out: Optional[int] = FieldInfo(alias="pbJsTimeOut", default=None)

    time_zone: Optional[str] = FieldInfo(alias="timeZone", default=None)
