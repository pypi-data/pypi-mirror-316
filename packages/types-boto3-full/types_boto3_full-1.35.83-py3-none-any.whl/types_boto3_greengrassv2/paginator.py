"""
Type annotations for greengrassv2 service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_greengrassv2.client import GreengrassV2Client
    from types_boto3_greengrassv2.paginator import (
        ListClientDevicesAssociatedWithCoreDevicePaginator,
        ListComponentVersionsPaginator,
        ListComponentsPaginator,
        ListCoreDevicesPaginator,
        ListDeploymentsPaginator,
        ListEffectiveDeploymentsPaginator,
        ListInstalledComponentsPaginator,
    )

    session = Session()
    client: GreengrassV2Client = session.client("greengrassv2")

    list_client_devices_associated_with_core_device_paginator: ListClientDevicesAssociatedWithCoreDevicePaginator = client.get_paginator("list_client_devices_associated_with_core_device")
    list_component_versions_paginator: ListComponentVersionsPaginator = client.get_paginator("list_component_versions")
    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_core_devices_paginator: ListCoreDevicesPaginator = client.get_paginator("list_core_devices")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_effective_deployments_paginator: ListEffectiveDeploymentsPaginator = client.get_paginator("list_effective_deployments")
    list_installed_components_paginator: ListInstalledComponentsPaginator = client.get_paginator("list_installed_components")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef,
    ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef,
    ListComponentsRequestListComponentsPaginateTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentVersionsRequestListComponentVersionsPaginateTypeDef,
    ListComponentVersionsResponseTypeDef,
    ListCoreDevicesRequestListCoreDevicesPaginateTypeDef,
    ListCoreDevicesResponseTypeDef,
    ListDeploymentsRequestListDeploymentsPaginateTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef,
    ListEffectiveDeploymentsResponseTypeDef,
    ListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef,
    ListInstalledComponentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListClientDevicesAssociatedWithCoreDevicePaginator",
    "ListComponentVersionsPaginator",
    "ListComponentsPaginator",
    "ListCoreDevicesPaginator",
    "ListDeploymentsPaginator",
    "ListEffectiveDeploymentsPaginator",
    "ListInstalledComponentsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListClientDevicesAssociatedWithCoreDevicePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListClientDevicesAssociatedWithCoreDevice.html#GreengrassV2.Paginator.ListClientDevicesAssociatedWithCoreDevice)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listclientdevicesassociatedwithcoredevicepaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef
        ],
    ) -> _PageIterator[ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListClientDevicesAssociatedWithCoreDevice.html#GreengrassV2.Paginator.ListClientDevicesAssociatedWithCoreDevice.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listclientdevicesassociatedwithcoredevicepaginator)
        """


class ListComponentVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListComponentVersions.html#GreengrassV2.Paginator.ListComponentVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listcomponentversionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComponentVersionsRequestListComponentVersionsPaginateTypeDef]
    ) -> _PageIterator[ListComponentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListComponentVersions.html#GreengrassV2.Paginator.ListComponentVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listcomponentversionspaginator)
        """


class ListComponentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListComponents.html#GreengrassV2.Paginator.ListComponents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listcomponentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListComponentsRequestListComponentsPaginateTypeDef]
    ) -> _PageIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListComponents.html#GreengrassV2.Paginator.ListComponents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listcomponentspaginator)
        """


class ListCoreDevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListCoreDevices.html#GreengrassV2.Paginator.ListCoreDevices)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listcoredevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListCoreDevicesRequestListCoreDevicesPaginateTypeDef]
    ) -> _PageIterator[ListCoreDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListCoreDevices.html#GreengrassV2.Paginator.ListCoreDevices.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listcoredevicespaginator)
        """


class ListDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListDeployments.html#GreengrassV2.Paginator.ListDeployments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listdeploymentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListDeploymentsRequestListDeploymentsPaginateTypeDef]
    ) -> _PageIterator[ListDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListDeployments.html#GreengrassV2.Paginator.ListDeployments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listdeploymentspaginator)
        """


class ListEffectiveDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListEffectiveDeployments.html#GreengrassV2.Paginator.ListEffectiveDeployments)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listeffectivedeploymentspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef],
    ) -> _PageIterator[ListEffectiveDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListEffectiveDeployments.html#GreengrassV2.Paginator.ListEffectiveDeployments.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listeffectivedeploymentspaginator)
        """


class ListInstalledComponentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListInstalledComponents.html#GreengrassV2.Paginator.ListInstalledComponents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listinstalledcomponentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef]
    ) -> _PageIterator[ListInstalledComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/paginator/ListInstalledComponents.html#GreengrassV2.Paginator.ListInstalledComponents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_greengrassv2/paginators/#listinstalledcomponentspaginator)
        """
