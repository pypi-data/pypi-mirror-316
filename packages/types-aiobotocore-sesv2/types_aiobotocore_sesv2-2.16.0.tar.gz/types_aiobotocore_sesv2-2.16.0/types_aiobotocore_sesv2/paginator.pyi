"""
Type annotations for sesv2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sesv2.client import SESV2Client
    from types_aiobotocore_sesv2.paginator import (
        ListMultiRegionEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("sesv2") as client:
        client: SESV2Client

        list_multi_region_endpoints_paginator: ListMultiRegionEndpointsPaginator = client.get_paginator("list_multi_region_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListMultiRegionEndpointsRequestListMultiRegionEndpointsPaginateTypeDef,
    ListMultiRegionEndpointsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListMultiRegionEndpointsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListMultiRegionEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListMultiRegionEndpoints.html#SESV2.Paginator.ListMultiRegionEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listmultiregionendpointspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListMultiRegionEndpointsRequestListMultiRegionEndpointsPaginateTypeDef],
    ) -> AsyncIterator[ListMultiRegionEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListMultiRegionEndpoints.html#SESV2.Paginator.ListMultiRegionEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listmultiregionendpointspaginator)
        """
