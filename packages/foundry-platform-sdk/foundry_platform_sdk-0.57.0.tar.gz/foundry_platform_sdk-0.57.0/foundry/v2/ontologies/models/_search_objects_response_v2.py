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

from typing import List
from typing import Optional
from typing import cast

import pydantic

from foundry.v2.core.models._page_token import PageToken
from foundry.v2.core.models._total_count import TotalCount
from foundry.v2.ontologies.models._ontology_object_v2 import OntologyObjectV2
from foundry.v2.ontologies.models._search_objects_response_v2_dict import (
    SearchObjectsResponseV2Dict,
)  # NOQA


class SearchObjectsResponseV2(pydantic.BaseModel):
    """SearchObjectsResponseV2"""

    data: List[OntologyObjectV2]

    next_page_token: Optional[PageToken] = pydantic.Field(alias="nextPageToken", default=None)

    total_count: TotalCount = pydantic.Field(alias="totalCount")

    model_config = {"extra": "allow"}

    def to_dict(self) -> SearchObjectsResponseV2Dict:
        """Return the dictionary representation of the model using the field aliases."""
        return cast(SearchObjectsResponseV2Dict, self.model_dump(by_alias=True, exclude_unset=True))
