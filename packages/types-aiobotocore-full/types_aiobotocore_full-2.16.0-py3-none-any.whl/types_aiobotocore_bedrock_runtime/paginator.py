"""
Type annotations for bedrock-runtime service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_runtime.client import BedrockRuntimeClient
    from types_aiobotocore_bedrock_runtime.paginator import (
        ListAsyncInvokesPaginator,
    )

    session = get_session()
    with session.create_client("bedrock-runtime") as client:
        client: BedrockRuntimeClient

        list_async_invokes_paginator: ListAsyncInvokesPaginator = client.get_paginator("list_async_invokes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAsyncInvokesRequestListAsyncInvokesPaginateTypeDef,
    ListAsyncInvokesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListAsyncInvokesPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAsyncInvokesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/paginator/ListAsyncInvokes.html#BedrockRuntime.Paginator.ListAsyncInvokes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/paginators/#listasyncinvokespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListAsyncInvokesRequestListAsyncInvokesPaginateTypeDef]
    ) -> AsyncIterator[ListAsyncInvokesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/paginator/ListAsyncInvokes.html#BedrockRuntime.Paginator.ListAsyncInvokes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/paginators/#listasyncinvokespaginator)
        """
