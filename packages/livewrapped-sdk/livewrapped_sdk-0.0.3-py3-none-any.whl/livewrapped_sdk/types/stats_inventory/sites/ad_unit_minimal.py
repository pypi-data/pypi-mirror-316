#  See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal, Any

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["AdUnitMinimal", "AlternativeFormat", "DefaultFormat"]


class AlternativeFormat(BaseModel):
    height: Optional[int] = None

    width: Optional[int] = None


class DefaultFormat(BaseModel):
    height: Optional[int] = None

    width: Optional[int] = None


class AdUnitMinimal(BaseModel):
    id: Optional[str] = None

    ad_unit_alternate_names: Optional[List[str]] = FieldInfo(alias="adUnitAlternateNames", default=None)

    alternative_formats: Optional[List[AlternativeFormat]] = FieldInfo(alias="alternativeFormats", default=None)

    default_format: Optional[DefaultFormat] = FieldInfo(alias="defaultFormat", default=None)

    disable_lazy_load: Optional[bool] = FieldInfo(alias="disableLazyLoad", default=None)

    enable_floor_price_optimization: Optional[bool] = FieldInfo(alias="enableFloorPriceOptimization", default=None)

    is_active: Optional[bool] = FieldInfo(alias="isActive", default=None)

    name: Optional[str] = None

    special_format_type: Optional[Any] = FieldInfo(alias="specialFormatType", default=None)

    traffic_type: Optional[int] = FieldInfo(alias="trafficType", default=None)
