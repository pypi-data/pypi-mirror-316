#  See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SiteMinimal"]


class SiteMinimal(BaseModel):
    id: Optional[str] = None

    cmp_enabled: Optional[bool] = FieldInfo(alias="cmpEnabled", default=None)

    is_active: Optional[bool] = FieldInfo(alias="isActive", default=None)

    name: Optional[str] = None
