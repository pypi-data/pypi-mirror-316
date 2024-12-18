# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities
from . import outputs

__all__ = [
    'GetServerlessCacheResult',
    'AwaitableGetServerlessCacheResult',
    'get_serverless_cache',
    'get_serverless_cache_output',
]

@pulumi.output_type
class GetServerlessCacheResult:
    """
    A collection of values returned by getServerlessCache.
    """
    def __init__(__self__, arn=None, cache_usage_limits=None, create_time=None, daily_snapshot_time=None, description=None, endpoint=None, engine=None, full_engine_version=None, id=None, kms_key_id=None, major_engine_version=None, name=None, reader_endpoint=None, security_group_ids=None, snapshot_retention_limit=None, status=None, subnet_ids=None, user_group_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if cache_usage_limits and not isinstance(cache_usage_limits, dict):
            raise TypeError("Expected argument 'cache_usage_limits' to be a dict")
        pulumi.set(__self__, "cache_usage_limits", cache_usage_limits)
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if daily_snapshot_time and not isinstance(daily_snapshot_time, str):
            raise TypeError("Expected argument 'daily_snapshot_time' to be a str")
        pulumi.set(__self__, "daily_snapshot_time", daily_snapshot_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if endpoint and not isinstance(endpoint, dict):
            raise TypeError("Expected argument 'endpoint' to be a dict")
        pulumi.set(__self__, "endpoint", endpoint)
        if engine and not isinstance(engine, str):
            raise TypeError("Expected argument 'engine' to be a str")
        pulumi.set(__self__, "engine", engine)
        if full_engine_version and not isinstance(full_engine_version, str):
            raise TypeError("Expected argument 'full_engine_version' to be a str")
        pulumi.set(__self__, "full_engine_version", full_engine_version)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if major_engine_version and not isinstance(major_engine_version, str):
            raise TypeError("Expected argument 'major_engine_version' to be a str")
        pulumi.set(__self__, "major_engine_version", major_engine_version)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if reader_endpoint and not isinstance(reader_endpoint, dict):
            raise TypeError("Expected argument 'reader_endpoint' to be a dict")
        pulumi.set(__self__, "reader_endpoint", reader_endpoint)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if snapshot_retention_limit and not isinstance(snapshot_retention_limit, int):
            raise TypeError("Expected argument 'snapshot_retention_limit' to be a int")
        pulumi.set(__self__, "snapshot_retention_limit", snapshot_retention_limit)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError("Expected argument 'subnet_ids' to be a list")
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if user_group_id and not isinstance(user_group_id, str):
            raise TypeError("Expected argument 'user_group_id' to be a str")
        pulumi.set(__self__, "user_group_id", user_group_id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the serverless cache.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="cacheUsageLimits")
    def cache_usage_limits(self) -> 'outputs.GetServerlessCacheCacheUsageLimitsResult':
        """
        The cache usage limits for storage and ElastiCache Processing Units for the cache. See `cache_usage_limits` Block for details.
        """
        return pulumi.get(self, "cache_usage_limits")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        Timestamp of when the serverless cache was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="dailySnapshotTime")
    def daily_snapshot_time(self) -> str:
        """
        The daily time that snapshots will be created from the new serverless cache. Only available for engine types `"redis"` and `"valkey"`.
        """
        return pulumi.get(self, "daily_snapshot_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the serverless cache.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def endpoint(self) -> 'outputs.GetServerlessCacheEndpointResult':
        """
        Represents the information required for client programs to connect to the cache. See `endpoint` Block for details.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def engine(self) -> str:
        """
        Name of the cache engine.
        """
        return pulumi.get(self, "engine")

    @property
    @pulumi.getter(name="fullEngineVersion")
    def full_engine_version(self) -> str:
        """
        The name and version number of the engine the serverless cache is compatible with.
        """
        return pulumi.get(self, "full_engine_version")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> str:
        """
        ARN of the customer managed key for encrypting the data at rest.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="majorEngineVersion")
    def major_engine_version(self) -> str:
        """
        The version number of the engine the serverless cache is compatible with.
        """
        return pulumi.get(self, "major_engine_version")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="readerEndpoint")
    def reader_endpoint(self) -> 'outputs.GetServerlessCacheReaderEndpointResult':
        """
        Represents the information required for client programs to connect to a cache node. See `reader_endpoint` Block for details.
        """
        return pulumi.get(self, "reader_endpoint")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        A list of the one or more VPC security groups associated with the serverless cache.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> int:
        """
        The number of snapshots that will be retained for the serverless cache. Available for Redis only.
        """
        return pulumi.get(self, "snapshot_retention_limit")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The current status of the serverless cache.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        A list of the identifiers of the subnets where the VPC endpoint for the serverless cache are deployed.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="userGroupId")
    def user_group_id(self) -> str:
        """
        The identifier of the UserGroup associated with the serverless cache. Available for Redis only.
        """
        return pulumi.get(self, "user_group_id")


