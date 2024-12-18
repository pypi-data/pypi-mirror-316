"""
Type annotations for mgh service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mgh.client import MigrationHubClient
    from types_aiobotocore_mgh.paginator import (
        ListApplicationStatesPaginator,
        ListCreatedArtifactsPaginator,
        ListDiscoveredResourcesPaginator,
        ListMigrationTaskUpdatesPaginator,
        ListMigrationTasksPaginator,
        ListProgressUpdateStreamsPaginator,
        ListSourceResourcesPaginator,
    )

    session = get_session()
    with session.create_client("mgh") as client:
        client: MigrationHubClient

        list_application_states_paginator: ListApplicationStatesPaginator = client.get_paginator("list_application_states")
        list_created_artifacts_paginator: ListCreatedArtifactsPaginator = client.get_paginator("list_created_artifacts")
        list_discovered_resources_paginator: ListDiscoveredResourcesPaginator = client.get_paginator("list_discovered_resources")
        list_migration_task_updates_paginator: ListMigrationTaskUpdatesPaginator = client.get_paginator("list_migration_task_updates")
        list_migration_tasks_paginator: ListMigrationTasksPaginator = client.get_paginator("list_migration_tasks")
        list_progress_update_streams_paginator: ListProgressUpdateStreamsPaginator = client.get_paginator("list_progress_update_streams")
        list_source_resources_paginator: ListSourceResourcesPaginator = client.get_paginator("list_source_resources")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationStatesRequestListApplicationStatesPaginateTypeDef,
    ListApplicationStatesResultTypeDef,
    ListCreatedArtifactsRequestListCreatedArtifactsPaginateTypeDef,
    ListCreatedArtifactsResultTypeDef,
    ListDiscoveredResourcesRequestListDiscoveredResourcesPaginateTypeDef,
    ListDiscoveredResourcesResultTypeDef,
    ListMigrationTasksRequestListMigrationTasksPaginateTypeDef,
    ListMigrationTasksResultTypeDef,
    ListMigrationTaskUpdatesRequestListMigrationTaskUpdatesPaginateTypeDef,
    ListMigrationTaskUpdatesResultTypeDef,
    ListProgressUpdateStreamsRequestListProgressUpdateStreamsPaginateTypeDef,
    ListProgressUpdateStreamsResultTypeDef,
    ListSourceResourcesRequestListSourceResourcesPaginateTypeDef,
    ListSourceResourcesResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationStatesPaginator",
    "ListCreatedArtifactsPaginator",
    "ListDiscoveredResourcesPaginator",
    "ListMigrationTaskUpdatesPaginator",
    "ListMigrationTasksPaginator",
    "ListProgressUpdateStreamsPaginator",
    "ListSourceResourcesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationStatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListApplicationStates.html#MigrationHub.Paginator.ListApplicationStates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listapplicationstatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationStatesRequestListApplicationStatesPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListApplicationStates.html#MigrationHub.Paginator.ListApplicationStates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listapplicationstatespaginator)
        """

class ListCreatedArtifactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListCreatedArtifacts.html#MigrationHub.Paginator.ListCreatedArtifacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listcreatedartifactspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCreatedArtifactsRequestListCreatedArtifactsPaginateTypeDef]
    ) -> AsyncIterator[ListCreatedArtifactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListCreatedArtifacts.html#MigrationHub.Paginator.ListCreatedArtifacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listcreatedartifactspaginator)
        """

class ListDiscoveredResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListDiscoveredResources.html#MigrationHub.Paginator.ListDiscoveredResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listdiscoveredresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDiscoveredResourcesRequestListDiscoveredResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListDiscoveredResourcesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListDiscoveredResources.html#MigrationHub.Paginator.ListDiscoveredResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listdiscoveredresourcespaginator)
        """

class ListMigrationTaskUpdatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListMigrationTaskUpdates.html#MigrationHub.Paginator.ListMigrationTaskUpdates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listmigrationtaskupdatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListMigrationTaskUpdatesRequestListMigrationTaskUpdatesPaginateTypeDef],
    ) -> AsyncIterator[ListMigrationTaskUpdatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListMigrationTaskUpdates.html#MigrationHub.Paginator.ListMigrationTaskUpdates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listmigrationtaskupdatespaginator)
        """

class ListMigrationTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListMigrationTasks.html#MigrationHub.Paginator.ListMigrationTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listmigrationtaskspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMigrationTasksRequestListMigrationTasksPaginateTypeDef]
    ) -> AsyncIterator[ListMigrationTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListMigrationTasks.html#MigrationHub.Paginator.ListMigrationTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listmigrationtaskspaginator)
        """

class ListProgressUpdateStreamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListProgressUpdateStreams.html#MigrationHub.Paginator.ListProgressUpdateStreams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listprogressupdatestreamspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListProgressUpdateStreamsRequestListProgressUpdateStreamsPaginateTypeDef],
    ) -> AsyncIterator[ListProgressUpdateStreamsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListProgressUpdateStreams.html#MigrationHub.Paginator.ListProgressUpdateStreams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listprogressupdatestreamspaginator)
        """

class ListSourceResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListSourceResources.html#MigrationHub.Paginator.ListSourceResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listsourceresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSourceResourcesRequestListSourceResourcesPaginateTypeDef]
    ) -> AsyncIterator[ListSourceResourcesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgh/paginator/ListSourceResources.html#MigrationHub.Paginator.ListSourceResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgh/paginators/#listsourceresourcespaginator)
        """
