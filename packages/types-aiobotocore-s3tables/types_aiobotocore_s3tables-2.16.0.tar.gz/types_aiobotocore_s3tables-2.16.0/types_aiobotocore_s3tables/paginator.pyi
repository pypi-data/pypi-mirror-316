"""
Type annotations for s3tables service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3tables.client import S3TablesClient
    from types_aiobotocore_s3tables.paginator import (
        ListNamespacesPaginator,
        ListTableBucketsPaginator,
        ListTablesPaginator,
    )

    session = get_session()
    with session.create_client("s3tables") as client:
        client: S3TablesClient

        list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
        list_table_buckets_paginator: ListTableBucketsPaginator = client.get_paginator("list_table_buckets")
        list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListNamespacesRequestListNamespacesPaginateTypeDef,
    ListNamespacesResponseTypeDef,
    ListTableBucketsRequestListTableBucketsPaginateTypeDef,
    ListTableBucketsResponseTypeDef,
    ListTablesRequestListTablesPaginateTypeDef,
    ListTablesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListNamespacesPaginator", "ListTableBucketsPaginator", "ListTablesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListNamespacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListNamespaces.html#S3Tables.Paginator.ListNamespaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listnamespacespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListNamespacesRequestListNamespacesPaginateTypeDef]
    ) -> AsyncIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListNamespaces.html#S3Tables.Paginator.ListNamespaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listnamespacespaginator)
        """

class ListTableBucketsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTableBuckets.html#S3Tables.Paginator.ListTableBuckets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listtablebucketspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTableBucketsRequestListTableBucketsPaginateTypeDef]
    ) -> AsyncIterator[ListTableBucketsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTableBuckets.html#S3Tables.Paginator.ListTableBuckets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listtablebucketspaginator)
        """

class ListTablesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTables.html#S3Tables.Paginator.ListTables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listtablespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTablesRequestListTablesPaginateTypeDef]
    ) -> AsyncIterator[ListTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/paginator/ListTables.html#S3Tables.Paginator.ListTables.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/paginators/#listtablespaginator)
        """
