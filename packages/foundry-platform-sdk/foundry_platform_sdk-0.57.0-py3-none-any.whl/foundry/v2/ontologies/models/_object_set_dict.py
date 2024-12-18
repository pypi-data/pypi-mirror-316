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
from typing import Literal
from typing import Union

import pydantic
from typing_extensions import Annotated
from typing_extensions import TypedDict

from foundry.v2.ontologies.models._link_type_api_name import LinkTypeApiName
from foundry.v2.ontologies.models._object_set_base_type_dict import ObjectSetBaseTypeDict  # NOQA
from foundry.v2.ontologies.models._object_set_reference_type_dict import (
    ObjectSetReferenceTypeDict,
)  # NOQA
from foundry.v2.ontologies.models._object_set_static_type_dict import (
    ObjectSetStaticTypeDict,
)  # NOQA
from foundry.v2.ontologies.models._search_json_query_v2_dict import SearchJsonQueryV2Dict  # NOQA


class ObjectSetFilterTypeDict(TypedDict):
    """ObjectSetFilterType"""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    objectSet: ObjectSetDict

    where: SearchJsonQueryV2Dict

    type: Literal["filter"]


class ObjectSetSearchAroundTypeDict(TypedDict):
    """ObjectSetSearchAroundType"""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    objectSet: ObjectSetDict

    link: LinkTypeApiName

    type: Literal["searchAround"]


class ObjectSetIntersectionTypeDict(TypedDict):
    """ObjectSetIntersectionType"""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    objectSets: List[ObjectSetDict]

    type: Literal["intersect"]


class ObjectSetSubtractTypeDict(TypedDict):
    """ObjectSetSubtractType"""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    objectSets: List[ObjectSetDict]

    type: Literal["subtract"]


class ObjectSetUnionTypeDict(TypedDict):
    """ObjectSetUnionType"""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    objectSets: List[ObjectSetDict]

    type: Literal["union"]


ObjectSetDict = Annotated[
    Union[
        ObjectSetReferenceTypeDict,
        ObjectSetFilterTypeDict,
        ObjectSetSearchAroundTypeDict,
        ObjectSetStaticTypeDict,
        ObjectSetIntersectionTypeDict,
        ObjectSetSubtractTypeDict,
        ObjectSetUnionTypeDict,
        ObjectSetBaseTypeDict,
    ],
    pydantic.Field(discriminator="type"),
]
"""Represents the definition of an `ObjectSet` in the ontology."""
