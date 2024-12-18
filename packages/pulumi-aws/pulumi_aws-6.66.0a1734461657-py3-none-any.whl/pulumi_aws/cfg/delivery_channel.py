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

__all__ = ['DeliveryChannelArgs', 'DeliveryChannel']

@pulumi.input_type
class DeliveryChannelArgs:
    def __init__(__self__, *,
                 s3_bucket_name: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 s3_key_prefix: Optional[pulumi.Input[str]] = None,
                 s3_kms_key_arn: Optional[pulumi.Input[str]] = None,
                 snapshot_delivery_properties: Optional[pulumi.Input['DeliveryChannelSnapshotDeliveryPropertiesArgs']] = None,
                 sns_topic_arn: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DeliveryChannel resource.
        :param pulumi.Input[str] s3_bucket_name: The name of the S3 bucket used to store the configuration history.
        :param pulumi.Input[str] name: The name of the delivery channel. Defaults to `default`. Changing it recreates the resource.
        :param pulumi.Input[str] s3_key_prefix: The prefix for the specified S3 bucket.
        :param pulumi.Input[str] s3_kms_key_arn: The ARN of the AWS KMS key used to encrypt objects delivered by AWS Config. Must belong to the same Region as the destination S3 bucket.
        :param pulumi.Input['DeliveryChannelSnapshotDeliveryPropertiesArgs'] snapshot_delivery_properties: Options for how AWS Config delivers configuration snapshots. See below
        :param pulumi.Input[str] sns_topic_arn: The ARN of the SNS topic that AWS Config delivers notifications to.
        """
        pulumi.set(__self__, "s3_bucket_name", s3_bucket_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if s3_key_prefix is not None:
            pulumi.set(__self__, "s3_key_prefix", s3_key_prefix)
        if s3_kms_key_arn is not None:
            pulumi.set(__self__, "s3_kms_key_arn", s3_kms_key_arn)
        if snapshot_delivery_properties is not None:
            pulumi.set(__self__, "snapshot_delivery_properties", snapshot_delivery_properties)
        if sns_topic_arn is not None:
            pulumi.set(__self__, "sns_topic_arn", sns_topic_arn)

    @property
    @pulumi.getter(name="s3BucketName")
    def s3_bucket_name(self) -> pulumi.Input[str]:
        """
        The name of the S3 bucket used to store the configuration history.
        """
        return pulumi.get(self, "s3_bucket_name")

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_bucket_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the delivery channel. Defaults to `default`. Changing it recreates the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="s3KeyPrefix")
    def s3_key_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The prefix for the specified S3 bucket.
        """
        return pulumi.get(self, "s3_key_prefix")

    @s3_key_prefix.setter
    def s3_key_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_key_prefix", value)

    @property
    @pulumi.getter(name="s3KmsKeyArn")
    def s3_kms_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the AWS KMS key used to encrypt objects delivered by AWS Config. Must belong to the same Region as the destination S3 bucket.
        """
        return pulumi.get(self, "s3_kms_key_arn")

    @s3_kms_key_arn.setter
    def s3_kms_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_kms_key_arn", value)

    @property
    @pulumi.getter(name="snapshotDeliveryProperties")
    def snapshot_delivery_properties(self) -> Optional[pulumi.Input['DeliveryChannelSnapshotDeliveryPropertiesArgs']]:
        """
        Options for how AWS Config delivers configuration snapshots. See below
        """
        return pulumi.get(self, "snapshot_delivery_properties")

    @snapshot_delivery_properties.setter
    def snapshot_delivery_properties(self, value: Optional[pulumi.Input['DeliveryChannelSnapshotDeliveryPropertiesArgs']]):
        pulumi.set(self, "snapshot_delivery_properties", value)

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the SNS topic that AWS Config delivers notifications to.
        """
        return pulumi.get(self, "sns_topic_arn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sns_topic_arn", value)


@pulumi.input_type
class _DeliveryChannelState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 s3_bucket_name: Optional[pulumi.Input[str]] = None,
                 s3_key_prefix: Optional[pulumi.Input[str]] = None,
                 s3_kms_key_arn: Optional[pulumi.Input[str]] = None,
                 snapshot_delivery_properties: Optional[pulumi.Input['DeliveryChannelSnapshotDeliveryPropertiesArgs']] = None,
                 sns_topic_arn: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DeliveryChannel resources.
        :param pulumi.Input[str] name: The name of the delivery channel. Defaults to `default`. Changing it recreates the resource.
        :param pulumi.Input[str] s3_bucket_name: The name of the S3 bucket used to store the configuration history.
        :param pulumi.Input[str] s3_key_prefix: The prefix for the specified S3 bucket.
        :param pulumi.Input[str] s3_kms_key_arn: The ARN of the AWS KMS key used to encrypt objects delivered by AWS Config. Must belong to the same Region as the destination S3 bucket.
        :param pulumi.Input['DeliveryChannelSnapshotDeliveryPropertiesArgs'] snapshot_delivery_properties: Options for how AWS Config delivers configuration snapshots. See below
        :param pulumi.Input[str] sns_topic_arn: The ARN of the SNS topic that AWS Config delivers notifications to.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if s3_bucket_name is not None:
            pulumi.set(__self__, "s3_bucket_name", s3_bucket_name)
        if s3_key_prefix is not None:
            pulumi.set(__self__, "s3_key_prefix", s3_key_prefix)
        if s3_kms_key_arn is not None:
            pulumi.set(__self__, "s3_kms_key_arn", s3_kms_key_arn)
        if snapshot_delivery_properties is not None:
            pulumi.set(__self__, "snapshot_delivery_properties", snapshot_delivery_properties)
        if sns_topic_arn is not None:
            pulumi.set(__self__, "sns_topic_arn", sns_topic_arn)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the delivery channel. Defaults to `default`. Changing it recreates the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="s3BucketName")
    def s3_bucket_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the S3 bucket used to store the configuration history.
        """
        return pulumi.get(self, "s3_bucket_name")

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_bucket_name", value)

    @property
    @pulumi.getter(name="s3KeyPrefix")
    def s3_key_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The prefix for the specified S3 bucket.
        """
        return pulumi.get(self, "s3_key_prefix")

    @s3_key_prefix.setter
    def s3_key_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_key_prefix", value)

    @property
    @pulumi.getter(name="s3KmsKeyArn")
    def s3_kms_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the AWS KMS key used to encrypt objects delivered by AWS Config. Must belong to the same Region as the destination S3 bucket.
        """
        return pulumi.get(self, "s3_kms_key_arn")

    @s3_kms_key_arn.setter
    def s3_kms_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "s3_kms_key_arn", value)

    @property
    @pulumi.getter(name="snapshotDeliveryProperties")
    def snapshot_delivery_properties(self) -> Optional[pulumi.Input['DeliveryChannelSnapshotDeliveryPropertiesArgs']]:
        """
        Options for how AWS Config delivers configuration snapshots. See below
        """
        return pulumi.get(self, "snapshot_delivery_properties")

    @snapshot_delivery_properties.setter
    def snapshot_delivery_properties(self, value: Optional[pulumi.Input['DeliveryChannelSnapshotDeliveryPropertiesArgs']]):
        pulumi.set(self, "snapshot_delivery_properties", value)

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the SNS topic that AWS Config delivers notifications to.
        """
        return pulumi.get(self, "sns_topic_arn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sns_topic_arn", value)


