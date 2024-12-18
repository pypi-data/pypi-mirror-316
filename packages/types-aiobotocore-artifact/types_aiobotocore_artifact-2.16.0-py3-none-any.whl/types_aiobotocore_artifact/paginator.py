"""
Type annotations for artifact service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_artifact.client import ArtifactClient
    from types_aiobotocore_artifact.paginator import (
        ListCustomerAgreementsPaginator,
        ListReportsPaginator,
    )

    session = get_session()
    with session.create_client("artifact") as client:
        client: ArtifactClient

        list_customer_agreements_paginator: ListCustomerAgreementsPaginator = client.get_paginator("list_customer_agreements")
        list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListCustomerAgreementsRequestListCustomerAgreementsPaginateTypeDef,
    ListCustomerAgreementsResponseTypeDef,
    ListReportsRequestListReportsPaginateTypeDef,
    ListReportsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListCustomerAgreementsPaginator", "ListReportsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListCustomerAgreementsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListCustomerAgreements.html#Artifact.Paginator.ListCustomerAgreements)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listcustomeragreementspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCustomerAgreementsRequestListCustomerAgreementsPaginateTypeDef]
    ) -> AsyncIterator[ListCustomerAgreementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListCustomerAgreements.html#Artifact.Paginator.ListCustomerAgreements.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listcustomeragreementspaginator)
        """


class ListReportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReports.html#Artifact.Paginator.ListReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listreportspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReportsRequestListReportsPaginateTypeDef]
    ) -> AsyncIterator[ListReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReports.html#Artifact.Paginator.ListReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listreportspaginator)
        """
