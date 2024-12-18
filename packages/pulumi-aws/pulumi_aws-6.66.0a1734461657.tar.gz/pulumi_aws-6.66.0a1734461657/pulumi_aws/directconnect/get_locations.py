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
    'GetLocationsResult',
    'AwaitableGetLocationsResult',
    'get_locations',
    'get_locations_output',
]

@pulumi.output_type
class GetLocationsResult:
    """
    A collection of values returned by getLocations.
    """
    def __init__(__self__, id=None, location_codes=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location_codes and not isinstance(location_codes, list):
            raise TypeError("Expected argument 'location_codes' to be a list")
        pulumi.set(__self__, "location_codes", location_codes)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="locationCodes")
    def location_codes(self) -> Sequence[str]:
        """
        Code for the locations.
        """
        return pulumi.get(self, "location_codes")


class AwaitableGetLocationsResult(GetLocationsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLocationsResult(
            id=self.id,
            location_codes=self.location_codes)


def get_locations(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLocationsResult:
    """
    Retrieve information about the AWS Direct Connect locations in the current AWS Region.
    These are the locations that can be specified when configuring `directconnect.Connection` or `directconnect.LinkAggregationGroup` resources.

    > **Note:** This data source is different from the `directconnect_get_location` data source which retrieves information about a specific AWS Direct Connect location in the current AWS Region.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    available = aws.directconnect.get_locations()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:directconnect/getLocations:getLocations', __args__, opts=opts, typ=GetLocationsResult).value

    return AwaitableGetLocationsResult(
        id=pulumi.get(__ret__, 'id'),
        location_codes=pulumi.get(__ret__, 'location_codes'))
def get_locations_output(opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetLocationsResult]:
    """
    Retrieve information about the AWS Direct Connect locations in the current AWS Region.
    These are the locations that can be specified when configuring `directconnect.Connection` or `directconnect.LinkAggregationGroup` resources.

    > **Note:** This data source is different from the `directconnect_get_location` data source which retrieves information about a specific AWS Direct Connect location in the current AWS Region.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    available = aws.directconnect.get_locations()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:directconnect/getLocations:getLocations', __args__, opts=opts, typ=GetLocationsResult)
    return __ret__.apply(lambda __response__: GetLocationsResult(
        id=pulumi.get(__response__, 'id'),
        location_codes=pulumi.get(__response__, 'location_codes')))
