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

from typing import Literal

from typing_extensions import TypedDict

from foundry.v1.ontologies.models._field_name_v1 import FieldNameV1


class PrefixQueryDict(TypedDict):
    """Returns objects where the specified field starts with the provided value."""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    field: FieldNameV1

    value: str

    type: Literal["prefix"]
