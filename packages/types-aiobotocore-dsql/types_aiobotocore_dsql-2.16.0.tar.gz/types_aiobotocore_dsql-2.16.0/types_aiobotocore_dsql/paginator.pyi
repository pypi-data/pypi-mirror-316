"""
Type annotations for dsql service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dsql.client import AuroraDSQLClient
    from types_aiobotocore_dsql.paginator import (
        ListClustersPaginator,
    )

    session = get_session()
    with session.create_client("dsql") as client:
        client: AuroraDSQLClient

        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListClustersInputListClustersPaginateTypeDef, ListClustersOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListClustersPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/paginator/ListClusters.html#AuroraDSQL.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/paginators/#listclusterspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListClustersInputListClustersPaginateTypeDef]
    ) -> AsyncIterator[ListClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dsql/paginator/ListClusters.html#AuroraDSQL.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dsql/paginators/#listclusterspaginator)
        """
