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
from typing import Literal

import pydantic
from typing_extensions import NotRequired
from typing_extensions import TypedDict

from foundry._errors import PalantirRPCException
from foundry.v1.ontologies.models._apply_action_request_options import (
    ApplyActionRequestOptions,
)  # NOQA


class InvalidApplyActionOptionCombinationParameters(TypedDict):
    """The given options are individually valid but cannot be used in the given combination."""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    invalidCombination: NotRequired[ApplyActionRequestOptions]


@dataclass
class InvalidApplyActionOptionCombination(PalantirRPCException):
    name: Literal["InvalidApplyActionOptionCombination"]
    parameters: InvalidApplyActionOptionCombinationParameters
    error_instance_id: str


__all__ = ["InvalidApplyActionOptionCombination"]
