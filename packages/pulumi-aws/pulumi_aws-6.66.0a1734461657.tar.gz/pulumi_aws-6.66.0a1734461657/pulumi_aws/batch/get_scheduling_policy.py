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
    'GetSchedulingPolicyResult',
    'AwaitableGetSchedulingPolicyResult',
    'get_scheduling_policy',
    'get_scheduling_policy_output',
]

@pulumi.output_type
class GetSchedulingPolicyResult:
    """
    A collection of values returned by getSchedulingPolicy.
    """
    def __init__(__self__, arn=None, fair_share_policies=None, id=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if fair_share_policies and not isinstance(fair_share_policies, list):
            raise TypeError("Expected argument 'fair_share_policies' to be a list")
        pulumi.set(__self__, "fair_share_policies", fair_share_policies)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="fairSharePolicies")
    def fair_share_policies(self) -> Sequence['outputs.GetSchedulingPolicyFairSharePolicyResult']:
        return pulumi.get(self, "fair_share_policies")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the scheduling policy.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Key-value map of resource tags
        """
        return pulumi.get(self, "tags")


class AwaitableGetSchedulingPolicyResult(GetSchedulingPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSchedulingPolicyResult(
            arn=self.arn,
            fair_share_policies=self.fair_share_policies,
            id=self.id,
            name=self.name,
            tags=self.tags)


def get_scheduling_policy(arn: Optional[str] = None,
                          tags: Optional[Mapping[str, str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSchedulingPolicyResult:
    """
    The Batch Scheduling Policy data source allows access to details of a specific Scheduling Policy within AWS Batch.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.batch.get_scheduling_policy(arn="arn:aws:batch:us-east-1:012345678910:scheduling-policy/example")
    ```


    :param str arn: ARN of the scheduling policy.
    :param Mapping[str, str] tags: Key-value map of resource tags
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:batch/getSchedulingPolicy:getSchedulingPolicy', __args__, opts=opts, typ=GetSchedulingPolicyResult).value

    return AwaitableGetSchedulingPolicyResult(
        arn=pulumi.get(__ret__, 'arn'),
        fair_share_policies=pulumi.get(__ret__, 'fair_share_policies'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_scheduling_policy_output(arn: Optional[pulumi.Input[str]] = None,
                                 tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                 opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSchedulingPolicyResult]:
    """
    The Batch Scheduling Policy data source allows access to details of a specific Scheduling Policy within AWS Batch.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.batch.get_scheduling_policy(arn="arn:aws:batch:us-east-1:012345678910:scheduling-policy/example")
    ```


    :param str arn: ARN of the scheduling policy.
    :param Mapping[str, str] tags: Key-value map of resource tags
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['tags'] = tags
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:batch/getSchedulingPolicy:getSchedulingPolicy', __args__, opts=opts, typ=GetSchedulingPolicyResult)
    return __ret__.apply(lambda __response__: GetSchedulingPolicyResult(
        arn=pulumi.get(__response__, 'arn'),
        fair_share_policies=pulumi.get(__response__, 'fair_share_policies'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
