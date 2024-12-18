"""
Type annotations for backupsearch service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_backupsearch.client import BackupSearchClient
    from mypy_boto3_backupsearch.paginator import (
        ListSearchJobBackupsPaginator,
        ListSearchJobResultsPaginator,
        ListSearchJobsPaginator,
        ListSearchResultExportJobsPaginator,
    )

    session = Session()
    client: BackupSearchClient = session.client("backupsearch")

    list_search_job_backups_paginator: ListSearchJobBackupsPaginator = client.get_paginator("list_search_job_backups")
    list_search_job_results_paginator: ListSearchJobResultsPaginator = client.get_paginator("list_search_job_results")
    list_search_jobs_paginator: ListSearchJobsPaginator = client.get_paginator("list_search_jobs")
    list_search_result_export_jobs_paginator: ListSearchResultExportJobsPaginator = client.get_paginator("list_search_result_export_jobs")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListSearchJobBackupsInputListSearchJobBackupsPaginateTypeDef,
    ListSearchJobBackupsOutputTypeDef,
    ListSearchJobResultsInputListSearchJobResultsPaginateTypeDef,
    ListSearchJobResultsOutputTypeDef,
    ListSearchJobsInputListSearchJobsPaginateTypeDef,
    ListSearchJobsOutputTypeDef,
    ListSearchResultExportJobsInputListSearchResultExportJobsPaginateTypeDef,
    ListSearchResultExportJobsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListSearchJobBackupsPaginator",
    "ListSearchJobResultsPaginator",
    "ListSearchJobsPaginator",
    "ListSearchResultExportJobsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListSearchJobBackupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobBackups.html#BackupSearch.Paginator.ListSearchJobBackups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/#listsearchjobbackupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSearchJobBackupsInputListSearchJobBackupsPaginateTypeDef]
    ) -> _PageIterator[ListSearchJobBackupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobBackups.html#BackupSearch.Paginator.ListSearchJobBackups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/#listsearchjobbackupspaginator)
        """


class ListSearchJobResultsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobResults.html#BackupSearch.Paginator.ListSearchJobResults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/#listsearchjobresultspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSearchJobResultsInputListSearchJobResultsPaginateTypeDef]
    ) -> _PageIterator[ListSearchJobResultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobResults.html#BackupSearch.Paginator.ListSearchJobResults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/#listsearchjobresultspaginator)
        """


class ListSearchJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobs.html#BackupSearch.Paginator.ListSearchJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/#listsearchjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSearchJobsInputListSearchJobsPaginateTypeDef]
    ) -> _PageIterator[ListSearchJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchJobs.html#BackupSearch.Paginator.ListSearchJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/#listsearchjobspaginator)
        """


class ListSearchResultExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchResultExportJobs.html#BackupSearch.Paginator.ListSearchResultExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/#listsearchresultexportjobspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSearchResultExportJobsInputListSearchResultExportJobsPaginateTypeDef],
    ) -> _PageIterator[ListSearchResultExportJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backupsearch/paginator/ListSearchResultExportJobs.html#BackupSearch.Paginator.ListSearchResultExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backupsearch/paginators/#listsearchresultexportjobspaginator)
        """
