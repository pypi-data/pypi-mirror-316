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

__all__ = ['OriginAccessControlArgs', 'OriginAccessControl']

@pulumi.input_type
class OriginAccessControlArgs:
    def __init__(__self__, *,
                 origin_access_control_origin_type: pulumi.Input[str],
                 signing_behavior: pulumi.Input[str],
                 signing_protocol: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OriginAccessControl resource.
        :param pulumi.Input[str] origin_access_control_origin_type: The type of origin that this Origin Access Control is for. Valid values are `lambda`, `mediapackagev2`, `mediastore`, and `s3`.
        :param pulumi.Input[str] signing_behavior: Specifies which requests CloudFront signs. Specify `always` for the most common use case. Allowed values: `always`, `never`, and `no-override`.
        :param pulumi.Input[str] signing_protocol: Determines how CloudFront signs (authenticates) requests. The only valid value is `sigv4`.
        :param pulumi.Input[str] description: The description of the Origin Access Control. Defaults to "Managed by Pulumi" if omitted.
        :param pulumi.Input[str] name: A name that identifies the Origin Access Control.
        """
        pulumi.set(__self__, "origin_access_control_origin_type", origin_access_control_origin_type)
        pulumi.set(__self__, "signing_behavior", signing_behavior)
        pulumi.set(__self__, "signing_protocol", signing_protocol)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="originAccessControlOriginType")
    def origin_access_control_origin_type(self) -> pulumi.Input[str]:
        """
        The type of origin that this Origin Access Control is for. Valid values are `lambda`, `mediapackagev2`, `mediastore`, and `s3`.
        """
        return pulumi.get(self, "origin_access_control_origin_type")

    @origin_access_control_origin_type.setter
    def origin_access_control_origin_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "origin_access_control_origin_type", value)

    @property
    @pulumi.getter(name="signingBehavior")
    def signing_behavior(self) -> pulumi.Input[str]:
        """
        Specifies which requests CloudFront signs. Specify `always` for the most common use case. Allowed values: `always`, `never`, and `no-override`.
        """
        return pulumi.get(self, "signing_behavior")

    @signing_behavior.setter
    def signing_behavior(self, value: pulumi.Input[str]):
        pulumi.set(self, "signing_behavior", value)

    @property
    @pulumi.getter(name="signingProtocol")
    def signing_protocol(self) -> pulumi.Input[str]:
        """
        Determines how CloudFront signs (authenticates) requests. The only valid value is `sigv4`.
        """
        return pulumi.get(self, "signing_protocol")

    @signing_protocol.setter
    def signing_protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "signing_protocol", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Origin Access Control. Defaults to "Managed by Pulumi" if omitted.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name that identifies the Origin Access Control.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _OriginAccessControlState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 origin_access_control_origin_type: Optional[pulumi.Input[str]] = None,
                 signing_behavior: Optional[pulumi.Input[str]] = None,
                 signing_protocol: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OriginAccessControl resources.
        :param pulumi.Input[str] description: The description of the Origin Access Control. Defaults to "Managed by Pulumi" if omitted.
        :param pulumi.Input[str] etag: The current version of this Origin Access Control.
        :param pulumi.Input[str] name: A name that identifies the Origin Access Control.
        :param pulumi.Input[str] origin_access_control_origin_type: The type of origin that this Origin Access Control is for. Valid values are `lambda`, `mediapackagev2`, `mediastore`, and `s3`.
        :param pulumi.Input[str] signing_behavior: Specifies which requests CloudFront signs. Specify `always` for the most common use case. Allowed values: `always`, `never`, and `no-override`.
        :param pulumi.Input[str] signing_protocol: Determines how CloudFront signs (authenticates) requests. The only valid value is `sigv4`.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if origin_access_control_origin_type is not None:
            pulumi.set(__self__, "origin_access_control_origin_type", origin_access_control_origin_type)
        if signing_behavior is not None:
            pulumi.set(__self__, "signing_behavior", signing_behavior)
        if signing_protocol is not None:
            pulumi.set(__self__, "signing_protocol", signing_protocol)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Origin Access Control. Defaults to "Managed by Pulumi" if omitted.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        The current version of this Origin Access Control.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name that identifies the Origin Access Control.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="originAccessControlOriginType")
    def origin_access_control_origin_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of origin that this Origin Access Control is for. Valid values are `lambda`, `mediapackagev2`, `mediastore`, and `s3`.
        """
        return pulumi.get(self, "origin_access_control_origin_type")

    @origin_access_control_origin_type.setter
    def origin_access_control_origin_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "origin_access_control_origin_type", value)

    @property
    @pulumi.getter(name="signingBehavior")
    def signing_behavior(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies which requests CloudFront signs. Specify `always` for the most common use case. Allowed values: `always`, `never`, and `no-override`.
        """
        return pulumi.get(self, "signing_behavior")

    @signing_behavior.setter
    def signing_behavior(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "signing_behavior", value)

    @property
    @pulumi.getter(name="signingProtocol")
    def signing_protocol(self) -> Optional[pulumi.Input[str]]:
        """
        Determines how CloudFront signs (authenticates) requests. The only valid value is `sigv4`.
        """
        return pulumi.get(self, "signing_protocol")

    @signing_protocol.setter
    def signing_protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "signing_protocol", value)


class OriginAccessControl(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 origin_access_control_origin_type: Optional[pulumi.Input[str]] = None,
                 signing_behavior: Optional[pulumi.Input[str]] = None,
                 signing_protocol: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an AWS CloudFront Origin Access Control, which is used by CloudFront Distributions with an Amazon S3 bucket as the origin.

        Read more about Origin Access Control in the [CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html).

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cloudfront.OriginAccessControl("example",
            name="example",
            description="Example Policy",
            origin_access_control_origin_type="s3",
            signing_behavior="always",
            signing_protocol="sigv4")
        ```

        ## Import

        Using `pulumi import`, import CloudFront Origin Access Control using the `id`. For example:

        ```sh
        $ pulumi import aws:cloudfront/originAccessControl:OriginAccessControl example E327GJI25M56DG
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the Origin Access Control. Defaults to "Managed by Pulumi" if omitted.
        :param pulumi.Input[str] name: A name that identifies the Origin Access Control.
        :param pulumi.Input[str] origin_access_control_origin_type: The type of origin that this Origin Access Control is for. Valid values are `lambda`, `mediapackagev2`, `mediastore`, and `s3`.
        :param pulumi.Input[str] signing_behavior: Specifies which requests CloudFront signs. Specify `always` for the most common use case. Allowed values: `always`, `never`, and `no-override`.
        :param pulumi.Input[str] signing_protocol: Determines how CloudFront signs (authenticates) requests. The only valid value is `sigv4`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OriginAccessControlArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an AWS CloudFront Origin Access Control, which is used by CloudFront Distributions with an Amazon S3 bucket as the origin.

        Read more about Origin Access Control in the [CloudFront Developer Guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html).

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cloudfront.OriginAccessControl("example",
            name="example",
            description="Example Policy",
            origin_access_control_origin_type="s3",
            signing_behavior="always",
            signing_protocol="sigv4")
        ```

        ## Import

        Using `pulumi import`, import CloudFront Origin Access Control using the `id`. For example:

        ```sh
        $ pulumi import aws:cloudfront/originAccessControl:OriginAccessControl example E327GJI25M56DG
        ```

        :param str resource_name: The name of the resource.
        :param OriginAccessControlArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OriginAccessControlArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 origin_access_control_origin_type: Optional[pulumi.Input[str]] = None,
                 signing_behavior: Optional[pulumi.Input[str]] = None,
                 signing_protocol: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OriginAccessControlArgs.__new__(OriginAccessControlArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            if origin_access_control_origin_type is None and not opts.urn:
                raise TypeError("Missing required property 'origin_access_control_origin_type'")
            __props__.__dict__["origin_access_control_origin_type"] = origin_access_control_origin_type
            if signing_behavior is None and not opts.urn:
                raise TypeError("Missing required property 'signing_behavior'")
            __props__.__dict__["signing_behavior"] = signing_behavior
            if signing_protocol is None and not opts.urn:
                raise TypeError("Missing required property 'signing_protocol'")
            __props__.__dict__["signing_protocol"] = signing_protocol
            __props__.__dict__["etag"] = None
        super(OriginAccessControl, __self__).__init__(
            'aws:cloudfront/originAccessControl:OriginAccessControl',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            origin_access_control_origin_type: Optional[pulumi.Input[str]] = None,
            signing_behavior: Optional[pulumi.Input[str]] = None,
            signing_protocol: Optional[pulumi.Input[str]] = None) -> 'OriginAccessControl':
        """
        Get an existing OriginAccessControl resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the Origin Access Control. Defaults to "Managed by Pulumi" if omitted.
        :param pulumi.Input[str] etag: The current version of this Origin Access Control.
        :param pulumi.Input[str] name: A name that identifies the Origin Access Control.
        :param pulumi.Input[str] origin_access_control_origin_type: The type of origin that this Origin Access Control is for. Valid values are `lambda`, `mediapackagev2`, `mediastore`, and `s3`.
        :param pulumi.Input[str] signing_behavior: Specifies which requests CloudFront signs. Specify `always` for the most common use case. Allowed values: `always`, `never`, and `no-override`.
        :param pulumi.Input[str] signing_protocol: Determines how CloudFront signs (authenticates) requests. The only valid value is `sigv4`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OriginAccessControlState.__new__(_OriginAccessControlState)

        __props__.__dict__["description"] = description
        __props__.__dict__["etag"] = etag
        __props__.__dict__["name"] = name
        __props__.__dict__["origin_access_control_origin_type"] = origin_access_control_origin_type
        __props__.__dict__["signing_behavior"] = signing_behavior
        __props__.__dict__["signing_protocol"] = signing_protocol
        return OriginAccessControl(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the Origin Access Control. Defaults to "Managed by Pulumi" if omitted.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The current version of this Origin Access Control.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A name that identifies the Origin Access Control.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="originAccessControlOriginType")
    def origin_access_control_origin_type(self) -> pulumi.Output[str]:
        """
        The type of origin that this Origin Access Control is for. Valid values are `lambda`, `mediapackagev2`, `mediastore`, and `s3`.
        """
        return pulumi.get(self, "origin_access_control_origin_type")

    @property
    @pulumi.getter(name="signingBehavior")
    def signing_behavior(self) -> pulumi.Output[str]:
        """
        Specifies which requests CloudFront signs. Specify `always` for the most common use case. Allowed values: `always`, `never`, and `no-override`.
        """
        return pulumi.get(self, "signing_behavior")

    @property
    @pulumi.getter(name="signingProtocol")
    def signing_protocol(self) -> pulumi.Output[str]:
        """
        Determines how CloudFront signs (authenticates) requests. The only valid value is `sigv4`.
        """
        return pulumi.get(self, "signing_protocol")

