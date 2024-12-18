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
from foundry.v1.datasets.models._dataset_rid import DatasetRid
from foundry.v1.datasets.models._transaction_rid import TransactionRid


class TransactionNotFoundParameters(TypedDict):
    """The requested transaction could not be found on the dataset, or the client token does not have access to it."""

    __pydantic_config__ = {"extra": "allow"}  # type: ignore

    datasetRid: DatasetRid

    transactionRid: TransactionRid


@dataclass
class TransactionNotFound(PalantirRPCException):
    name: Literal["TransactionNotFound"]
    parameters: TransactionNotFoundParameters
    error_instance_id: str


__all__ = ["TransactionNotFound"]
