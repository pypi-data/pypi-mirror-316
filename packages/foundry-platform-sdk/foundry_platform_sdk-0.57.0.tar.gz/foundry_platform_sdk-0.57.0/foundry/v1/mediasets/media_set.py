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

from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional
from typing import Union

import pydantic
from typing_extensions import Annotated
from typing_extensions import overload

from foundry._core import ApiClient
from foundry._core import Auth
from foundry._core import BinaryStream
from foundry._core import RequestInfo
from foundry._core.utils import maybe_ignore_preview
from foundry._errors import handle_unexpected
from foundry.v1.core.models._media_item_path import MediaItemPath
from foundry.v1.core.models._media_item_rid import MediaItemRid
from foundry.v1.core.models._media_reference import MediaReference
from foundry.v1.core.models._media_set_rid import MediaSetRid
from foundry.v1.core.models._media_set_view_rid import MediaSetViewRid
from foundry.v1.mediasets.models._branch_name import BranchName
from foundry.v1.mediasets.models._branch_rid import BranchRid
from foundry.v1.mediasets.models._get_media_item_info_response import (
    GetMediaItemInfoResponse,
)  # NOQA
from foundry.v1.mediasets.models._put_media_item_response import PutMediaItemResponse
from foundry.v1.mediasets.models._transaction_id import TransactionId


