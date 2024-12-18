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

from foundry._errors import PalantirRPCException
from foundry.v2.functions.models._parameter_id import ParameterId


class UnknownParameterParameters(TypedDict):
    """
    The provided parameters were not found. Please look at the `knownParameters` field
    to see which ones are available.
    """

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    unknownParameters: List[ParameterId]

    expectedParameters: List[ParameterId]


@dataclass
class UnknownParameter(PalantirRPCException):
    name: Literal["UnknownParameter"]
    parameters: UnknownParameterParameters
    error_instance_id: str


__all__ = ["UnknownParameter"]
