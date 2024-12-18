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
    'GetNetworkInterfacesResult',
    'AwaitableGetNetworkInterfacesResult',
    'get_network_interfaces',
    'get_network_interfaces_output',
]

@pulumi.output_type
class GetNetworkInterfacesResult:
    """
    A collection of values returned by getNetworkInterfaces.
    """
    def __init__(__self__, filters=None, id=None, ids=None, tags=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetNetworkInterfacesFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        List of all the network interface ids found.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetNetworkInterfacesResult(GetNetworkInterfacesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkInterfacesResult(
            filters=self.filters,
            id=self.id,
            ids=self.ids,
            tags=self.tags)


def get_network_interfaces(filters: Optional[Sequence[Union['GetNetworkInterfacesFilterArgs', 'GetNetworkInterfacesFilterArgsDict']]] = None,
                           tags: Optional[Mapping[str, str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkInterfacesResult:
    """
    ## Example Usage

    The following shows outputting all network interface ids in a region.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_network_interfaces()
    pulumi.export("example", example.ids)
    ```

    The following example retrieves a list of all network interface ids with a custom tag of `Name` set to a value of `test`.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_network_interfaces(tags={
        "Name": "test",
    })
    pulumi.export("example1", example.ids)
    ```

    The following example retrieves a network interface ids which associated
    with specific subnet.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_network_interfaces(filters=[{
        "name": "subnet-id",
        "values": [test["id"]],
    }])
    pulumi.export("example", example.ids)
    ```


    :param Sequence[Union['GetNetworkInterfacesFilterArgs', 'GetNetworkInterfacesFilterArgsDict']] filters: Custom filter block as described below.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired network interfaces.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getNetworkInterfaces:getNetworkInterfaces', __args__, opts=opts, typ=GetNetworkInterfacesResult).value

    return AwaitableGetNetworkInterfacesResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        tags=pulumi.get(__ret__, 'tags'))
def get_network_interfaces_output(filters: Optional[pulumi.Input[Optional[Sequence[Union['GetNetworkInterfacesFilterArgs', 'GetNetworkInterfacesFilterArgsDict']]]]] = None,
                                  tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetNetworkInterfacesResult]:
    """
    ## Example Usage

    The following shows outputting all network interface ids in a region.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_network_interfaces()
    pulumi.export("example", example.ids)
    ```

    The following example retrieves a list of all network interface ids with a custom tag of `Name` set to a value of `test`.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_network_interfaces(tags={
        "Name": "test",
    })
    pulumi.export("example1", example.ids)
    ```

    The following example retrieves a network interface ids which associated
    with specific subnet.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_network_interfaces(filters=[{
        "name": "subnet-id",
        "values": [test["id"]],
    }])
    pulumi.export("example", example.ids)
    ```


    :param Sequence[Union['GetNetworkInterfacesFilterArgs', 'GetNetworkInterfacesFilterArgsDict']] filters: Custom filter block as described below.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired network interfaces.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:ec2/getNetworkInterfaces:getNetworkInterfaces', __args__, opts=opts, typ=GetNetworkInterfacesResult)
    return __ret__.apply(lambda __response__: GetNetworkInterfacesResult(
        filters=pulumi.get(__response__, 'filters'),
        id=pulumi.get(__response__, 'id'),
        ids=pulumi.get(__response__, 'ids'),
        tags=pulumi.get(__response__, 'tags')))
