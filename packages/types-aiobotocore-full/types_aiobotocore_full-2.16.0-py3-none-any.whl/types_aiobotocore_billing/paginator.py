"""
Type annotations for billing service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_billing.client import BillingClient
    from types_aiobotocore_billing.paginator import (
        ListBillingViewsPaginator,
    )

    session = get_session()
    with session.create_client("billing") as client:
        client: BillingClient

        list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListBillingViewsRequestListBillingViewsPaginateTypeDef,
    ListBillingViewsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListBillingViewsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBillingViewsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbillingviewspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBillingViewsRequestListBillingViewsPaginateTypeDef]
    ) -> AsyncIterator[ListBillingViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billing/paginators/#listbillingviewspaginator)
        """
