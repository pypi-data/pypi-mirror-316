"""
Type annotations for stepfunctions service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_stepfunctions.client import SFNClient
    from mypy_boto3_stepfunctions.paginator import (
        GetExecutionHistoryPaginator,
        ListActivitiesPaginator,
        ListExecutionsPaginator,
        ListMapRunsPaginator,
        ListStateMachinesPaginator,
    )

    session = Session()
    client: SFNClient = session.client("stepfunctions")

    get_execution_history_paginator: GetExecutionHistoryPaginator = client.get_paginator("get_execution_history")
    list_activities_paginator: ListActivitiesPaginator = client.get_paginator("list_activities")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_map_runs_paginator: ListMapRunsPaginator = client.get_paginator("list_map_runs")
    list_state_machines_paginator: ListStateMachinesPaginator = client.get_paginator("list_state_machines")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetExecutionHistoryInputGetExecutionHistoryPaginateTypeDef,
    GetExecutionHistoryOutputTypeDef,
    ListActivitiesInputListActivitiesPaginateTypeDef,
    ListActivitiesOutputTypeDef,
    ListExecutionsInputListExecutionsPaginateTypeDef,
    ListExecutionsOutputTypeDef,
    ListMapRunsInputListMapRunsPaginateTypeDef,
    ListMapRunsOutputTypeDef,
    ListStateMachinesInputListStateMachinesPaginateTypeDef,
    ListStateMachinesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetExecutionHistoryPaginator",
    "ListActivitiesPaginator",
    "ListExecutionsPaginator",
    "ListMapRunsPaginator",
    "ListStateMachinesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetExecutionHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/GetExecutionHistory.html#SFN.Paginator.GetExecutionHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#getexecutionhistorypaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetExecutionHistoryInputGetExecutionHistoryPaginateTypeDef]
    ) -> _PageIterator[GetExecutionHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/GetExecutionHistory.html#SFN.Paginator.GetExecutionHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#getexecutionhistorypaginator)
        """

class ListActivitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListActivities.html#SFN.Paginator.ListActivities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listactivitiespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListActivitiesInputListActivitiesPaginateTypeDef]
    ) -> _PageIterator[ListActivitiesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListActivities.html#SFN.Paginator.ListActivities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listactivitiespaginator)
        """

class ListExecutionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListExecutions.html#SFN.Paginator.ListExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listexecutionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListExecutionsInputListExecutionsPaginateTypeDef]
    ) -> _PageIterator[ListExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListExecutions.html#SFN.Paginator.ListExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listexecutionspaginator)
        """

class ListMapRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListMapRuns.html#SFN.Paginator.ListMapRuns)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listmaprunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMapRunsInputListMapRunsPaginateTypeDef]
    ) -> _PageIterator[ListMapRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListMapRuns.html#SFN.Paginator.ListMapRuns.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#listmaprunspaginator)
        """

class ListStateMachinesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListStateMachines.html#SFN.Paginator.ListStateMachines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#liststatemachinespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStateMachinesInputListStateMachinesPaginateTypeDef]
    ) -> _PageIterator[ListStateMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListStateMachines.html#SFN.Paginator.ListStateMachines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_stepfunctions/paginators/#liststatemachinespaginator)
        """
