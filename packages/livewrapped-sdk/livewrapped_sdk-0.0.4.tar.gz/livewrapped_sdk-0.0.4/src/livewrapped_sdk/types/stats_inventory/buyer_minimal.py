#  See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal, Any

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["BuyerMinimal"]


class BuyerMinimal(BaseModel):
    id: Optional[str] = None

    alias: Optional[str] = None

    external: Optional[bool] = None

    external_id: Optional[str] = FieldInfo(alias="externalId", default=None)

    is_active: Optional[bool] = FieldInfo(alias="isActive", default=None)

    name: Optional[str] = None

    traffic_type: Optional[int] = FieldInfo(alias="trafficType", default=None)

    type: Optional[Any] = None
