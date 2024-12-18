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

__all__ = ['InviteAccepterArgs', 'InviteAccepter']

@pulumi.input_type
class InviteAccepterArgs:
    def __init__(__self__, *,
                 master_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a InviteAccepter resource.
        :param pulumi.Input[str] master_id: The account ID of the master Security Hub account whose invitation you're accepting.
        """
        pulumi.set(__self__, "master_id", master_id)

    @property
    @pulumi.getter(name="masterId")
    def master_id(self) -> pulumi.Input[str]:
        """
        The account ID of the master Security Hub account whose invitation you're accepting.
        """
        return pulumi.get(self, "master_id")

    @master_id.setter
    def master_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "master_id", value)


@pulumi.input_type
class _InviteAccepterState:
    def __init__(__self__, *,
                 invitation_id: Optional[pulumi.Input[str]] = None,
                 master_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InviteAccepter resources.
        :param pulumi.Input[str] invitation_id: The ID of the invitation.
        :param pulumi.Input[str] master_id: The account ID of the master Security Hub account whose invitation you're accepting.
        """
        if invitation_id is not None:
            pulumi.set(__self__, "invitation_id", invitation_id)
        if master_id is not None:
            pulumi.set(__self__, "master_id", master_id)

    @property
    @pulumi.getter(name="invitationId")
    def invitation_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the invitation.
        """
        return pulumi.get(self, "invitation_id")

    @invitation_id.setter
    def invitation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "invitation_id", value)

    @property
    @pulumi.getter(name="masterId")
    def master_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account ID of the master Security Hub account whose invitation you're accepting.
        """
        return pulumi.get(self, "master_id")

    @master_id.setter
    def master_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "master_id", value)


class InviteAccepter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 master_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        > **Note:** AWS accounts can only be associated with a single Security Hub master account. Destroying this resource will disassociate the member account from the master account.

        Accepts a Security Hub invitation.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.securityhub.Account("example")
        example_member = aws.securityhub.Member("example",
            account_id="123456789012",
            email="example@example.com",
            invite=True)
        invitee = aws.securityhub.Account("invitee")
        invitee_invite_accepter = aws.securityhub.InviteAccepter("invitee", master_id=example_member.master_id,
        opts = pulumi.ResourceOptions(depends_on=[invitee]))
        ```

        ## Import

        Using `pulumi import`, import Security Hub invite acceptance using the account ID. For example:

        ```sh
        $ pulumi import aws:securityhub/inviteAccepter:InviteAccepter example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] master_id: The account ID of the master Security Hub account whose invitation you're accepting.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InviteAccepterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > **Note:** AWS accounts can only be associated with a single Security Hub master account. Destroying this resource will disassociate the member account from the master account.

        Accepts a Security Hub invitation.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.securityhub.Account("example")
        example_member = aws.securityhub.Member("example",
            account_id="123456789012",
            email="example@example.com",
            invite=True)
        invitee = aws.securityhub.Account("invitee")
        invitee_invite_accepter = aws.securityhub.InviteAccepter("invitee", master_id=example_member.master_id,
        opts = pulumi.ResourceOptions(depends_on=[invitee]))
        ```

        ## Import

        Using `pulumi import`, import Security Hub invite acceptance using the account ID. For example:

        ```sh
        $ pulumi import aws:securityhub/inviteAccepter:InviteAccepter example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param InviteAccepterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InviteAccepterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 master_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InviteAccepterArgs.__new__(InviteAccepterArgs)

            if master_id is None and not opts.urn:
                raise TypeError("Missing required property 'master_id'")
            __props__.__dict__["master_id"] = master_id
            __props__.__dict__["invitation_id"] = None
        super(InviteAccepter, __self__).__init__(
            'aws:securityhub/inviteAccepter:InviteAccepter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            invitation_id: Optional[pulumi.Input[str]] = None,
            master_id: Optional[pulumi.Input[str]] = None) -> 'InviteAccepter':
        """
        Get an existing InviteAccepter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] invitation_id: The ID of the invitation.
        :param pulumi.Input[str] master_id: The account ID of the master Security Hub account whose invitation you're accepting.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InviteAccepterState.__new__(_InviteAccepterState)

        __props__.__dict__["invitation_id"] = invitation_id
        __props__.__dict__["master_id"] = master_id
        return InviteAccepter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="invitationId")
    def invitation_id(self) -> pulumi.Output[str]:
        """
        The ID of the invitation.
        """
        return pulumi.get(self, "invitation_id")

    @property
    @pulumi.getter(name="masterId")
    def master_id(self) -> pulumi.Output[str]:
        """
        The account ID of the master Security Hub account whose invitation you're accepting.
        """
        return pulumi.get(self, "master_id")

