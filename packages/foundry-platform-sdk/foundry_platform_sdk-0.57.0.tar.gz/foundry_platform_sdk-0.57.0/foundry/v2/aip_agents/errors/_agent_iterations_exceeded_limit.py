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
from typing_extensions import TypedDict

from foundry._errors import PalantirRPCException
from foundry.v2.aip_agents.models._agent_rid import AgentRid
from foundry.v2.aip_agents.models._session_rid import SessionRid


class AgentIterationsExceededLimitParameters(TypedDict):
    """
    The Agent was unable to produce an answer in the set number of maximum iterations.
    This can happen if the Agent gets confused or stuck in a loop, or if the query is too complex.
    Try a different query or review the Agent configuration in AIP Agent Studio.
    """

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    agentRid: AgentRid

    sessionRid: SessionRid

    details: str
    """Any additional details provided for the error."""


@dataclass
class AgentIterationsExceededLimit(PalantirRPCException):
    name: Literal["AgentIterationsExceededLimit"]
    parameters: AgentIterationsExceededLimitParameters
    error_instance_id: str


__all__ = ["AgentIterationsExceededLimit"]
