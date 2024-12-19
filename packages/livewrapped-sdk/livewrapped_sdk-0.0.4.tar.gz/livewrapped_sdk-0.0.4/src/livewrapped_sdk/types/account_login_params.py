#  See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AccountLoginParams"]


class AccountLoginParams(TypedDict, total=False):
    email: Required[str]

    password: Required[str]
