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
    'GetProductResult',
    'AwaitableGetProductResult',
    'get_product',
    'get_product_output',
]

@pulumi.output_type
class GetProductResult:
    """
    A collection of values returned by getProduct.
    """
    def __init__(__self__, accept_language=None, arn=None, created_time=None, description=None, distributor=None, has_default_path=None, id=None, name=None, owner=None, status=None, support_description=None, support_email=None, support_url=None, tags=None, type=None):
        if accept_language and not isinstance(accept_language, str):
            raise TypeError("Expected argument 'accept_language' to be a str")
        pulumi.set(__self__, "accept_language", accept_language)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_time and not isinstance(created_time, str):
            raise TypeError("Expected argument 'created_time' to be a str")
        pulumi.set(__self__, "created_time", created_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if distributor and not isinstance(distributor, str):
            raise TypeError("Expected argument 'distributor' to be a str")
        pulumi.set(__self__, "distributor", distributor)
        if has_default_path and not isinstance(has_default_path, bool):
            raise TypeError("Expected argument 'has_default_path' to be a bool")
        pulumi.set(__self__, "has_default_path", has_default_path)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if owner and not isinstance(owner, str):
            raise TypeError("Expected argument 'owner' to be a str")
        pulumi.set(__self__, "owner", owner)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if support_description and not isinstance(support_description, str):
            raise TypeError("Expected argument 'support_description' to be a str")
        pulumi.set(__self__, "support_description", support_description)
        if support_email and not isinstance(support_email, str):
            raise TypeError("Expected argument 'support_email' to be a str")
        pulumi.set(__self__, "support_email", support_email)
        if support_url and not isinstance(support_url, str):
            raise TypeError("Expected argument 'support_url' to be a str")
        pulumi.set(__self__, "support_url", support_url)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> Optional[str]:
        return pulumi.get(self, "accept_language")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the product.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> str:
        """
        Time when the product was created.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the product.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def distributor(self) -> str:
        """
        Vendor of the product.
        """
        return pulumi.get(self, "distributor")

    @property
    @pulumi.getter(name="hasDefaultPath")
    def has_default_path(self) -> bool:
        """
        Whether the product has a default path.
        """
        return pulumi.get(self, "has_default_path")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the product.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> str:
        """
        Owner of the product.
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the product.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="supportDescription")
    def support_description(self) -> str:
        """
        Field that provides support information about the product.
        """
        return pulumi.get(self, "support_description")

    @property
    @pulumi.getter(name="supportEmail")
    def support_email(self) -> str:
        """
        Contact email for product support.
        """
        return pulumi.get(self, "support_email")

    @property
    @pulumi.getter(name="supportUrl")
    def support_url(self) -> str:
        """
        Contact URL for product support.
        """
        return pulumi.get(self, "support_url")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Tags applied to the product.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of product.
        """
        return pulumi.get(self, "type")


class AwaitableGetProductResult(GetProductResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProductResult(
            accept_language=self.accept_language,
            arn=self.arn,
            created_time=self.created_time,
            description=self.description,
            distributor=self.distributor,
            has_default_path=self.has_default_path,
            id=self.id,
            name=self.name,
            owner=self.owner,
            status=self.status,
            support_description=self.support_description,
            support_email=self.support_email,
            support_url=self.support_url,
            tags=self.tags,
            type=self.type)


def get_product(accept_language: Optional[str] = None,
                id: Optional[str] = None,
                tags: Optional[Mapping[str, str]] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProductResult:
    """
    Use this data source to retrieve information about a Service Catalog product.

    > **NOTE:** A "provisioning artifact" is also known as a "version," and a "distributor" is also known as a "vendor."

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicecatalog.get_product(id="prod-dnigbtea24ste")
    ```


    :param str accept_language: Language code. Valid values are `en` (English), `jp` (Japanese), `zh` (Chinese). The default value is `en`.
    :param str id: ID of the product.
           
           The following arguments are optional:
    :param Mapping[str, str] tags: Tags applied to the product.
    """
    __args__ = dict()
    __args__['acceptLanguage'] = accept_language
    __args__['id'] = id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:servicecatalog/getProduct:getProduct', __args__, opts=opts, typ=GetProductResult).value

    return AwaitableGetProductResult(
        accept_language=pulumi.get(__ret__, 'accept_language'),
        arn=pulumi.get(__ret__, 'arn'),
        created_time=pulumi.get(__ret__, 'created_time'),
        description=pulumi.get(__ret__, 'description'),
        distributor=pulumi.get(__ret__, 'distributor'),
        has_default_path=pulumi.get(__ret__, 'has_default_path'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        owner=pulumi.get(__ret__, 'owner'),
        status=pulumi.get(__ret__, 'status'),
        support_description=pulumi.get(__ret__, 'support_description'),
        support_email=pulumi.get(__ret__, 'support_email'),
        support_url=pulumi.get(__ret__, 'support_url'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'))
def get_product_output(accept_language: Optional[pulumi.Input[Optional[str]]] = None,
                       id: Optional[pulumi.Input[str]] = None,
                       tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                       opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetProductResult]:
    """
    Use this data source to retrieve information about a Service Catalog product.

    > **NOTE:** A "provisioning artifact" is also known as a "version," and a "distributor" is also known as a "vendor."

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicecatalog.get_product(id="prod-dnigbtea24ste")
    ```


    :param str accept_language: Language code. Valid values are `en` (English), `jp` (Japanese), `zh` (Chinese). The default value is `en`.
    :param str id: ID of the product.
           
           The following arguments are optional:
    :param Mapping[str, str] tags: Tags applied to the product.
    """
    __args__ = dict()
    __args__['acceptLanguage'] = accept_language
    __args__['id'] = id
    __args__['tags'] = tags
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:servicecatalog/getProduct:getProduct', __args__, opts=opts, typ=GetProductResult)
    return __ret__.apply(lambda __response__: GetProductResult(
        accept_language=pulumi.get(__response__, 'accept_language'),
        arn=pulumi.get(__response__, 'arn'),
        created_time=pulumi.get(__response__, 'created_time'),
        description=pulumi.get(__response__, 'description'),
        distributor=pulumi.get(__response__, 'distributor'),
        has_default_path=pulumi.get(__response__, 'has_default_path'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        owner=pulumi.get(__response__, 'owner'),
        status=pulumi.get(__response__, 'status'),
        support_description=pulumi.get(__response__, 'support_description'),
        support_email=pulumi.get(__response__, 'support_email'),
        support_url=pulumi.get(__response__, 'support_url'),
        tags=pulumi.get(__response__, 'tags'),
        type=pulumi.get(__response__, 'type')))
