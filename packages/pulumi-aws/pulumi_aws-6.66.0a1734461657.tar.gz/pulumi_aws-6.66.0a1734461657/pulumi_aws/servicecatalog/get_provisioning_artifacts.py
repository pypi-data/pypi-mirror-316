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
    'GetProvisioningArtifactsResult',
    'AwaitableGetProvisioningArtifactsResult',
    'get_provisioning_artifacts',
    'get_provisioning_artifacts_output',
]

@pulumi.output_type
class GetProvisioningArtifactsResult:
    """
    A collection of values returned by getProvisioningArtifacts.
    """
    def __init__(__self__, accept_language=None, id=None, product_id=None, provisioning_artifact_details=None):
        if accept_language and not isinstance(accept_language, str):
            raise TypeError("Expected argument 'accept_language' to be a str")
        pulumi.set(__self__, "accept_language", accept_language)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if product_id and not isinstance(product_id, str):
            raise TypeError("Expected argument 'product_id' to be a str")
        pulumi.set(__self__, "product_id", product_id)
        if provisioning_artifact_details and not isinstance(provisioning_artifact_details, list):
            raise TypeError("Expected argument 'provisioning_artifact_details' to be a list")
        pulumi.set(__self__, "provisioning_artifact_details", provisioning_artifact_details)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> Optional[str]:
        return pulumi.get(self, "accept_language")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> str:
        return pulumi.get(self, "product_id")

    @property
    @pulumi.getter(name="provisioningArtifactDetails")
    def provisioning_artifact_details(self) -> Sequence['outputs.GetProvisioningArtifactsProvisioningArtifactDetailResult']:
        """
        List with information about the provisioning artifacts. See details below.
        """
        return pulumi.get(self, "provisioning_artifact_details")


class AwaitableGetProvisioningArtifactsResult(GetProvisioningArtifactsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProvisioningArtifactsResult(
            accept_language=self.accept_language,
            id=self.id,
            product_id=self.product_id,
            provisioning_artifact_details=self.provisioning_artifact_details)


def get_provisioning_artifacts(accept_language: Optional[str] = None,
                               product_id: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProvisioningArtifactsResult:
    """
    Lists the provisioning artifacts for the specified product.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicecatalog.get_provisioning_artifacts(product_id="prod-yakog5pdriver")
    ```


    :param str accept_language: Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
    :param str product_id: Product identifier.
           
           The following arguments are optional:
    """
    __args__ = dict()
    __args__['acceptLanguage'] = accept_language
    __args__['productId'] = product_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:servicecatalog/getProvisioningArtifacts:getProvisioningArtifacts', __args__, opts=opts, typ=GetProvisioningArtifactsResult).value

    return AwaitableGetProvisioningArtifactsResult(
        accept_language=pulumi.get(__ret__, 'accept_language'),
        id=pulumi.get(__ret__, 'id'),
        product_id=pulumi.get(__ret__, 'product_id'),
        provisioning_artifact_details=pulumi.get(__ret__, 'provisioning_artifact_details'))
def get_provisioning_artifacts_output(accept_language: Optional[pulumi.Input[Optional[str]]] = None,
                                      product_id: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetProvisioningArtifactsResult]:
    """
    Lists the provisioning artifacts for the specified product.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicecatalog.get_provisioning_artifacts(product_id="prod-yakog5pdriver")
    ```


    :param str accept_language: Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
    :param str product_id: Product identifier.
           
           The following arguments are optional:
    """
    __args__ = dict()
    __args__['acceptLanguage'] = accept_language
    __args__['productId'] = product_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:servicecatalog/getProvisioningArtifacts:getProvisioningArtifacts', __args__, opts=opts, typ=GetProvisioningArtifactsResult)
    return __ret__.apply(lambda __response__: GetProvisioningArtifactsResult(
        accept_language=pulumi.get(__response__, 'accept_language'),
        id=pulumi.get(__response__, 'id'),
        product_id=pulumi.get(__response__, 'product_id'),
        provisioning_artifact_details=pulumi.get(__response__, 'provisioning_artifact_details')))
