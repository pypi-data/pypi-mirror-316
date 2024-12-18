"""
Main interface for billing service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_billing import (
        BillingClient,
        Client,
        ListBillingViewsPaginator,
    )

    session = get_session()
    async with session.create_client("billing") as client:
        client: BillingClient
        ...


    list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import BillingClient
from .paginator import ListBillingViewsPaginator

Client = BillingClient


__all__ = ("BillingClient", "Client", "ListBillingViewsPaginator")
