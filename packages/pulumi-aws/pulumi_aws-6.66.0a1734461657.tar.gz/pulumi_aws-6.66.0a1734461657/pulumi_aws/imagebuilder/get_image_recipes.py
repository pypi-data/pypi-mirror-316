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
    'GetImageRecipesResult',
    'AwaitableGetImageRecipesResult',
    'get_image_recipes',
    'get_image_recipes_output',
]

@pulumi.output_type
class GetImageRecipesResult:
    """
    A collection of values returned by getImageRecipes.
    """
    def __init__(__self__, arns=None, filters=None, id=None, names=None, owner=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if owner and not isinstance(owner, str):
            raise TypeError("Expected argument 'owner' to be a str")
        pulumi.set(__self__, "owner", owner)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        Set of ARNs of the matched Image Builder Image Recipes.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetImageRecipesFilterResult']]:
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
    def names(self) -> Sequence[str]:
        """
        Set of names of the matched Image Builder Image Recipes.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter
    def owner(self) -> Optional[str]:
        return pulumi.get(self, "owner")


class AwaitableGetImageRecipesResult(GetImageRecipesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetImageRecipesResult(
            arns=self.arns,
            filters=self.filters,
            id=self.id,
            names=self.names,
            owner=self.owner)


def get_image_recipes(filters: Optional[Sequence[Union['GetImageRecipesFilterArgs', 'GetImageRecipesFilterArgsDict']]] = None,
                      owner: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetImageRecipesResult:
    """
    Use this data source to get the ARNs and names of Image Builder Image Recipes matching the specified criteria.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.imagebuilder.get_image_recipes(owner="Self",
        filters=[{
            "name": "platform",
            "values": ["Linux"],
        }])
    ```


    :param Sequence[Union['GetImageRecipesFilterArgs', 'GetImageRecipesFilterArgsDict']] filters: Configuration block(s) for filtering. Detailed below.
    :param str owner: Owner of the image recipes. Valid values are `Self`, `Shared`, `Amazon` and `ThirdParty`. Defaults to `Self`.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['owner'] = owner
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:imagebuilder/getImageRecipes:getImageRecipes', __args__, opts=opts, typ=GetImageRecipesResult).value

    return AwaitableGetImageRecipesResult(
        arns=pulumi.get(__ret__, 'arns'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        names=pulumi.get(__ret__, 'names'),
        owner=pulumi.get(__ret__, 'owner'))
def get_image_recipes_output(filters: Optional[pulumi.Input[Optional[Sequence[Union['GetImageRecipesFilterArgs', 'GetImageRecipesFilterArgsDict']]]]] = None,
                             owner: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetImageRecipesResult]:
    """
    Use this data source to get the ARNs and names of Image Builder Image Recipes matching the specified criteria.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.imagebuilder.get_image_recipes(owner="Self",
        filters=[{
            "name": "platform",
            "values": ["Linux"],
        }])
    ```


    :param Sequence[Union['GetImageRecipesFilterArgs', 'GetImageRecipesFilterArgsDict']] filters: Configuration block(s) for filtering. Detailed below.
    :param str owner: Owner of the image recipes. Valid values are `Self`, `Shared`, `Amazon` and `ThirdParty`. Defaults to `Self`.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['owner'] = owner
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:imagebuilder/getImageRecipes:getImageRecipes', __args__, opts=opts, typ=GetImageRecipesResult)
    return __ret__.apply(lambda __response__: GetImageRecipesResult(
        arns=pulumi.get(__response__, 'arns'),
        filters=pulumi.get(__response__, 'filters'),
        id=pulumi.get(__response__, 'id'),
        names=pulumi.get(__response__, 'names'),
        owner=pulumi.get(__response__, 'owner')))