class AwaitableGetServerlessCacheResult(GetServerlessCacheResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerlessCacheResult(
            arn=self.arn,
            cache_usage_limits=self.cache_usage_limits,
            create_time=self.create_time,
            daily_snapshot_time=self.daily_snapshot_time,
            description=self.description,
            endpoint=self.endpoint,
            engine=self.engine,
            full_engine_version=self.full_engine_version,
            id=self.id,
            kms_key_id=self.kms_key_id,
            major_engine_version=self.major_engine_version,
            name=self.name,
            reader_endpoint=self.reader_endpoint,
            security_group_ids=self.security_group_ids,
            snapshot_retention_limit=self.snapshot_retention_limit,
            status=self.status,
            subnet_ids=self.subnet_ids,
            user_group_id=self.user_group_id)


def get_serverless_cache(name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerlessCacheResult:
    """
    Use this data source to get information about an ElastiCache Serverless Cache.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.elasticache.get_serverless_cache(name="example")
    ```


    :param str name: Identifier for the serverless cache.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:elasticache/getServerlessCache:getServerlessCache', __args__, opts=opts, typ=GetServerlessCacheResult).value

    return AwaitableGetServerlessCacheResult(
        arn=pulumi.get(__ret__, 'arn'),
        cache_usage_limits=pulumi.get(__ret__, 'cache_usage_limits'),
        create_time=pulumi.get(__ret__, 'create_time'),
        daily_snapshot_time=pulumi.get(__ret__, 'daily_snapshot_time'),
        description=pulumi.get(__ret__, 'description'),
        endpoint=pulumi.get(__ret__, 'endpoint'),
        engine=pulumi.get(__ret__, 'engine'),
        full_engine_version=pulumi.get(__ret__, 'full_engine_version'),
        id=pulumi.get(__ret__, 'id'),
        kms_key_id=pulumi.get(__ret__, 'kms_key_id'),
        major_engine_version=pulumi.get(__ret__, 'major_engine_version'),
        name=pulumi.get(__ret__, 'name'),
        reader_endpoint=pulumi.get(__ret__, 'reader_endpoint'),
        security_group_ids=pulumi.get(__ret__, 'security_group_ids'),
        snapshot_retention_limit=pulumi.get(__ret__, 'snapshot_retention_limit'),
        status=pulumi.get(__ret__, 'status'),
        subnet_ids=pulumi.get(__ret__, 'subnet_ids'),
        user_group_id=pulumi.get(__ret__, 'user_group_id'))
def get_serverless_cache_output(name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetServerlessCacheResult]:
    """
    Use this data source to get information about an ElastiCache Serverless Cache.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.elasticache.get_serverless_cache(name="example")
    ```


    :param str name: Identifier for the serverless cache.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:elasticache/getServerlessCache:getServerlessCache', __args__, opts=opts, typ=GetServerlessCacheResult)
    return __ret__.apply(lambda __response__: GetServerlessCacheResult(
        arn=pulumi.get(__response__, 'arn'),
        cache_usage_limits=pulumi.get(__response__, 'cache_usage_limits'),
        create_time=pulumi.get(__response__, 'create_time'),
        daily_snapshot_time=pulumi.get(__response__, 'daily_snapshot_time'),
        description=pulumi.get(__response__, 'description'),
        endpoint=pulumi.get(__response__, 'endpoint'),
        engine=pulumi.get(__response__, 'engine'),
        full_engine_version=pulumi.get(__response__, 'full_engine_version'),
        id=pulumi.get(__response__, 'id'),
        kms_key_id=pulumi.get(__response__, 'kms_key_id'),
        major_engine_version=pulumi.get(__response__, 'major_engine_version'),
        name=pulumi.get(__response__, 'name'),
        reader_endpoint=pulumi.get(__response__, 'reader_endpoint'),
        security_group_ids=pulumi.get(__response__, 'security_group_ids'),
        snapshot_retention_limit=pulumi.get(__response__, 'snapshot_retention_limit'),
        status=pulumi.get(__response__, 'status'),
        subnet_ids=pulumi.get(__response__, 'subnet_ids'),
        user_group_id=pulumi.get(__response__, 'user_group_id')))
