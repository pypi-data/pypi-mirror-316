#  See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .site_minimal import SiteMinimal

__all__ = ["SiteRetrieveResponse"]

SiteRetrieveResponse: TypeAlias = List[SiteMinimal]
