"""
Type annotations for dataexchange service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dataexchange.client import DataExchangeClient
    from types_aiobotocore_dataexchange.paginator import (
        ListDataGrantsPaginator,
        ListDataSetRevisionsPaginator,
        ListDataSetsPaginator,
        ListEventActionsPaginator,
        ListJobsPaginator,
        ListReceivedDataGrantsPaginator,
        ListRevisionAssetsPaginator,
    )

    session = get_session()
    with session.create_client("dataexchange") as client:
        client: DataExchangeClient

        list_data_grants_paginator: ListDataGrantsPaginator = client.get_paginator("list_data_grants")
        list_data_set_revisions_paginator: ListDataSetRevisionsPaginator = client.get_paginator("list_data_set_revisions")
        list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
        list_event_actions_paginator: ListEventActionsPaginator = client.get_paginator("list_event_actions")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_received_data_grants_paginator: ListReceivedDataGrantsPaginator = client.get_paginator("list_received_data_grants")
        list_revision_assets_paginator: ListRevisionAssetsPaginator = client.get_paginator("list_revision_assets")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDataGrantsRequestListDataGrantsPaginateTypeDef,
    ListDataGrantsResponseTypeDef,
    ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef,
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsRequestListDataSetsPaginateTypeDef,
    ListDataSetsResponseTypeDef,
    ListEventActionsRequestListEventActionsPaginateTypeDef,
    ListEventActionsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListReceivedDataGrantsRequestListReceivedDataGrantsPaginateTypeDef,
    ListReceivedDataGrantsResponseTypeDef,
    ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef,
    ListRevisionAssetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDataGrantsPaginator",
    "ListDataSetRevisionsPaginator",
    "ListDataSetsPaginator",
    "ListEventActionsPaginator",
    "ListJobsPaginator",
    "ListReceivedDataGrantsPaginator",
    "ListRevisionAssetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDataGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataGrants.html#DataExchange.Paginator.ListDataGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatagrantspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataGrantsRequestListDataGrantsPaginateTypeDef]
    ) -> AsyncIterator[ListDataGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataGrants.html#DataExchange.Paginator.ListDataGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatagrantspaginator)
        """


class ListDataSetRevisionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSetRevisions.html#DataExchange.Paginator.ListDataSetRevisions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatasetrevisionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSetRevisionsRequestListDataSetRevisionsPaginateTypeDef]
    ) -> AsyncIterator[ListDataSetRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSetRevisions.html#DataExchange.Paginator.ListDataSetRevisions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatasetrevisionspaginator)
        """


class ListDataSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSets.html#DataExchange.Paginator.ListDataSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatasetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDataSetsRequestListDataSetsPaginateTypeDef]
    ) -> AsyncIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListDataSets.html#DataExchange.Paginator.ListDataSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listdatasetspaginator)
        """


class ListEventActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListEventActions.html#DataExchange.Paginator.ListEventActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listeventactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEventActionsRequestListEventActionsPaginateTypeDef]
    ) -> AsyncIterator[ListEventActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListEventActions.html#DataExchange.Paginator.ListEventActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listeventactionspaginator)
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListJobs.html#DataExchange.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListJobs.html#DataExchange.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listjobspaginator)
        """


class ListReceivedDataGrantsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListReceivedDataGrants.html#DataExchange.Paginator.ListReceivedDataGrants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listreceiveddatagrantspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReceivedDataGrantsRequestListReceivedDataGrantsPaginateTypeDef]
    ) -> AsyncIterator[ListReceivedDataGrantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListReceivedDataGrants.html#DataExchange.Paginator.ListReceivedDataGrants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listreceiveddatagrantspaginator)
        """


class ListRevisionAssetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListRevisionAssets.html#DataExchange.Paginator.ListRevisionAssets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listrevisionassetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListRevisionAssetsRequestListRevisionAssetsPaginateTypeDef]
    ) -> AsyncIterator[ListRevisionAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange/paginator/ListRevisionAssets.html#DataExchange.Paginator.ListRevisionAssets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/paginators/#listrevisionassetspaginator)
        """
