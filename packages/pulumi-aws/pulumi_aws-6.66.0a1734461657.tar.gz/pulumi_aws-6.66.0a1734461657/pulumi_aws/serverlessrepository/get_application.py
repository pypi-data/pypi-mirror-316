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
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
    'get_application_output',
]

@pulumi.output_type
class GetApplicationResult:
    """
    A collection of values returned by getApplication.
    """
    def __init__(__self__, application_id=None, id=None, name=None, required_capabilities=None, semantic_version=None, source_code_url=None, template_url=None):
        if application_id and not isinstance(application_id, str):
            raise TypeError("Expected argument 'application_id' to be a str")
        pulumi.set(__self__, "application_id", application_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if required_capabilities and not isinstance(required_capabilities, list):
            raise TypeError("Expected argument 'required_capabilities' to be a list")
        pulumi.set(__self__, "required_capabilities", required_capabilities)
        if semantic_version and not isinstance(semantic_version, str):
            raise TypeError("Expected argument 'semantic_version' to be a str")
        pulumi.set(__self__, "semantic_version", semantic_version)
        if source_code_url and not isinstance(source_code_url, str):
            raise TypeError("Expected argument 'source_code_url' to be a str")
        pulumi.set(__self__, "source_code_url", source_code_url)
        if template_url and not isinstance(template_url, str):
            raise TypeError("Expected argument 'template_url' to be a str")
        pulumi.set(__self__, "template_url", template_url)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> str:
        """
        ARN of the application.
        """
        return pulumi.get(self, "application_id")

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
        Name of the application.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requiredCapabilities")
    def required_capabilities(self) -> Sequence[str]:
        """
        A list of capabilities describing the permissions needed to deploy the application.
        """
        return pulumi.get(self, "required_capabilities")

    @property
    @pulumi.getter(name="semanticVersion")
    def semantic_version(self) -> str:
        return pulumi.get(self, "semantic_version")

    @property
    @pulumi.getter(name="sourceCodeUrl")
    def source_code_url(self) -> str:
        """
        URL pointing to the source code of the application version.
        """
        return pulumi.get(self, "source_code_url")

    @property
    @pulumi.getter(name="templateUrl")
    def template_url(self) -> str:
        """
        URL pointing to the Cloud Formation template for the application version.
        """
        return pulumi.get(self, "template_url")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            application_id=self.application_id,
            id=self.id,
            name=self.name,
            required_capabilities=self.required_capabilities,
            semantic_version=self.semantic_version,
            source_code_url=self.source_code_url,
            template_url=self.template_url)


def get_application(application_id: Optional[str] = None,
                    semantic_version: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    Use this data source to get information about an AWS Serverless Application Repository application. For example, this can be used to determine the required `capabilities` for an application.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.serverlessrepository.get_application(application_id="arn:aws:serverlessrepo:us-east-1:123456789012:applications/ExampleApplication")
    example_cloud_formation_stack = aws.serverlessrepository.CloudFormationStack("example",
        name="Example",
        application_id=example.application_id,
        semantic_version=example.semantic_version,
        capabilities=example.required_capabilities)
    ```


    :param str application_id: ARN of the application.
    :param str semantic_version: Requested version of the application. By default, retrieves the latest version.
    """
    __args__ = dict()
    __args__['applicationId'] = application_id
    __args__['semanticVersion'] = semantic_version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:serverlessrepository/getApplication:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        application_id=pulumi.get(__ret__, 'application_id'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        required_capabilities=pulumi.get(__ret__, 'required_capabilities'),
        semantic_version=pulumi.get(__ret__, 'semantic_version'),
        source_code_url=pulumi.get(__ret__, 'source_code_url'),
        template_url=pulumi.get(__ret__, 'template_url'))
def get_application_output(application_id: Optional[pulumi.Input[str]] = None,
                           semantic_version: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetApplicationResult]:
    """
    Use this data source to get information about an AWS Serverless Application Repository application. For example, this can be used to determine the required `capabilities` for an application.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.serverlessrepository.get_application(application_id="arn:aws:serverlessrepo:us-east-1:123456789012:applications/ExampleApplication")
    example_cloud_formation_stack = aws.serverlessrepository.CloudFormationStack("example",
        name="Example",
        application_id=example.application_id,
        semantic_version=example.semantic_version,
        capabilities=example.required_capabilities)
    ```


    :param str application_id: ARN of the application.
    :param str semantic_version: Requested version of the application. By default, retrieves the latest version.
    """
    __args__ = dict()
    __args__['applicationId'] = application_id
    __args__['semanticVersion'] = semantic_version
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:serverlessrepository/getApplication:getApplication', __args__, opts=opts, typ=GetApplicationResult)
    return __ret__.apply(lambda __response__: GetApplicationResult(
        application_id=pulumi.get(__response__, 'application_id'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        required_capabilities=pulumi.get(__response__, 'required_capabilities'),
        semantic_version=pulumi.get(__response__, 'semantic_version'),
        source_code_url=pulumi.get(__response__, 'source_code_url'),
        template_url=pulumi.get(__response__, 'template_url')))
