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
from typing import cast

import pydantic

from foundry.v2.functions.models._query_aggregation_range_sub_type import (
    QueryAggregationRangeSubType,
)  # NOQA
from foundry.v2.functions.models._query_aggregation_range_type_dict import (
    QueryAggregationRangeTypeDict,
)  # NOQA


class QueryAggregationRangeType(pydantic.BaseModel):
    """QueryAggregationRangeType"""

    sub_type: QueryAggregationRangeSubType = pydantic.Field(alias="subType")

    type: Literal["range"] = "range"

    model_config = {"extra": "allow"}

    def to_dict(self) -> QueryAggregationRangeTypeDict:
        """Return the dictionary representation of the model using the field aliases."""
        return cast(
            QueryAggregationRangeTypeDict, self.model_dump(by_alias=True, exclude_unset=True)
        )
