"""
Type annotations for networkflowmonitor service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_networkflowmonitor.client import NetworkFlowMonitorClient
    from types_aiobotocore_networkflowmonitor.paginator import (
        GetQueryResultsMonitorTopContributorsPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsDataPaginator,
        GetQueryResultsWorkloadInsightsTopContributorsPaginator,
        ListMonitorsPaginator,
        ListScopesPaginator,
    )

    session = get_session()
    with session.create_client("networkflowmonitor") as client:
        client: NetworkFlowMonitorClient

        get_query_results_monitor_top_contributors_paginator: GetQueryResultsMonitorTopContributorsPaginator = client.get_paginator("get_query_results_monitor_top_contributors")
        get_query_results_workload_insights_top_contributors_data_paginator: GetQueryResultsWorkloadInsightsTopContributorsDataPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors_data")
        get_query_results_workload_insights_top_contributors_paginator: GetQueryResultsWorkloadInsightsTopContributorsPaginator = client.get_paginator("get_query_results_workload_insights_top_contributors")
        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
        list_scopes_paginator: ListScopesPaginator = client.get_paginator("list_scopes")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetQueryResultsMonitorTopContributorsInputGetQueryResultsMonitorTopContributorsPaginateTypeDef,
    GetQueryResultsMonitorTopContributorsOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataInputGetQueryResultsWorkloadInsightsTopContributorsDataPaginateTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsInputGetQueryResultsWorkloadInsightsTopContributorsPaginateTypeDef,
    GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef,
    ListMonitorsInputListMonitorsPaginateTypeDef,
    ListMonitorsOutputTypeDef,
    ListScopesInputListScopesPaginateTypeDef,
    ListScopesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetQueryResultsMonitorTopContributorsPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsDataPaginator",
    "GetQueryResultsWorkloadInsightsTopContributorsPaginator",
    "ListMonitorsPaginator",
    "ListScopesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetQueryResultsMonitorTopContributorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsMonitorTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsMonitorTopContributors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsmonitortopcontributorspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetQueryResultsMonitorTopContributorsInputGetQueryResultsMonitorTopContributorsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetQueryResultsMonitorTopContributorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsMonitorTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsMonitorTopContributors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsmonitortopcontributorspaginator)
        """

class GetQueryResultsWorkloadInsightsTopContributorsDataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributorsData.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributorsData)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorsdatapaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetQueryResultsWorkloadInsightsTopContributorsDataInputGetQueryResultsWorkloadInsightsTopContributorsDataPaginateTypeDef
        ],
    ) -> AsyncIterator[GetQueryResultsWorkloadInsightsTopContributorsDataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributorsData.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributorsData.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorsdatapaginator)
        """

class GetQueryResultsWorkloadInsightsTopContributorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetQueryResultsWorkloadInsightsTopContributorsInputGetQueryResultsWorkloadInsightsTopContributorsPaginateTypeDef
        ],
    ) -> AsyncIterator[GetQueryResultsWorkloadInsightsTopContributorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/GetQueryResultsWorkloadInsightsTopContributors.html#NetworkFlowMonitor.Paginator.GetQueryResultsWorkloadInsightsTopContributors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#getqueryresultsworkloadinsightstopcontributorspaginator)
        """

class ListMonitorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListMonitors.html#NetworkFlowMonitor.Paginator.ListMonitors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#listmonitorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMonitorsInputListMonitorsPaginateTypeDef]
    ) -> AsyncIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListMonitors.html#NetworkFlowMonitor.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#listmonitorspaginator)
        """

class ListScopesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListScopes.html#NetworkFlowMonitor.Paginator.ListScopes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#listscopespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListScopesInputListScopesPaginateTypeDef]
    ) -> AsyncIterator[ListScopesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkflowmonitor/paginator/ListScopes.html#NetworkFlowMonitor.Paginator.ListScopes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkflowmonitor/paginators/#listscopespaginator)
        """