class DeliveryChannel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 s3_bucket_name: Optional[pulumi.Input[str]] = None,
                 s3_key_prefix: Optional[pulumi.Input[str]] = None,
                 s3_kms_key_arn: Optional[pulumi.Input[str]] = None,
                 snapshot_delivery_properties: Optional[pulumi.Input[Union['DeliveryChannelSnapshotDeliveryPropertiesArgs', 'DeliveryChannelSnapshotDeliveryPropertiesArgsDict']]] = None,
                 sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an AWS Config Delivery Channel.

        > **Note:** Delivery Channel requires a Configuration Recorder to be present. Use of `depends_on` (as shown below) is recommended to avoid race conditions.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        b = aws.s3.BucketV2("b",
            bucket="example-awsconfig",
            force_destroy=True)
        assume_role = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "principals": [{
                "type": "Service",
                "identifiers": ["config.amazonaws.com"],
            }],
            "actions": ["sts:AssumeRole"],
        }])
        r = aws.iam.Role("r",
            name="awsconfig-example",
            assume_role_policy=assume_role.json)
        foo_recorder = aws.cfg.Recorder("foo",
            name="example",
            role_arn=r.arn)
        foo = aws.cfg.DeliveryChannel("foo",
            name="example",
            s3_bucket_name=b.bucket,
            opts = pulumi.ResourceOptions(depends_on=[foo_recorder]))
        p = aws.iam.get_policy_document_output(statements=[{
            "effect": "Allow",
            "actions": ["s3:*"],
            "resources": [
                b.arn,
                b.arn.apply(lambda arn: f"{arn}/*"),
            ],
        }])
        p_role_policy = aws.iam.RolePolicy("p",
            name="awsconfig-example",
            role=r.id,
            policy=p.json)
        ```

        ## Import

        Using `pulumi import`, import Delivery Channel using the name. For example:

        ```sh
        $ pulumi import aws:cfg/deliveryChannel:DeliveryChannel foo example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the delivery channel. Defaults to `default`. Changing it recreates the resource.
        :param pulumi.Input[str] s3_bucket_name: The name of the S3 bucket used to store the configuration history.
        :param pulumi.Input[str] s3_key_prefix: The prefix for the specified S3 bucket.
        :param pulumi.Input[str] s3_kms_key_arn: The ARN of the AWS KMS key used to encrypt objects delivered by AWS Config. Must belong to the same Region as the destination S3 bucket.
        :param pulumi.Input[Union['DeliveryChannelSnapshotDeliveryPropertiesArgs', 'DeliveryChannelSnapshotDeliveryPropertiesArgsDict']] snapshot_delivery_properties: Options for how AWS Config delivers configuration snapshots. See below
        :param pulumi.Input[str] sns_topic_arn: The ARN of the SNS topic that AWS Config delivers notifications to.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeliveryChannelArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an AWS Config Delivery Channel.

        > **Note:** Delivery Channel requires a Configuration Recorder to be present. Use of `depends_on` (as shown below) is recommended to avoid race conditions.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        b = aws.s3.BucketV2("b",
            bucket="example-awsconfig",
            force_destroy=True)
        assume_role = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "principals": [{
                "type": "Service",
                "identifiers": ["config.amazonaws.com"],
            }],
            "actions": ["sts:AssumeRole"],
        }])
        r = aws.iam.Role("r",
            name="awsconfig-example",
            assume_role_policy=assume_role.json)
        foo_recorder = aws.cfg.Recorder("foo",
            name="example",
            role_arn=r.arn)
        foo = aws.cfg.DeliveryChannel("foo",
            name="example",
            s3_bucket_name=b.bucket,
            opts = pulumi.ResourceOptions(depends_on=[foo_recorder]))
        p = aws.iam.get_policy_document_output(statements=[{
            "effect": "Allow",
            "actions": ["s3:*"],
            "resources": [
                b.arn,
                b.arn.apply(lambda arn: f"{arn}/*"),
            ],
        }])
        p_role_policy = aws.iam.RolePolicy("p",
            name="awsconfig-example",
            role=r.id,
            policy=p.json)
        ```

        ## Import

        Using `pulumi import`, import Delivery Channel using the name. For example:

        ```sh
        $ pulumi import aws:cfg/deliveryChannel:DeliveryChannel foo example
        ```

        :param str resource_name: The name of the resource.
        :param DeliveryChannelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeliveryChannelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 s3_bucket_name: Optional[pulumi.Input[str]] = None,
                 s3_key_prefix: Optional[pulumi.Input[str]] = None,
                 s3_kms_key_arn: Optional[pulumi.Input[str]] = None,
                 snapshot_delivery_properties: Optional[pulumi.Input[Union['DeliveryChannelSnapshotDeliveryPropertiesArgs', 'DeliveryChannelSnapshotDeliveryPropertiesArgsDict']]] = None,
                 sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeliveryChannelArgs.__new__(DeliveryChannelArgs)

            __props__.__dict__["name"] = name
            if s3_bucket_name is None and not opts.urn:
                raise TypeError("Missing required property 's3_bucket_name'")
            __props__.__dict__["s3_bucket_name"] = s3_bucket_name
            __props__.__dict__["s3_key_prefix"] = s3_key_prefix
            __props__.__dict__["s3_kms_key_arn"] = s3_kms_key_arn
            __props__.__dict__["snapshot_delivery_properties"] = snapshot_delivery_properties
            __props__.__dict__["sns_topic_arn"] = sns_topic_arn
        super(DeliveryChannel, __self__).__init__(
            'aws:cfg/deliveryChannel:DeliveryChannel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            s3_bucket_name: Optional[pulumi.Input[str]] = None,
            s3_key_prefix: Optional[pulumi.Input[str]] = None,
            s3_kms_key_arn: Optional[pulumi.Input[str]] = None,
            snapshot_delivery_properties: Optional[pulumi.Input[Union['DeliveryChannelSnapshotDeliveryPropertiesArgs', 'DeliveryChannelSnapshotDeliveryPropertiesArgsDict']]] = None,
            sns_topic_arn: Optional[pulumi.Input[str]] = None) -> 'DeliveryChannel':
        """
        Get an existing DeliveryChannel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the delivery channel. Defaults to `default`. Changing it recreates the resource.
        :param pulumi.Input[str] s3_bucket_name: The name of the S3 bucket used to store the configuration history.
        :param pulumi.Input[str] s3_key_prefix: The prefix for the specified S3 bucket.
        :param pulumi.Input[str] s3_kms_key_arn: The ARN of the AWS KMS key used to encrypt objects delivered by AWS Config. Must belong to the same Region as the destination S3 bucket.
        :param pulumi.Input[Union['DeliveryChannelSnapshotDeliveryPropertiesArgs', 'DeliveryChannelSnapshotDeliveryPropertiesArgsDict']] snapshot_delivery_properties: Options for how AWS Config delivers configuration snapshots. See below
        :param pulumi.Input[str] sns_topic_arn: The ARN of the SNS topic that AWS Config delivers notifications to.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DeliveryChannelState.__new__(_DeliveryChannelState)

        __props__.__dict__["name"] = name
        __props__.__dict__["s3_bucket_name"] = s3_bucket_name
        __props__.__dict__["s3_key_prefix"] = s3_key_prefix
        __props__.__dict__["s3_kms_key_arn"] = s3_kms_key_arn
        __props__.__dict__["snapshot_delivery_properties"] = snapshot_delivery_properties
        __props__.__dict__["sns_topic_arn"] = sns_topic_arn
        return DeliveryChannel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the delivery channel. Defaults to `default`. Changing it recreates the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="s3BucketName")
    def s3_bucket_name(self) -> pulumi.Output[str]:
        """
        The name of the S3 bucket used to store the configuration history.
        """
        return pulumi.get(self, "s3_bucket_name")

    @property
    @pulumi.getter(name="s3KeyPrefix")
    def s3_key_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The prefix for the specified S3 bucket.
        """
        return pulumi.get(self, "s3_key_prefix")

    @property
    @pulumi.getter(name="s3KmsKeyArn")
    def s3_kms_key_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The ARN of the AWS KMS key used to encrypt objects delivered by AWS Config. Must belong to the same Region as the destination S3 bucket.
        """
        return pulumi.get(self, "s3_kms_key_arn")

    @property
    @pulumi.getter(name="snapshotDeliveryProperties")
    def snapshot_delivery_properties(self) -> pulumi.Output[Optional['outputs.DeliveryChannelSnapshotDeliveryProperties']]:
        """
        Options for how AWS Config delivers configuration snapshots. See below
        """
        return pulumi.get(self, "snapshot_delivery_properties")

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The ARN of the SNS topic that AWS Config delivers notifications to.
        """
        return pulumi.get(self, "sns_topic_arn")

