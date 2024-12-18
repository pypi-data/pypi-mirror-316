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

__all__ = ['PolicyAttachmentArgs', 'PolicyAttachment']

@pulumi.input_type
class PolicyAttachmentArgs:
    def __init__(__self__, *,
                 policy: pulumi.Input[str],
                 target: pulumi.Input[str]):
        """
        The set of arguments for constructing a PolicyAttachment resource.
        :param pulumi.Input[str] policy: The name of the policy to attach.
        :param pulumi.Input[str] target: The identity to which the policy is attached.
        """
        pulumi.set(__self__, "policy", policy)
        pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        The name of the policy to attach.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        """
        The identity to which the policy is attached.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)


@pulumi.input_type
class _PolicyAttachmentState:
    def __init__(__self__, *,
                 policy: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PolicyAttachment resources.
        :param pulumi.Input[str] policy: The name of the policy to attach.
        :param pulumi.Input[str] target: The identity to which the policy is attached.
        """
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if target is not None:
            pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the policy to attach.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input[str]]:
        """
        The identity to which the policy is attached.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target", value)


class PolicyAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an IoT policy attachment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        pubsub = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "actions": ["iot:*"],
            "resources": ["*"],
        }])
        pubsub_policy = aws.iot.Policy("pubsub",
            name="PubSubToAnyTopic",
            policy=pubsub.json)
        cert = aws.iot.Certificate("cert",
            csr=std.file(input="csr.pem").result,
            active=True)
        att = aws.iot.PolicyAttachment("att",
            policy=pubsub_policy.name,
            target=cert.arn)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The name of the policy to attach.
        :param pulumi.Input[str] target: The identity to which the policy is attached.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PolicyAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an IoT policy attachment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        pubsub = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "actions": ["iot:*"],
            "resources": ["*"],
        }])
        pubsub_policy = aws.iot.Policy("pubsub",
            name="PubSubToAnyTopic",
            policy=pubsub.json)
        cert = aws.iot.Certificate("cert",
            csr=std.file(input="csr.pem").result,
            active=True)
        att = aws.iot.PolicyAttachment("att",
            policy=pubsub_policy.name,
            target=cert.arn)
        ```

        :param str resource_name: The name of the resource.
        :param PolicyAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PolicyAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PolicyAttachmentArgs.__new__(PolicyAttachmentArgs)

            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
            if target is None and not opts.urn:
                raise TypeError("Missing required property 'target'")
            __props__.__dict__["target"] = target
        super(PolicyAttachment, __self__).__init__(
            'aws:iot/policyAttachment:PolicyAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            policy: Optional[pulumi.Input[str]] = None,
            target: Optional[pulumi.Input[str]] = None) -> 'PolicyAttachment':
        """
        Get an existing PolicyAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The name of the policy to attach.
        :param pulumi.Input[str] target: The identity to which the policy is attached.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PolicyAttachmentState.__new__(_PolicyAttachmentState)

        __props__.__dict__["policy"] = policy
        __props__.__dict__["target"] = target
        return PolicyAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The name of the policy to attach.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output[str]:
        """
        The identity to which the policy is attached.
        """
        return pulumi.get(self, "target")

