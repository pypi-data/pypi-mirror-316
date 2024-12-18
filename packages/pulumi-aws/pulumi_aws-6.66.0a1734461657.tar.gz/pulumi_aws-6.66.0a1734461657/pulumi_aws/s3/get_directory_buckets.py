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
    'GetDirectoryBucketsResult',
    'AwaitableGetDirectoryBucketsResult',
    'get_directory_buckets',
    'get_directory_buckets_output',
]

@pulumi.output_type
class GetDirectoryBucketsResult:
    """
    A collection of values returned by getDirectoryBuckets.
    """
    def __init__(__self__, arns=None, buckets=None, id=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if buckets and not isinstance(buckets, list):
            raise TypeError("Expected argument 'buckets' to be a list")
        pulumi.set(__self__, "buckets", buckets)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        Bucket ARNs.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def buckets(self) -> Sequence[str]:
        """
        Buckets names.
        """
        return pulumi.get(self, "buckets")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")


class AwaitableGetDirectoryBucketsResult(GetDirectoryBucketsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDirectoryBucketsResult(
            arns=self.arns,
            buckets=self.buckets,
            id=self.id)


def get_directory_buckets(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDirectoryBucketsResult:
    """
    Lists Amazon S3 Express directory buckets.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.s3.get_directory_buckets()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:s3/getDirectoryBuckets:getDirectoryBuckets', __args__, opts=opts, typ=GetDirectoryBucketsResult).value

    return AwaitableGetDirectoryBucketsResult(
        arns=pulumi.get(__ret__, 'arns'),
        buckets=pulumi.get(__ret__, 'buckets'),
        id=pulumi.get(__ret__, 'id'))
def get_directory_buckets_output(opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetDirectoryBucketsResult]:
    """
    Lists Amazon S3 Express directory buckets.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.s3.get_directory_buckets()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:s3/getDirectoryBuckets:getDirectoryBuckets', __args__, opts=opts, typ=GetDirectoryBucketsResult)
    return __ret__.apply(lambda __response__: GetDirectoryBucketsResult(
        arns=pulumi.get(__response__, 'arns'),
        buckets=pulumi.get(__response__, 'buckets'),
        id=pulumi.get(__response__, 'id')))
