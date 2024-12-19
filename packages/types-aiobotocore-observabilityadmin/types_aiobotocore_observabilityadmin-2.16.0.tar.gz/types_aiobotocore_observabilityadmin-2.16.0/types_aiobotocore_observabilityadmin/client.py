"""
Type annotations for observabilityadmin service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_observabilityadmin.client import CloudWatchObservabilityAdminServiceClient

    session = get_session()
    async with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListResourceTelemetryForOrganizationPaginator, ListResourceTelemetryPaginator
from .type_defs import (
    EmptyResponseMetadataTypeDef,
    GetTelemetryEvaluationStatusForOrganizationOutputTypeDef,
    GetTelemetryEvaluationStatusOutputTypeDef,
    ListResourceTelemetryForOrganizationInputRequestTypeDef,
    ListResourceTelemetryForOrganizationOutputTypeDef,
    ListResourceTelemetryInputRequestTypeDef,
    ListResourceTelemetryOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CloudWatchObservabilityAdminServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudWatchObservabilityAdminServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchObservabilityAdminServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/close.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#close)
        """

    async def get_telemetry_evaluation_status(self) -> GetTelemetryEvaluationStatusOutputTypeDef:
        """
        Returns the current onboarding status of the telemetry config feature,
        including the status of the feature and reason the feature failed to start or
        stop.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_evaluation_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_evaluation_status)
        """

    async def get_telemetry_evaluation_status_for_organization(
        self,
    ) -> GetTelemetryEvaluationStatusForOrganizationOutputTypeDef:
        """
        This returns the onboarding status of the telemetry configuration feature for
        the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_evaluation_status_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_evaluation_status_for_organization)
        """

    async def list_resource_telemetry(
        self, **kwargs: Unpack[ListResourceTelemetryInputRequestTypeDef]
    ) -> ListResourceTelemetryOutputTypeDef:
        """
        Returns a list of telemetry configurations for AWS resources supported by
        telemetry config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_resource_telemetry.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_resource_telemetry)
        """

    async def list_resource_telemetry_for_organization(
        self, **kwargs: Unpack[ListResourceTelemetryForOrganizationInputRequestTypeDef]
    ) -> ListResourceTelemetryForOrganizationOutputTypeDef:
        """
        Returns a list of telemetry configurations for AWS resources supported by
        telemetry config in the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_resource_telemetry_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_resource_telemetry_for_organization)
        """

    async def start_telemetry_evaluation(self) -> EmptyResponseMetadataTypeDef:
        """
        This action begins onboarding onboarding the caller AWS account to the
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/start_telemetry_evaluation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#start_telemetry_evaluation)
        """

    async def start_telemetry_evaluation_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        This actions begins onboarding the organization and all member accounts to the
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/start_telemetry_evaluation_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#start_telemetry_evaluation_for_organization)
        """

    async def stop_telemetry_evaluation(self) -> EmptyResponseMetadataTypeDef:
        """
        This action begins offboarding the caller AWS account from the telemetry config
        feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/stop_telemetry_evaluation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#stop_telemetry_evaluation)
        """

    async def stop_telemetry_evaluation_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        This action offboards the Organization of the caller AWS account from thef
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/stop_telemetry_evaluation_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#stop_telemetry_evaluation_for_organization)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_telemetry_for_organization"]
    ) -> ListResourceTelemetryForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_telemetry"]
    ) -> ListResourceTelemetryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    async def __aenter__(self) -> "CloudWatchObservabilityAdminServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
        """
