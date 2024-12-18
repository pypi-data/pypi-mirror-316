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

__all__ = [
    'GetLogGroupResult',
    'AwaitableGetLogGroupResult',
    'get_log_group',
    'get_log_group_output',
]

@pulumi.output_type
class GetLogGroupResult:
    """
    A collection of values returned by getLogGroup.
    """
    def __init__(__self__, arn=None, creation_time=None, id=None, kms_key_id=None, log_group_class=None, name=None, retention_in_days=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if creation_time and not isinstance(creation_time, int):
            raise TypeError("Expected argument 'creation_time' to be a int")
        pulumi.set(__self__, "creation_time", creation_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if log_group_class and not isinstance(log_group_class, str):
            raise TypeError("Expected argument 'log_group_class' to be a str")
        pulumi.set(__self__, "log_group_class", log_group_class)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if retention_in_days and not isinstance(retention_in_days, int):
            raise TypeError("Expected argument 'retention_in_days' to be a int")
        pulumi.set(__self__, "retention_in_days", retention_in_days)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Cloudwatch log group. Any `:*` suffix added by the API, denoting all CloudWatch Log Streams under the CloudWatch Log Group, is removed for greater compatibility with other AWS services that do not accept the suffix.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> int:
        """
        Creation time of the log group, expressed as the number of milliseconds after Jan 1, 1970 00:00:00 UTC.
        """
        return pulumi.get(self, "creation_time")

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
        ARN of the KMS Key to use when encrypting log data.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="logGroupClass")
    def log_group_class(self) -> str:
        """
        The log class of the log group.
        """
        return pulumi.get(self, "log_group_class")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="retentionInDays")
    def retention_in_days(self) -> int:
        """
        Number of days log events retained in the specified log group.
        """
        return pulumi.get(self, "retention_in_days")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetLogGroupResult(GetLogGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLogGroupResult(
            arn=self.arn,
            creation_time=self.creation_time,
            id=self.id,
            kms_key_id=self.kms_key_id,
            log_group_class=self.log_group_class,
            name=self.name,
            retention_in_days=self.retention_in_days,
            tags=self.tags)


def get_log_group(name: Optional[str] = None,
                  tags: Optional[Mapping[str, str]] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLogGroupResult:
    """
    Use this data source to get information about an AWS Cloudwatch Log Group

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudwatch.get_log_group(name="MyImportantLogs")
    ```


    :param str name: Name of the Cloudwatch log group
    :param Mapping[str, str] tags: Map of tags to assign to the resource.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cloudwatch/getLogGroup:getLogGroup', __args__, opts=opts, typ=GetLogGroupResult).value

    return AwaitableGetLogGroupResult(
        arn=pulumi.get(__ret__, 'arn'),
        creation_time=pulumi.get(__ret__, 'creation_time'),
        id=pulumi.get(__ret__, 'id'),
        kms_key_id=pulumi.get(__ret__, 'kms_key_id'),
        log_group_class=pulumi.get(__ret__, 'log_group_class'),
        name=pulumi.get(__ret__, 'name'),
        retention_in_days=pulumi.get(__ret__, 'retention_in_days'),
        tags=pulumi.get(__ret__, 'tags'))
def get_log_group_output(name: Optional[pulumi.Input[str]] = None,
                         tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                         opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetLogGroupResult]:
    """
    Use this data source to get information about an AWS Cloudwatch Log Group

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudwatch.get_log_group(name="MyImportantLogs")
    ```


    :param str name: Name of the Cloudwatch log group
    :param Mapping[str, str] tags: Map of tags to assign to the resource.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:cloudwatch/getLogGroup:getLogGroup', __args__, opts=opts, typ=GetLogGroupResult)
    return __ret__.apply(lambda __response__: GetLogGroupResult(
        arn=pulumi.get(__response__, 'arn'),
        creation_time=pulumi.get(__response__, 'creation_time'),
        id=pulumi.get(__response__, 'id'),
        kms_key_id=pulumi.get(__response__, 'kms_key_id'),
        log_group_class=pulumi.get(__response__, 'log_group_class'),
        name=pulumi.get(__response__, 'name'),
        retention_in_days=pulumi.get(__response__, 'retention_in_days'),
        tags=pulumi.get(__response__, 'tags')))