class MediaSetClient:
    def __init__(self, auth: Auth, hostname: str) -> None:
        self._api_client = ApiClient(auth=auth, hostname=hostname)

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def abort(
        self,
        media_set_rid: MediaSetRid,
        transaction_id: TransactionId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> None:
        """
        Aborts an open transaction. Items uploaded to the media set during this transaction will be deleted.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-write`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param transaction_id: transactionId
        :type transaction_id: TransactionId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: None
        """

        return self._api_client.call_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/mediasets/{mediaSetRid}/transactions/{transactionId}/abort",
                query_params={},
                path_params={
                    "mediaSetRid": media_set_rid,
                    "transactionId": transaction_id,
                },
                header_params={},
                body=None,
                body_type=None,
                response_type=None,
                request_timeout=request_timeout,
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def commit(
        self,
        media_set_rid: MediaSetRid,
        transaction_id: TransactionId,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> None:
        """
        Commits an open transaction. On success, items uploaded to the media set during this transaction will become available.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-write`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param transaction_id: transactionId
        :type transaction_id: TransactionId
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: None
        """

        return self._api_client.call_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/mediasets/{mediaSetRid}/transactions/{transactionId}/commit",
                query_params={},
                path_params={
                    "mediaSetRid": media_set_rid,
                    "transactionId": transaction_id,
                },
                header_params={},
                body=None,
                body_type=None,
                response_type=None,
                request_timeout=request_timeout,
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def create(
        self,
        media_set_rid: MediaSetRid,
        *,
        branch_name: Optional[BranchName] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> TransactionId:
        """
        Creates a new transaction. Items uploaded to the media set while this transaction is open will not be reflected until the transaction is committed.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-write`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param branch_name: branchName
        :type branch_name: Optional[BranchName]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: TransactionId
        """

        return self._api_client.call_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/mediasets/{mediaSetRid}/transactions",
                query_params={
                    "branchName": branch_name,
                },
                path_params={
                    "mediaSetRid": media_set_rid,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=TransactionId,
                request_timeout=request_timeout,
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def info(
        self,
        media_set_rid: MediaSetRid,
        media_item_rid: MediaItemRid,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> GetMediaItemInfoResponse:
        """
        Gets information about the media item.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-read`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param media_item_rid: mediaItemRid
        :type media_item_rid: MediaItemRid
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: GetMediaItemInfoResponse
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/info",
                query_params={},
                path_params={
                    "mediaSetRid": media_set_rid,
                    "mediaItemRid": media_item_rid,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=GetMediaItemInfoResponse,
                request_timeout=request_timeout,
            ),
        )

    @overload
    def read(
        self,
        media_set_rid: MediaSetRid,
        media_item_rid: MediaItemRid,
        *,
        stream: Literal[True],
        chunk_size: Optional[int] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> BinaryStream:
        """
        Gets the content of a media item.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-read`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param media_item_rid: mediaItemRid
        :type media_item_rid: MediaItemRid
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: BinaryStream
        """
        ...

    @overload
    def read(
        self,
        media_set_rid: MediaSetRid,
        media_item_rid: MediaItemRid,
        *,
        stream: Literal[False] = False,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> bytes:
        """
        Gets the content of a media item.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-read`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param media_item_rid: mediaItemRid
        :type media_item_rid: MediaItemRid
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: bytes
        """
        ...

    @overload
    def read(
        self,
        media_set_rid: MediaSetRid,
        media_item_rid: MediaItemRid,
        *,
        stream: bool,
        chunk_size: Optional[int] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> Union[bytes, BinaryStream]:
        """
        Gets the content of a media item.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-read`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param media_item_rid: mediaItemRid
        :type media_item_rid: MediaItemRid
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: Union[bytes, BinaryStream]
        """
        ...

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def read(
        self,
        media_set_rid: MediaSetRid,
        media_item_rid: MediaItemRid,
        *,
        stream: bool = False,
        chunk_size: Optional[int] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> Union[bytes, BinaryStream]:
        """
        Gets the content of a media item.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-read`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param media_item_rid: mediaItemRid
        :type media_item_rid: MediaItemRid
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: Union[bytes, BinaryStream]
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/mediasets/{mediaSetRid}/items/{mediaItemRid}",
                query_params={},
                path_params={
                    "mediaSetRid": media_set_rid,
                    "mediaItemRid": media_item_rid,
                },
                header_params={
                    "Accept": "*/*",
                },
                body=None,
                body_type=None,
                response_type=bytes,
                stream=stream,
                chunk_size=chunk_size,
                request_timeout=request_timeout,
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def reference(
        self,
        media_set_rid: MediaSetRid,
        media_item_rid: MediaItemRid,
        *,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> MediaReference:
        """
        Gets the [media reference](/docs/foundry/data-integration/media-sets/#media-references) for this media item.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-read`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param media_item_rid: mediaItemRid
        :type media_item_rid: MediaItemRid
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: MediaReference
        """

        return self._api_client.call_api(
            RequestInfo(
                method="GET",
                resource_path="/v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/reference",
                query_params={},
                path_params={
                    "mediaSetRid": media_set_rid,
                    "mediaItemRid": media_item_rid,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=MediaReference,
                request_timeout=request_timeout,
            ),
        )

    @maybe_ignore_preview
    @pydantic.validate_call
    @handle_unexpected
    def upload(
        self,
        media_set_rid: MediaSetRid,
        body: bytes,
        *,
        branch_name: Optional[BranchName] = None,
        branch_rid: Optional[BranchRid] = None,
        media_item_path: Optional[MediaItemPath] = None,
        transaction_id: Optional[TransactionId] = None,
        view_rid: Optional[MediaSetViewRid] = None,
        request_timeout: Optional[Annotated[pydantic.StrictInt, pydantic.Field(gt=0)]] = None,
    ) -> PutMediaItemResponse:
        """
        Uploads a media item to an existing media set.
        The body of the request must contain the binary content of the file and the `Content-Type` header must be `application/octet-stream`.
        A branch name, or branch rid, or view rid may optionally be specified.  If none is specified, the item will be uploaded to the default branch. If more than one is specified, an error is thrown.

        Third-party applications using this endpoint via OAuth2 must request the following operation scope: `api:mediasets-write`.

        :param media_set_rid: mediaSetRid
        :type media_set_rid: MediaSetRid
        :param body: Body of the request
        :type body: bytes
        :param branch_name: branchName
        :type branch_name: Optional[BranchName]
        :param branch_rid: branchRid
        :type branch_rid: Optional[BranchRid]
        :param media_item_path: mediaItemPath
        :type media_item_path: Optional[MediaItemPath]
        :param transaction_id: transactionId
        :type transaction_id: Optional[TransactionId]
        :param view_rid: viewRid
        :type view_rid: Optional[MediaSetViewRid]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: PutMediaItemResponse
        """

        return self._api_client.call_api(
            RequestInfo(
                method="POST",
                resource_path="/v2/mediasets/{mediaSetRid}/items",
                query_params={
                    "branchName": branch_name,
                    "branchRid": branch_rid,
                    "mediaItemPath": media_item_path,
                    "transactionId": transaction_id,
                    "viewRid": view_rid,
                },
                path_params={
                    "mediaSetRid": media_set_rid,
                },
                header_params={
                    "Content-Type": "*/*",
                    "Accept": "application/json",
                },
                body=body,
                body_type=bytes,
                response_type=PutMediaItemResponse,
                request_timeout=request_timeout,
            ),
        )
