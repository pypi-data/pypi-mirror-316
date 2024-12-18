"""
Type annotations for workspaces-web service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workspaces_web.client import WorkSpacesWebClient
    from types_aiobotocore_workspaces_web.paginator import (
        ListDataProtectionSettingsPaginator,
        ListSessionsPaginator,
    )

    session = get_session()
    with session.create_client("workspaces-web") as client:
        client: WorkSpacesWebClient

        list_data_protection_settings_paginator: ListDataProtectionSettingsPaginator = client.get_paginator("list_data_protection_settings")
        list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDataProtectionSettingsRequestListDataProtectionSettingsPaginateTypeDef,
    ListDataProtectionSettingsResponseTypeDef,
    ListSessionsRequestListSessionsPaginateTypeDef,
    ListSessionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDataProtectionSettingsPaginator", "ListSessionsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDataProtectionSettingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/paginator/ListDataProtectionSettings.html#WorkSpacesWeb.Paginator.ListDataProtectionSettings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/paginators/#listdataprotectionsettingspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListDataProtectionSettingsRequestListDataProtectionSettingsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDataProtectionSettingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/paginator/ListDataProtectionSettings.html#WorkSpacesWeb.Paginator.ListDataProtectionSettings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/paginators/#listdataprotectionsettingspaginator)
        """

class ListSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/paginator/ListSessions.html#WorkSpacesWeb.Paginator.ListSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/paginators/#listsessionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSessionsRequestListSessionsPaginateTypeDef]
    ) -> AsyncIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/paginator/ListSessions.html#WorkSpacesWeb.Paginator.ListSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/paginators/#listsessionspaginator)
        """
