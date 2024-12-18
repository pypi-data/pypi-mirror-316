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

from dataclasses import dataclass
from typing import List
from typing import Literal

import pydantic
from typing_extensions import TypedDict

from foundry._core.utils import RID
from foundry._errors import PalantirRPCException


class BuildInputsPermissionDeniedParameters(TypedDict):
    """The provided token does not have permission to use the given resources as inputs to the build."""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    resourceRids: List[RID]


@dataclass
class BuildInputsPermissionDenied(PalantirRPCException):
    name: Literal["BuildInputsPermissionDenied"]
    parameters: BuildInputsPermissionDeniedParameters
    error_instance_id: str


__all__ = ["BuildInputsPermissionDenied"]
