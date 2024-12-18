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
from ._inputs import *

__all__ = [
    'GetFrameworkResult',
    'AwaitableGetFrameworkResult',
    'get_framework',
    'get_framework_output',
]

@pulumi.output_type
class GetFrameworkResult:
    """
    A collection of values returned by getFramework.
    """
    def __init__(__self__, arn=None, compliance_type=None, control_sets=None, description=None, framework_type=None, id=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if compliance_type and not isinstance(compliance_type, str):
            raise TypeError("Expected argument 'compliance_type' to be a str")
        pulumi.set(__self__, "compliance_type", compliance_type)
        if control_sets and not isinstance(control_sets, list):
            raise TypeError("Expected argument 'control_sets' to be a list")
        pulumi.set(__self__, "control_sets", control_sets)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if framework_type and not isinstance(framework_type, str):
            raise TypeError("Expected argument 'framework_type' to be a str")
        pulumi.set(__self__, "framework_type", framework_type)
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
    @pulumi.getter(name="complianceType")
    def compliance_type(self) -> str:
        return pulumi.get(self, "compliance_type")

    @property
    @pulumi.getter(name="controlSets")
    def control_sets(self) -> Optional[Sequence['outputs.GetFrameworkControlSetResult']]:
        return pulumi.get(self, "control_sets")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="frameworkType")
    def framework_type(self) -> str:
        return pulumi.get(self, "framework_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetFrameworkResult(GetFrameworkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFrameworkResult(
            arn=self.arn,
            compliance_type=self.compliance_type,
            control_sets=self.control_sets,
            description=self.description,
            framework_type=self.framework_type,
            id=self.id,
            name=self.name,
            tags=self.tags)


def get_framework(control_sets: Optional[Sequence[Union['GetFrameworkControlSetArgs', 'GetFrameworkControlSetArgsDict']]] = None,
                  framework_type: Optional[str] = None,
                  name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFrameworkResult:
    """
    Data source for managing an AWS Audit Manager Framework.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.auditmanager.get_framework(name="Essential Eight",
        framework_type="Standard")
    ```


    :param str name: Name of the framework.
    """
    __args__ = dict()
    __args__['controlSets'] = control_sets
    __args__['frameworkType'] = framework_type
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:auditmanager/getFramework:getFramework', __args__, opts=opts, typ=GetFrameworkResult).value

    return AwaitableGetFrameworkResult(
        arn=pulumi.get(__ret__, 'arn'),
        compliance_type=pulumi.get(__ret__, 'compliance_type'),
        control_sets=pulumi.get(__ret__, 'control_sets'),
        description=pulumi.get(__ret__, 'description'),
        framework_type=pulumi.get(__ret__, 'framework_type'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_framework_output(control_sets: Optional[pulumi.Input[Optional[Sequence[Union['GetFrameworkControlSetArgs', 'GetFrameworkControlSetArgsDict']]]]] = None,
                         framework_type: Optional[pulumi.Input[str]] = None,
                         name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetFrameworkResult]:
    """
    Data source for managing an AWS Audit Manager Framework.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.auditmanager.get_framework(name="Essential Eight",
        framework_type="Standard")
    ```


    :param str name: Name of the framework.
    """
    __args__ = dict()
    __args__['controlSets'] = control_sets
    __args__['frameworkType'] = framework_type
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:auditmanager/getFramework:getFramework', __args__, opts=opts, typ=GetFrameworkResult)
    return __ret__.apply(lambda __response__: GetFrameworkResult(
        arn=pulumi.get(__response__, 'arn'),
        compliance_type=pulumi.get(__response__, 'compliance_type'),
        control_sets=pulumi.get(__response__, 'control_sets'),
        description=pulumi.get(__response__, 'description'),
        framework_type=pulumi.get(__response__, 'framework_type'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
