"""
Type annotations for invoicing service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_invoicing.client import InvoicingClient
    from types_aiobotocore_invoicing.paginator import (
        ListInvoiceUnitsPaginator,
    )

    session = get_session()
    with session.create_client("invoicing") as client:
        client: InvoicingClient

        list_invoice_units_paginator: ListInvoiceUnitsPaginator = client.get_paginator("list_invoice_units")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListInvoiceUnitsRequestListInvoiceUnitsPaginateTypeDef,
    ListInvoiceUnitsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListInvoiceUnitsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListInvoiceUnitsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceUnits.html#Invoicing.Paginator.ListInvoiceUnits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/paginators/#listinvoiceunitspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInvoiceUnitsRequestListInvoiceUnitsPaginateTypeDef]
    ) -> AsyncIterator[ListInvoiceUnitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/invoicing/paginator/ListInvoiceUnits.html#Invoicing.Paginator.ListInvoiceUnits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_invoicing/paginators/#listinvoiceunitspaginator)
        """
