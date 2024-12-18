#  Copyright 2024 Palantir Technologies, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from __future__ import annotations

from typing import Any
from typing import Literal

from typing_extensions import NotRequired
from typing_extensions import TypedDict


class StringLengthConstraintDict(TypedDict):
    """
    The parameter value must have a length within the defined range.
    *This range is always inclusive.*
    """

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    lt: NotRequired[Any]
    """Less than"""

    lte: NotRequired[Any]
    """Less than or equal"""

    gt: NotRequired[Any]
    """Greater than"""

    gte: NotRequired[Any]
    """Greater than or equal"""

    type: Literal["stringLength"]
