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
    'GetInstanceProfilesResult',
    'AwaitableGetInstanceProfilesResult',
    'get_instance_profiles',
    'get_instance_profiles_output',
]

@pulumi.output_type
class GetInstanceProfilesResult:
    """
    A collection of values returned by getInstanceProfiles.
    """
    def __init__(__self__, arns=None, id=None, names=None, paths=None, role_name=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if paths and not isinstance(paths, list):
            raise TypeError("Expected argument 'paths' to be a list")
        pulumi.set(__self__, "paths", paths)
        if role_name and not isinstance(role_name, str):
            raise TypeError("Expected argument 'role_name' to be a str")
        pulumi.set(__self__, "role_name", role_name)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        Set of ARNs of instance profiles.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        Set of IAM instance profile names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter
    def paths(self) -> Sequence[str]:
        """
        Set of IAM instance profile paths.
        """
        return pulumi.get(self, "paths")

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> str:
        return pulumi.get(self, "role_name")


class AwaitableGetInstanceProfilesResult(GetInstanceProfilesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceProfilesResult(
            arns=self.arns,
            id=self.id,
            names=self.names,
            paths=self.paths,
            role_name=self.role_name)


def get_instance_profiles(role_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceProfilesResult:
    """
    This data source can be used to fetch information about all
    IAM instance profiles under a role. By using this data source, you can reference IAM
    instance profile properties without having to hard code ARNs as input.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.iam.get_instance_profiles(role_name="an_example_iam_role_name")
    ```


    :param str role_name: IAM role name.
    """
    __args__ = dict()
    __args__['roleName'] = role_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:iam/getInstanceProfiles:getInstanceProfiles', __args__, opts=opts, typ=GetInstanceProfilesResult).value

    return AwaitableGetInstanceProfilesResult(
        arns=pulumi.get(__ret__, 'arns'),
        id=pulumi.get(__ret__, 'id'),
        names=pulumi.get(__ret__, 'names'),
        paths=pulumi.get(__ret__, 'paths'),
        role_name=pulumi.get(__ret__, 'role_name'))
def get_instance_profiles_output(role_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetInstanceProfilesResult]:
    """
    This data source can be used to fetch information about all
    IAM instance profiles under a role. By using this data source, you can reference IAM
    instance profile properties without having to hard code ARNs as input.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.iam.get_instance_profiles(role_name="an_example_iam_role_name")
    ```


    :param str role_name: IAM role name.
    """
    __args__ = dict()
    __args__['roleName'] = role_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:iam/getInstanceProfiles:getInstanceProfiles', __args__, opts=opts, typ=GetInstanceProfilesResult)
    return __ret__.apply(lambda __response__: GetInstanceProfilesResult(
        arns=pulumi.get(__response__, 'arns'),
        id=pulumi.get(__response__, 'id'),
        names=pulumi.get(__response__, 'names'),
        paths=pulumi.get(__response__, 'paths'),
        role_name=pulumi.get(__response__, 'role_name')))
