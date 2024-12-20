"""
Type annotations for billing service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_billing.client import BillingClient
    from types_boto3_billing.paginator import (
        ListBillingViewsPaginator,
    )

    session = Session()
    client: BillingClient = session.client("billing")

    list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListBillingViewsRequestPaginateTypeDef, ListBillingViewsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListBillingViewsPaginator",)

if TYPE_CHECKING:
    _ListBillingViewsPaginatorBase = Paginator[ListBillingViewsResponseTypeDef]
else:
    _ListBillingViewsPaginatorBase = Paginator  # type: ignore[assignment]

class ListBillingViewsPaginator(_ListBillingViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/paginators/#listbillingviewspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingViewsRequestPaginateTypeDef]
    ) -> PageIterator[ListBillingViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billing/paginator/ListBillingViews.html#Billing.Paginator.ListBillingViews.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_billing/paginators/#listbillingviewspaginator)
        """
