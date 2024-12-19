#  See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .ad_unit_minimal import AdUnitMinimal

__all__ = ["AdUnitListResponse"]

AdUnitListResponse: TypeAlias = List[AdUnitMinimal]
