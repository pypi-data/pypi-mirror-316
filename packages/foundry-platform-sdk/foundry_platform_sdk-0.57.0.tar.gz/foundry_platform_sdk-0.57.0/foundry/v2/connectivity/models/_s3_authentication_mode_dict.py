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

from typing import Union

import pydantic
from typing_extensions import Annotated

from foundry.v2.connectivity.models._aws_access_key_dict import AwsAccessKeyDict
from foundry.v2.connectivity.models._cloud_identity_dict import CloudIdentityDict
from foundry.v2.connectivity.models._oidc_dict import OidcDict

S3AuthenticationModeDict = Annotated[
    Union[AwsAccessKeyDict, CloudIdentityDict, OidcDict], pydantic.Field(discriminator="type")
]
"""S3AuthenticationMode"""
