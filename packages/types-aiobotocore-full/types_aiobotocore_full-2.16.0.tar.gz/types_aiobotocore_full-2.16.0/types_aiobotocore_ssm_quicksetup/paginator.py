"""
Type annotations for ssm-quicksetup service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm_quicksetup.client import SystemsManagerQuickSetupClient
    from types_aiobotocore_ssm_quicksetup.paginator import (
        ListConfigurationManagersPaginator,
        ListConfigurationsPaginator,
    )

    session = get_session()
    with session.create_client("ssm-quicksetup") as client:
        client: SystemsManagerQuickSetupClient

        list_configuration_managers_paginator: ListConfigurationManagersPaginator = client.get_paginator("list_configuration_managers")
        list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListConfigurationManagersInputListConfigurationManagersPaginateTypeDef,
    ListConfigurationManagersOutputTypeDef,
    ListConfigurationsInputListConfigurationsPaginateTypeDef,
    ListConfigurationsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListConfigurationManagersPaginator", "ListConfigurationsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListConfigurationManagersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurationManagers.html#SystemsManagerQuickSetup.Paginator.ListConfigurationManagers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/#listconfigurationmanagerspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListConfigurationManagersInputListConfigurationManagersPaginateTypeDef],
    ) -> AsyncIterator[ListConfigurationManagersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurationManagers.html#SystemsManagerQuickSetup.Paginator.ListConfigurationManagers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/#listconfigurationmanagerspaginator)
        """


class ListConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurations.html#SystemsManagerQuickSetup.Paginator.ListConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/#listconfigurationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListConfigurationsInputListConfigurationsPaginateTypeDef]
    ) -> AsyncIterator[ListConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-quicksetup/paginator/ListConfigurations.html#SystemsManagerQuickSetup.Paginator.ListConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_quicksetup/paginators/#listconfigurationspaginator)
        """
