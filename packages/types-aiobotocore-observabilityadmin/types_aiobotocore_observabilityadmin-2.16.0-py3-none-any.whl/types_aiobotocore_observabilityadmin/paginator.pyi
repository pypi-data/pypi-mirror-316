"""
Type annotations for observabilityadmin service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_observabilityadmin.client import CloudWatchObservabilityAdminServiceClient
    from types_aiobotocore_observabilityadmin.paginator import (
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
    )

    session = get_session()
    with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient

        list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
        list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListResourceTelemetryForOrganizationInputListResourceTelemetryForOrganizationPaginateTypeDef,
    ListResourceTelemetryForOrganizationOutputTypeDef,
    ListResourceTelemetryInputListResourceTelemetryPaginateTypeDef,
    ListResourceTelemetryOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListResourceTelemetryForOrganizationPaginator", "ListResourceTelemetryPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListResourceTelemetryForOrganizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetryForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetryForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetryfororganizationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListResourceTelemetryForOrganizationInputListResourceTelemetryForOrganizationPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResourceTelemetryForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetryForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetryForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetryfororganizationpaginator)
        """

class ListResourceTelemetryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetry.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetry)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetrypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResourceTelemetryInputListResourceTelemetryPaginateTypeDef]
    ) -> AsyncIterator[ListResourceTelemetryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetry.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetry.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetrypaginator)
        """
