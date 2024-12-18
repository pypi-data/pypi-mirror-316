"""
Type annotations for connectcampaignsv2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_connectcampaignsv2.client import ConnectCampaignServiceV2Client
    from types_aiobotocore_connectcampaignsv2.paginator import (
        ListCampaignsPaginator,
        ListConnectInstanceIntegrationsPaginator,
    )

    session = get_session()
    with session.create_client("connectcampaignsv2") as client:
        client: ConnectCampaignServiceV2Client

        list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
        list_connect_instance_integrations_paginator: ListConnectInstanceIntegrationsPaginator = client.get_paginator("list_connect_instance_integrations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListCampaignsRequestListCampaignsPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListConnectInstanceIntegrationsRequestListConnectInstanceIntegrationsPaginateTypeDef,
    ListConnectInstanceIntegrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListCampaignsPaginator", "ListConnectInstanceIntegrationsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCampaignsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListCampaigns.html#ConnectCampaignServiceV2.Paginator.ListCampaigns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/#listcampaignspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCampaignsRequestListCampaignsPaginateTypeDef]
    ) -> AsyncIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListCampaigns.html#ConnectCampaignServiceV2.Paginator.ListCampaigns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/#listcampaignspaginator)
        """

class ListConnectInstanceIntegrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListConnectInstanceIntegrations.html#ConnectCampaignServiceV2.Paginator.ListConnectInstanceIntegrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/#listconnectinstanceintegrationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListConnectInstanceIntegrationsRequestListConnectInstanceIntegrationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListConnectInstanceIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcampaignsv2/paginator/ListConnectInstanceIntegrations.html#ConnectCampaignServiceV2.Paginator.ListConnectInstanceIntegrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcampaignsv2/paginators/#listconnectinstanceintegrationspaginator)
        """
