"""
Type annotations for artifact service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_artifact.client import ArtifactClient

    session = get_session()
    async with session.create_client("artifact") as client:
        client: ArtifactClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListCustomerAgreementsPaginator, ListReportsPaginator
from .type_defs import (
    GetAccountSettingsResponseTypeDef,
    GetReportMetadataRequestRequestTypeDef,
    GetReportMetadataResponseTypeDef,
    GetReportRequestRequestTypeDef,
    GetReportResponseTypeDef,
    GetTermForReportRequestRequestTypeDef,
    GetTermForReportResponseTypeDef,
    ListCustomerAgreementsRequestRequestTypeDef,
    ListCustomerAgreementsResponseTypeDef,
    ListReportsRequestRequestTypeDef,
    ListReportsResponseTypeDef,
    PutAccountSettingsRequestRequestTypeDef,
    PutAccountSettingsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ArtifactClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ArtifactClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ArtifactClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/close.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#close)
        """

    async def get_account_settings(self) -> GetAccountSettingsResponseTypeDef:
        """
        Get the account settings for Artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_account_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_account_settings)
        """

    async def get_report(
        self, **kwargs: Unpack[GetReportRequestRequestTypeDef]
    ) -> GetReportResponseTypeDef:
        """
        Get the content for a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_report.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_report)
        """

    async def get_report_metadata(
        self, **kwargs: Unpack[GetReportMetadataRequestRequestTypeDef]
    ) -> GetReportMetadataResponseTypeDef:
        """
        Get the metadata for a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_report_metadata.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_report_metadata)
        """

    async def get_term_for_report(
        self, **kwargs: Unpack[GetTermForReportRequestRequestTypeDef]
    ) -> GetTermForReportResponseTypeDef:
        """
        Get the Term content associated with a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_term_for_report.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_term_for_report)
        """

    async def list_customer_agreements(
        self, **kwargs: Unpack[ListCustomerAgreementsRequestRequestTypeDef]
    ) -> ListCustomerAgreementsResponseTypeDef:
        """
        List active customer-agreements applicable to calling identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_customer_agreements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#list_customer_agreements)
        """

    async def list_reports(
        self, **kwargs: Unpack[ListReportsRequestRequestTypeDef]
    ) -> ListReportsResponseTypeDef:
        """
        List available reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_reports.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#list_reports)
        """

    async def put_account_settings(
        self, **kwargs: Unpack[PutAccountSettingsRequestRequestTypeDef]
    ) -> PutAccountSettingsResponseTypeDef:
        """
        Put the account settings for Artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/put_account_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#put_account_settings)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_customer_agreements"]
    ) -> ListCustomerAgreementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_reports"]) -> ListReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_paginator)
        """

    async def __aenter__(self) -> "ArtifactClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/)
        """
