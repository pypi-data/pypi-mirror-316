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

__all__ = ['EmailIdentityMailFromAttributesArgs', 'EmailIdentityMailFromAttributes']

@pulumi.input_type
class EmailIdentityMailFromAttributesArgs:
    def __init__(__self__, *,
                 email_identity: pulumi.Input[str],
                 behavior_on_mx_failure: Optional[pulumi.Input[str]] = None,
                 mail_from_domain: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EmailIdentityMailFromAttributes resource.
        :param pulumi.Input[str] email_identity: The verified email identity.
        :param pulumi.Input[str] behavior_on_mx_failure: The action to take if the required MX record isn't found when you send an email. Valid values: `USE_DEFAULT_VALUE`, `REJECT_MESSAGE`.
        :param pulumi.Input[str] mail_from_domain: The custom MAIL FROM domain that you want the verified identity to use. Required if `behavior_on_mx_failure` is `REJECT_MESSAGE`.
        """
        pulumi.set(__self__, "email_identity", email_identity)
        if behavior_on_mx_failure is not None:
            pulumi.set(__self__, "behavior_on_mx_failure", behavior_on_mx_failure)
        if mail_from_domain is not None:
            pulumi.set(__self__, "mail_from_domain", mail_from_domain)

    @property
    @pulumi.getter(name="emailIdentity")
    def email_identity(self) -> pulumi.Input[str]:
        """
        The verified email identity.
        """
        return pulumi.get(self, "email_identity")

    @email_identity.setter
    def email_identity(self, value: pulumi.Input[str]):
        pulumi.set(self, "email_identity", value)

    @property
    @pulumi.getter(name="behaviorOnMxFailure")
    def behavior_on_mx_failure(self) -> Optional[pulumi.Input[str]]:
        """
        The action to take if the required MX record isn't found when you send an email. Valid values: `USE_DEFAULT_VALUE`, `REJECT_MESSAGE`.
        """
        return pulumi.get(self, "behavior_on_mx_failure")

    @behavior_on_mx_failure.setter
    def behavior_on_mx_failure(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "behavior_on_mx_failure", value)

    @property
    @pulumi.getter(name="mailFromDomain")
    def mail_from_domain(self) -> Optional[pulumi.Input[str]]:
        """
        The custom MAIL FROM domain that you want the verified identity to use. Required if `behavior_on_mx_failure` is `REJECT_MESSAGE`.
        """
        return pulumi.get(self, "mail_from_domain")

    @mail_from_domain.setter
    def mail_from_domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mail_from_domain", value)


@pulumi.input_type
class _EmailIdentityMailFromAttributesState:
    def __init__(__self__, *,
                 behavior_on_mx_failure: Optional[pulumi.Input[str]] = None,
                 email_identity: Optional[pulumi.Input[str]] = None,
                 mail_from_domain: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EmailIdentityMailFromAttributes resources.
        :param pulumi.Input[str] behavior_on_mx_failure: The action to take if the required MX record isn't found when you send an email. Valid values: `USE_DEFAULT_VALUE`, `REJECT_MESSAGE`.
        :param pulumi.Input[str] email_identity: The verified email identity.
        :param pulumi.Input[str] mail_from_domain: The custom MAIL FROM domain that you want the verified identity to use. Required if `behavior_on_mx_failure` is `REJECT_MESSAGE`.
        """
        if behavior_on_mx_failure is not None:
            pulumi.set(__self__, "behavior_on_mx_failure", behavior_on_mx_failure)
        if email_identity is not None:
            pulumi.set(__self__, "email_identity", email_identity)
        if mail_from_domain is not None:
            pulumi.set(__self__, "mail_from_domain", mail_from_domain)

    @property
    @pulumi.getter(name="behaviorOnMxFailure")
    def behavior_on_mx_failure(self) -> Optional[pulumi.Input[str]]:
        """
        The action to take if the required MX record isn't found when you send an email. Valid values: `USE_DEFAULT_VALUE`, `REJECT_MESSAGE`.
        """
        return pulumi.get(self, "behavior_on_mx_failure")

    @behavior_on_mx_failure.setter
    def behavior_on_mx_failure(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "behavior_on_mx_failure", value)

    @property
    @pulumi.getter(name="emailIdentity")
    def email_identity(self) -> Optional[pulumi.Input[str]]:
        """
        The verified email identity.
        """
        return pulumi.get(self, "email_identity")

    @email_identity.setter
    def email_identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_identity", value)

    @property
    @pulumi.getter(name="mailFromDomain")
    def mail_from_domain(self) -> Optional[pulumi.Input[str]]:
        """
        The custom MAIL FROM domain that you want the verified identity to use. Required if `behavior_on_mx_failure` is `REJECT_MESSAGE`.
        """
        return pulumi.get(self, "mail_from_domain")

    @mail_from_domain.setter
    def mail_from_domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mail_from_domain", value)


class EmailIdentityMailFromAttributes(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 behavior_on_mx_failure: Optional[pulumi.Input[str]] = None,
                 email_identity: Optional[pulumi.Input[str]] = None,
                 mail_from_domain: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS SESv2 (Simple Email V2) Email Identity Mail From Attributes.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sesv2.EmailIdentity("example", email_identity="example.com")
        example_email_identity_mail_from_attributes = aws.sesv2.EmailIdentityMailFromAttributes("example",
            email_identity=example.email_identity,
            behavior_on_mx_failure="REJECT_MESSAGE",
            mail_from_domain=example.email_identity.apply(lambda email_identity: f"subdomain.{email_identity}"))
        ```

        ## Import

        Using `pulumi import`, import SESv2 (Simple Email V2) Email Identity Mail From Attributes using the `email_identity`. For example:

        ```sh
        $ pulumi import aws:sesv2/emailIdentityMailFromAttributes:EmailIdentityMailFromAttributes example example.com
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] behavior_on_mx_failure: The action to take if the required MX record isn't found when you send an email. Valid values: `USE_DEFAULT_VALUE`, `REJECT_MESSAGE`.
        :param pulumi.Input[str] email_identity: The verified email identity.
        :param pulumi.Input[str] mail_from_domain: The custom MAIL FROM domain that you want the verified identity to use. Required if `behavior_on_mx_failure` is `REJECT_MESSAGE`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EmailIdentityMailFromAttributesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS SESv2 (Simple Email V2) Email Identity Mail From Attributes.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sesv2.EmailIdentity("example", email_identity="example.com")
        example_email_identity_mail_from_attributes = aws.sesv2.EmailIdentityMailFromAttributes("example",
            email_identity=example.email_identity,
            behavior_on_mx_failure="REJECT_MESSAGE",
            mail_from_domain=example.email_identity.apply(lambda email_identity: f"subdomain.{email_identity}"))
        ```

        ## Import

        Using `pulumi import`, import SESv2 (Simple Email V2) Email Identity Mail From Attributes using the `email_identity`. For example:

        ```sh
        $ pulumi import aws:sesv2/emailIdentityMailFromAttributes:EmailIdentityMailFromAttributes example example.com
        ```

        :param str resource_name: The name of the resource.
        :param EmailIdentityMailFromAttributesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EmailIdentityMailFromAttributesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 behavior_on_mx_failure: Optional[pulumi.Input[str]] = None,
                 email_identity: Optional[pulumi.Input[str]] = None,
                 mail_from_domain: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EmailIdentityMailFromAttributesArgs.__new__(EmailIdentityMailFromAttributesArgs)

            __props__.__dict__["behavior_on_mx_failure"] = behavior_on_mx_failure
            if email_identity is None and not opts.urn:
                raise TypeError("Missing required property 'email_identity'")
            __props__.__dict__["email_identity"] = email_identity
            __props__.__dict__["mail_from_domain"] = mail_from_domain
        super(EmailIdentityMailFromAttributes, __self__).__init__(
            'aws:sesv2/emailIdentityMailFromAttributes:EmailIdentityMailFromAttributes',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            behavior_on_mx_failure: Optional[pulumi.Input[str]] = None,
            email_identity: Optional[pulumi.Input[str]] = None,
            mail_from_domain: Optional[pulumi.Input[str]] = None) -> 'EmailIdentityMailFromAttributes':
        """
        Get an existing EmailIdentityMailFromAttributes resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] behavior_on_mx_failure: The action to take if the required MX record isn't found when you send an email. Valid values: `USE_DEFAULT_VALUE`, `REJECT_MESSAGE`.
        :param pulumi.Input[str] email_identity: The verified email identity.
        :param pulumi.Input[str] mail_from_domain: The custom MAIL FROM domain that you want the verified identity to use. Required if `behavior_on_mx_failure` is `REJECT_MESSAGE`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EmailIdentityMailFromAttributesState.__new__(_EmailIdentityMailFromAttributesState)

        __props__.__dict__["behavior_on_mx_failure"] = behavior_on_mx_failure
        __props__.__dict__["email_identity"] = email_identity
        __props__.__dict__["mail_from_domain"] = mail_from_domain
        return EmailIdentityMailFromAttributes(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="behaviorOnMxFailure")
    def behavior_on_mx_failure(self) -> pulumi.Output[Optional[str]]:
        """
        The action to take if the required MX record isn't found when you send an email. Valid values: `USE_DEFAULT_VALUE`, `REJECT_MESSAGE`.
        """
        return pulumi.get(self, "behavior_on_mx_failure")

    @property
    @pulumi.getter(name="emailIdentity")
    def email_identity(self) -> pulumi.Output[str]:
        """
        The verified email identity.
        """
        return pulumi.get(self, "email_identity")

    @property
    @pulumi.getter(name="mailFromDomain")
    def mail_from_domain(self) -> pulumi.Output[Optional[str]]:
        """
        The custom MAIL FROM domain that you want the verified identity to use. Required if `behavior_on_mx_failure` is `REJECT_MESSAGE`.
        """
        return pulumi.get(self, "mail_from_domain")

