"""
Type annotations for socialmessaging service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_socialmessaging.client import EndUserMessagingSocialClient
    from types_aiobotocore_socialmessaging.paginator import (
        ListLinkedWhatsAppBusinessAccountsPaginator,
    )

    session = get_session()
    with session.create_client("socialmessaging") as client:
        client: EndUserMessagingSocialClient

        list_linked_whatsapp_business_accounts_paginator: ListLinkedWhatsAppBusinessAccountsPaginator = client.get_paginator("list_linked_whatsapp_business_accounts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListLinkedWhatsAppBusinessAccountsInputListLinkedWhatsAppBusinessAccountsPaginateTypeDef,
    ListLinkedWhatsAppBusinessAccountsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListLinkedWhatsAppBusinessAccountsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListLinkedWhatsAppBusinessAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListLinkedWhatsAppBusinessAccounts.html#EndUserMessagingSocial.Paginator.ListLinkedWhatsAppBusinessAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/#listlinkedwhatsappbusinessaccountspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListLinkedWhatsAppBusinessAccountsInputListLinkedWhatsAppBusinessAccountsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListLinkedWhatsAppBusinessAccountsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListLinkedWhatsAppBusinessAccounts.html#EndUserMessagingSocial.Paginator.ListLinkedWhatsAppBusinessAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/#listlinkedwhatsappbusinessaccountspaginator)
        """
