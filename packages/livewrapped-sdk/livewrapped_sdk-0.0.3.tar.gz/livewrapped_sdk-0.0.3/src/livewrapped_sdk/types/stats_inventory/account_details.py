#  See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .buyer_minimal import BuyerMinimal
from .publisher_minimal import PublisherMinimal

__all__ = ["AccountDetails", "MasterPublisher"]


class MasterPublisher(BaseModel):
    id: Optional[str] = None

    buyer_subset_buyer_ids: Optional[List[str]] = FieldInfo(alias="buyerSubsetBuyerIds", default=None)

    buyer_subset_publishers: Optional[List[PublisherMinimal]] = FieldInfo(alias="buyerSubsetPublishers", default=None)

    culture: Optional[str] = None

    currency: Optional[str] = None

    domain: Optional[str] = None

    is_active: Optional[bool] = FieldInfo(alias="isActive", default=None)

    name: Optional[str] = None

    publishers: Optional[List[PublisherMinimal]] = None

    time_zone: Optional[str] = FieldInfo(alias="timeZone", default=None)

    type: Optional[int] = None


class AccountDetails(BaseModel):
    buyers: Optional[List[BuyerMinimal]] = None

    email: Optional[str] = None

    master_publisher: Optional[MasterPublisher] = FieldInfo(alias="masterPublisher", default=None)

    name: Optional[str] = None

    publisher: Optional[PublisherMinimal] = None
