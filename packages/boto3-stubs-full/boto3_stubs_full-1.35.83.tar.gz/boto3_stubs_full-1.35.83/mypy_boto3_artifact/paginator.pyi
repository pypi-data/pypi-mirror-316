"""
Type annotations for artifact service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_artifact.client import ArtifactClient
    from mypy_boto3_artifact.paginator import (
        ListCustomerAgreementsPaginator,
        ListReportsPaginator,
    )

    session = Session()
    client: ArtifactClient = session.client("artifact")

    list_customer_agreements_paginator: ListCustomerAgreementsPaginator = client.get_paginator("list_customer_agreements")
    list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

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

class ListCustomerAgreementsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListCustomerAgreements.html#Artifact.Paginator.ListCustomerAgreements)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/paginators/#listcustomeragreementspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCustomerAgreementsRequestListCustomerAgreementsPaginateTypeDef]
    ) -> _PageIterator[ListCustomerAgreementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListCustomerAgreements.html#Artifact.Paginator.ListCustomerAgreements.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/paginators/#listcustomeragreementspaginator)
        """

class ListReportsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReports.html#Artifact.Paginator.ListReports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/paginators/#listreportspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListReportsRequestListReportsPaginateTypeDef]
    ) -> _PageIterator[ListReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/paginator/ListReports.html#Artifact.Paginator.ListReports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/paginators/#listreportspaginator)
        """
