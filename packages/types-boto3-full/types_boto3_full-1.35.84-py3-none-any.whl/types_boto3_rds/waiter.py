"""
Type annotations for rds service client waiters.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_rds.client import RDSClient
    from types_boto3_rds.waiter import (
        DBClusterAvailableWaiter,
        DBClusterDeletedWaiter,
        DBClusterSnapshotAvailableWaiter,
        DBClusterSnapshotDeletedWaiter,
        DBInstanceAvailableWaiter,
        DBInstanceDeletedWaiter,
        DBSnapshotAvailableWaiter,
        DBSnapshotCompletedWaiter,
        DBSnapshotDeletedWaiter,
        TenantDatabaseAvailableWaiter,
        TenantDatabaseDeletedWaiter,
    )

    session = Session()
    client: RDSClient = session.client("rds")

    db_cluster_available_waiter: DBClusterAvailableWaiter = client.get_waiter("db_cluster_available")
    db_cluster_deleted_waiter: DBClusterDeletedWaiter = client.get_waiter("db_cluster_deleted")
    db_cluster_snapshot_available_waiter: DBClusterSnapshotAvailableWaiter = client.get_waiter("db_cluster_snapshot_available")
    db_cluster_snapshot_deleted_waiter: DBClusterSnapshotDeletedWaiter = client.get_waiter("db_cluster_snapshot_deleted")
    db_instance_available_waiter: DBInstanceAvailableWaiter = client.get_waiter("db_instance_available")
    db_instance_deleted_waiter: DBInstanceDeletedWaiter = client.get_waiter("db_instance_deleted")
    db_snapshot_available_waiter: DBSnapshotAvailableWaiter = client.get_waiter("db_snapshot_available")
    db_snapshot_completed_waiter: DBSnapshotCompletedWaiter = client.get_waiter("db_snapshot_completed")
    db_snapshot_deleted_waiter: DBSnapshotDeletedWaiter = client.get_waiter("db_snapshot_deleted")
    tenant_database_available_waiter: TenantDatabaseAvailableWaiter = client.get_waiter("tenant_database_available")
    tenant_database_deleted_waiter: TenantDatabaseDeletedWaiter = client.get_waiter("tenant_database_deleted")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeDBClustersMessageDBClusterAvailableWaitTypeDef,
    DescribeDBClustersMessageDBClusterDeletedWaitTypeDef,
    DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef,
    DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef,
    DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef,
    DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef,
    DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef,
    DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef,
    DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef,
    DescribeTenantDatabasesMessageTenantDatabaseAvailableWaitTypeDef,
    DescribeTenantDatabasesMessageTenantDatabaseDeletedWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DBClusterAvailableWaiter",
    "DBClusterDeletedWaiter",
    "DBClusterSnapshotAvailableWaiter",
    "DBClusterSnapshotDeletedWaiter",
    "DBInstanceAvailableWaiter",
    "DBInstanceDeletedWaiter",
    "DBSnapshotAvailableWaiter",
    "DBSnapshotCompletedWaiter",
    "DBSnapshotDeletedWaiter",
    "TenantDatabaseAvailableWaiter",
    "TenantDatabaseDeletedWaiter",
)


class DBClusterAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterAvailable.html#RDS.Waiter.DBClusterAvailable)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbclusteravailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBClustersMessageDBClusterAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterAvailable.html#RDS.Waiter.DBClusterAvailable.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbclusteravailablewaiter)
        """


class DBClusterDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterDeleted.html#RDS.Waiter.DBClusterDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbclusterdeletedwaiter)
    """

    def wait(self, **kwargs: Unpack[DescribeDBClustersMessageDBClusterDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterDeleted.html#RDS.Waiter.DBClusterDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbclusterdeletedwaiter)
        """


class DBClusterSnapshotAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterSnapshotAvailable.html#RDS.Waiter.DBClusterSnapshotAvailable)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbclustersnapshotavailablewaiter)
    """

    def wait(
        self,
        **kwargs: Unpack[DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterSnapshotAvailable.html#RDS.Waiter.DBClusterSnapshotAvailable.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbclustersnapshotavailablewaiter)
        """


class DBClusterSnapshotDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterSnapshotDeleted.html#RDS.Waiter.DBClusterSnapshotDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbclustersnapshotdeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBClusterSnapshotDeleted.html#RDS.Waiter.DBClusterSnapshotDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbclustersnapshotdeletedwaiter)
        """


class DBInstanceAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBInstanceAvailable.html#RDS.Waiter.DBInstanceAvailable)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbinstanceavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBInstanceAvailable.html#RDS.Waiter.DBInstanceAvailable.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbinstanceavailablewaiter)
        """


class DBInstanceDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBInstanceDeleted.html#RDS.Waiter.DBInstanceDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbinstancedeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBInstanceDeleted.html#RDS.Waiter.DBInstanceDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbinstancedeletedwaiter)
        """


class DBSnapshotAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotAvailable.html#RDS.Waiter.DBSnapshotAvailable)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbsnapshotavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotAvailable.html#RDS.Waiter.DBSnapshotAvailable.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbsnapshotavailablewaiter)
        """


class DBSnapshotCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotCompleted.html#RDS.Waiter.DBSnapshotCompleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbsnapshotcompletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotCompleted.html#RDS.Waiter.DBSnapshotCompleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbsnapshotcompletedwaiter)
        """


class DBSnapshotDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotDeleted.html#RDS.Waiter.DBSnapshotDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbsnapshotdeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/DBSnapshotDeleted.html#RDS.Waiter.DBSnapshotDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#dbsnapshotdeletedwaiter)
        """


class TenantDatabaseAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/TenantDatabaseAvailable.html#RDS.Waiter.TenantDatabaseAvailable)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#tenantdatabaseavailablewaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeTenantDatabasesMessageTenantDatabaseAvailableWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/TenantDatabaseAvailable.html#RDS.Waiter.TenantDatabaseAvailable.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#tenantdatabaseavailablewaiter)
        """


class TenantDatabaseDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/TenantDatabaseDeleted.html#RDS.Waiter.TenantDatabaseDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#tenantdatabasedeletedwaiter)
    """

    def wait(
        self, **kwargs: Unpack[DescribeTenantDatabasesMessageTenantDatabaseDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/waiter/TenantDatabaseDeleted.html#RDS.Waiter.TenantDatabaseDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rds/waiters/#tenantdatabasedeletedwaiter)
        """
