"""
Type annotations for bedrock-data-automation service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_data_automation.client import DataAutomationforBedrockClient
    from types_aiobotocore_bedrock_data_automation.paginator import (
        ListBlueprintsPaginator,
        ListDataAutomationProjectsPaginator,
    )

    session = get_session()
    with session.create_client("bedrock-data-automation") as client:
        client: DataAutomationforBedrockClient

        list_blueprints_paginator: ListBlueprintsPaginator = client.get_paginator("list_blueprints")
        list_data_automation_projects_paginator: ListDataAutomationProjectsPaginator = client.get_paginator("list_data_automation_projects")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListBlueprintsRequestListBlueprintsPaginateTypeDef,
    ListBlueprintsResponseTypeDef,
    ListDataAutomationProjectsRequestListDataAutomationProjectsPaginateTypeDef,
    ListDataAutomationProjectsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListBlueprintsPaginator", "ListDataAutomationProjectsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBlueprintsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListBlueprints.html#DataAutomationforBedrock.Paginator.ListBlueprints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listblueprintspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBlueprintsRequestListBlueprintsPaginateTypeDef]
    ) -> AsyncIterator[ListBlueprintsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListBlueprints.html#DataAutomationforBedrock.Paginator.ListBlueprints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listblueprintspaginator)
        """


class ListDataAutomationProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationProjects.html#DataAutomationforBedrock.Paginator.ListDataAutomationProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationprojectspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListDataAutomationProjectsRequestListDataAutomationProjectsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListDataAutomationProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/paginator/ListDataAutomationProjects.html#DataAutomationforBedrock.Paginator.ListDataAutomationProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/paginators/#listdataautomationprojectspaginator)
        """
