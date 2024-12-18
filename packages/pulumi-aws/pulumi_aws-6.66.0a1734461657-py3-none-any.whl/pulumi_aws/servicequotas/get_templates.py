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
    'GetTemplatesResult',
    'AwaitableGetTemplatesResult',
    'get_templates',
    'get_templates_output',
]

@pulumi.output_type
class GetTemplatesResult:
    """
    A collection of values returned by getTemplates.
    """
    def __init__(__self__, id=None, region=None, templates=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if templates and not isinstance(templates, list):
            raise TypeError("Expected argument 'templates' to be a list")
        pulumi.set(__self__, "templates", templates)

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        AWS Region to which the template applies.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def templates(self) -> Optional[Sequence['outputs.GetTemplatesTemplateResult']]:
        """
        A list of quota increase templates for specified region. See `templates`.
        """
        return pulumi.get(self, "templates")


class AwaitableGetTemplatesResult(GetTemplatesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTemplatesResult(
            id=self.id,
            region=self.region,
            templates=self.templates)


def get_templates(region: Optional[str] = None,
                  templates: Optional[Sequence[Union['GetTemplatesTemplateArgs', 'GetTemplatesTemplateArgsDict']]] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTemplatesResult:
    """
    Data source for managing an AWS Service Quotas Templates.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicequotas.get_templates(region="us-east-1")
    ```


    :param str region: AWS Region to which the quota increases apply.
    :param Sequence[Union['GetTemplatesTemplateArgs', 'GetTemplatesTemplateArgsDict']] templates: A list of quota increase templates for specified region. See `templates`.
    """
    __args__ = dict()
    __args__['region'] = region
    __args__['templates'] = templates
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:servicequotas/getTemplates:getTemplates', __args__, opts=opts, typ=GetTemplatesResult).value

    return AwaitableGetTemplatesResult(
        id=pulumi.get(__ret__, 'id'),
        region=pulumi.get(__ret__, 'region'),
        templates=pulumi.get(__ret__, 'templates'))
def get_templates_output(region: Optional[pulumi.Input[str]] = None,
                         templates: Optional[pulumi.Input[Optional[Sequence[Union['GetTemplatesTemplateArgs', 'GetTemplatesTemplateArgsDict']]]]] = None,
                         opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetTemplatesResult]:
    """
    Data source for managing an AWS Service Quotas Templates.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicequotas.get_templates(region="us-east-1")
    ```


    :param str region: AWS Region to which the quota increases apply.
    :param Sequence[Union['GetTemplatesTemplateArgs', 'GetTemplatesTemplateArgsDict']] templates: A list of quota increase templates for specified region. See `templates`.
    """
    __args__ = dict()
    __args__['region'] = region
    __args__['templates'] = templates
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:servicequotas/getTemplates:getTemplates', __args__, opts=opts, typ=GetTemplatesResult)
    return __ret__.apply(lambda __response__: GetTemplatesResult(
        id=pulumi.get(__response__, 'id'),
        region=pulumi.get(__response__, 'region'),
        templates=pulumi.get(__response__, 'templates')))
