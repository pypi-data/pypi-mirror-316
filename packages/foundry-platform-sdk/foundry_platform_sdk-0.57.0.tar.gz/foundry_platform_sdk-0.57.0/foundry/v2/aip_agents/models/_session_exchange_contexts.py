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
from typing import cast

import pydantic

from foundry.v2.aip_agents.models._object_context import ObjectContext
from foundry.v2.aip_agents.models._session_exchange_contexts_dict import (
    SessionExchangeContextsDict,
)  # NOQA


class SessionExchangeContexts(pydantic.BaseModel):
    """Retrieved context which was passed to the Agent as input for the exchange."""

    object_contexts: List[ObjectContext] = pydantic.Field(alias="objectContexts")

    """Relevant object context for the user's message that was included in the prompt to the Agent."""

    model_config = {"extra": "allow"}

    def to_dict(self) -> SessionExchangeContextsDict:
        """Return the dictionary representation of the model using the field aliases."""
        return cast(SessionExchangeContextsDict, self.model_dump(by_alias=True, exclude_unset=True))
