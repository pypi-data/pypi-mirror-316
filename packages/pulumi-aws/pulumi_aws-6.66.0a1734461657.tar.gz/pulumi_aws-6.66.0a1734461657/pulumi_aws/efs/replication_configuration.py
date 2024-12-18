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

__all__ = ['ReplicationConfigurationArgs', 'ReplicationConfiguration']

@pulumi.input_type
class ReplicationConfigurationArgs:
    def __init__(__self__, *,
                 destination: pulumi.Input['ReplicationConfigurationDestinationArgs'],
                 source_file_system_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a ReplicationConfiguration resource.
        :param pulumi.Input['ReplicationConfigurationDestinationArgs'] destination: A destination configuration block (documented below).
        :param pulumi.Input[str] source_file_system_id: The ID of the file system that is to be replicated.
        """
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "source_file_system_id", source_file_system_id)

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Input['ReplicationConfigurationDestinationArgs']:
        """
        A destination configuration block (documented below).
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: pulumi.Input['ReplicationConfigurationDestinationArgs']):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter(name="sourceFileSystemId")
    def source_file_system_id(self) -> pulumi.Input[str]:
        """
        The ID of the file system that is to be replicated.
        """
        return pulumi.get(self, "source_file_system_id")

    @source_file_system_id.setter
    def source_file_system_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_file_system_id", value)


@pulumi.input_type
class _ReplicationConfigurationState:
    def __init__(__self__, *,
                 creation_time: Optional[pulumi.Input[str]] = None,
                 destination: Optional[pulumi.Input['ReplicationConfigurationDestinationArgs']] = None,
                 original_source_file_system_arn: Optional[pulumi.Input[str]] = None,
                 source_file_system_arn: Optional[pulumi.Input[str]] = None,
                 source_file_system_id: Optional[pulumi.Input[str]] = None,
                 source_file_system_region: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ReplicationConfiguration resources.
        :param pulumi.Input[str] creation_time: When the replication configuration was created.
               * `destination[0].file_system_id` - The fs ID of the replica.
               * `destination[0].status` - The status of the replication.
        :param pulumi.Input['ReplicationConfigurationDestinationArgs'] destination: A destination configuration block (documented below).
        :param pulumi.Input[str] original_source_file_system_arn: The Amazon Resource Name (ARN) of the original source Amazon EFS file system in the replication configuration.
        :param pulumi.Input[str] source_file_system_arn: The Amazon Resource Name (ARN) of the current source file system in the replication configuration.
        :param pulumi.Input[str] source_file_system_id: The ID of the file system that is to be replicated.
        :param pulumi.Input[str] source_file_system_region: The AWS Region in which the source Amazon EFS file system is located.
        """
        if creation_time is not None:
            pulumi.set(__self__, "creation_time", creation_time)
        if destination is not None:
            pulumi.set(__self__, "destination", destination)
        if original_source_file_system_arn is not None:
            pulumi.set(__self__, "original_source_file_system_arn", original_source_file_system_arn)
        if source_file_system_arn is not None:
            pulumi.set(__self__, "source_file_system_arn", source_file_system_arn)
        if source_file_system_id is not None:
            pulumi.set(__self__, "source_file_system_id", source_file_system_id)
        if source_file_system_region is not None:
            pulumi.set(__self__, "source_file_system_region", source_file_system_region)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[pulumi.Input[str]]:
        """
        When the replication configuration was created.
        * `destination[0].file_system_id` - The fs ID of the replica.
        * `destination[0].status` - The status of the replication.
        """
        return pulumi.get(self, "creation_time")

    @creation_time.setter
    def creation_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_time", value)

    @property
    @pulumi.getter
    def destination(self) -> Optional[pulumi.Input['ReplicationConfigurationDestinationArgs']]:
        """
        A destination configuration block (documented below).
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: Optional[pulumi.Input['ReplicationConfigurationDestinationArgs']]):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter(name="originalSourceFileSystemArn")
    def original_source_file_system_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the original source Amazon EFS file system in the replication configuration.
        """
        return pulumi.get(self, "original_source_file_system_arn")

    @original_source_file_system_arn.setter
    def original_source_file_system_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "original_source_file_system_arn", value)

    @property
    @pulumi.getter(name="sourceFileSystemArn")
    def source_file_system_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the current source file system in the replication configuration.
        """
        return pulumi.get(self, "source_file_system_arn")

    @source_file_system_arn.setter
    def source_file_system_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_file_system_arn", value)

    @property
    @pulumi.getter(name="sourceFileSystemId")
    def source_file_system_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the file system that is to be replicated.
        """
        return pulumi.get(self, "source_file_system_id")

    @source_file_system_id.setter
    def source_file_system_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_file_system_id", value)

    @property
    @pulumi.getter(name="sourceFileSystemRegion")
    def source_file_system_region(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS Region in which the source Amazon EFS file system is located.
        """
        return pulumi.get(self, "source_file_system_region")

    @source_file_system_region.setter
    def source_file_system_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_file_system_region", value)


class ReplicationConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination: Optional[pulumi.Input[Union['ReplicationConfigurationDestinationArgs', 'ReplicationConfigurationDestinationArgsDict']]] = None,
                 source_file_system_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a replica of an existing EFS file system in the same or another region. Creating this resource causes the source EFS file system to be replicated to a new read-only destination EFS file system (unless using the `destination.file_system_id` attribute). Deleting this resource will cause the replication from source to destination to stop and the destination file system will no longer be read only.

        > **NOTE:** Deleting this resource does **not** delete the destination file system that was created.

        ## Example Usage

        Will create a replica using regional storage in us-west-2 that will be encrypted by the default EFS KMS key `/aws/elasticfilesystem`.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.efs.FileSystem("example")
        example_replication_configuration = aws.efs.ReplicationConfiguration("example",
            source_file_system_id=example.id,
            destination={
                "region": "us-west-2",
            })
        ```

        Replica will be created as One Zone storage in the us-west-2b Availability Zone and encrypted with the specified KMS key.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.efs.FileSystem("example")
        example_replication_configuration = aws.efs.ReplicationConfiguration("example",
            source_file_system_id=example.id,
            destination={
                "availability_zone_name": "us-west-2b",
                "kms_key_id": "1234abcd-12ab-34cd-56ef-1234567890ab",
            })
        ```

        Will create a replica and set the existing file system with id `fs-1234567890` in us-west-2 as destination.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.efs.FileSystem("example")
        example_replication_configuration = aws.efs.ReplicationConfiguration("example",
            source_file_system_id=example.id,
            destination={
                "file_system_id": "fs-1234567890",
                "region": "us-west-2",
            })
        ```

        ## Import

        Using `pulumi import`, import EFS Replication Configurations using the file system ID of either the source or destination file system. When importing, the `availability_zone_name` and `kms_key_id` attributes must __not__ be set in the configuration. The AWS API does not return these values when querying the replication configuration and their presence will therefore show as a diff in a subsequent plan. For example:

        ```sh
        $ pulumi import aws:efs/replicationConfiguration:ReplicationConfiguration example fs-id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['ReplicationConfigurationDestinationArgs', 'ReplicationConfigurationDestinationArgsDict']] destination: A destination configuration block (documented below).
        :param pulumi.Input[str] source_file_system_id: The ID of the file system that is to be replicated.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicationConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a replica of an existing EFS file system in the same or another region. Creating this resource causes the source EFS file system to be replicated to a new read-only destination EFS file system (unless using the `destination.file_system_id` attribute). Deleting this resource will cause the replication from source to destination to stop and the destination file system will no longer be read only.

        > **NOTE:** Deleting this resource does **not** delete the destination file system that was created.

        ## Example Usage

        Will create a replica using regional storage in us-west-2 that will be encrypted by the default EFS KMS key `/aws/elasticfilesystem`.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.efs.FileSystem("example")
        example_replication_configuration = aws.efs.ReplicationConfiguration("example",
            source_file_system_id=example.id,
            destination={
                "region": "us-west-2",
            })
        ```

        Replica will be created as One Zone storage in the us-west-2b Availability Zone and encrypted with the specified KMS key.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.efs.FileSystem("example")
        example_replication_configuration = aws.efs.ReplicationConfiguration("example",
            source_file_system_id=example.id,
            destination={
                "availability_zone_name": "us-west-2b",
                "kms_key_id": "1234abcd-12ab-34cd-56ef-1234567890ab",
            })
        ```

        Will create a replica and set the existing file system with id `fs-1234567890` in us-west-2 as destination.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.efs.FileSystem("example")
        example_replication_configuration = aws.efs.ReplicationConfiguration("example",
            source_file_system_id=example.id,
            destination={
                "file_system_id": "fs-1234567890",
                "region": "us-west-2",
            })
        ```

        ## Import

        Using `pulumi import`, import EFS Replication Configurations using the file system ID of either the source or destination file system. When importing, the `availability_zone_name` and `kms_key_id` attributes must __not__ be set in the configuration. The AWS API does not return these values when querying the replication configuration and their presence will therefore show as a diff in a subsequent plan. For example:

        ```sh
        $ pulumi import aws:efs/replicationConfiguration:ReplicationConfiguration example fs-id
        ```

        :param str resource_name: The name of the resource.
        :param ReplicationConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicationConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination: Optional[pulumi.Input[Union['ReplicationConfigurationDestinationArgs', 'ReplicationConfigurationDestinationArgsDict']]] = None,
                 source_file_system_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicationConfigurationArgs.__new__(ReplicationConfigurationArgs)

            if destination is None and not opts.urn:
                raise TypeError("Missing required property 'destination'")
            __props__.__dict__["destination"] = destination
            if source_file_system_id is None and not opts.urn:
                raise TypeError("Missing required property 'source_file_system_id'")
            __props__.__dict__["source_file_system_id"] = source_file_system_id
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["original_source_file_system_arn"] = None
            __props__.__dict__["source_file_system_arn"] = None
            __props__.__dict__["source_file_system_region"] = None
        super(ReplicationConfiguration, __self__).__init__(
            'aws:efs/replicationConfiguration:ReplicationConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            creation_time: Optional[pulumi.Input[str]] = None,
            destination: Optional[pulumi.Input[Union['ReplicationConfigurationDestinationArgs', 'ReplicationConfigurationDestinationArgsDict']]] = None,
            original_source_file_system_arn: Optional[pulumi.Input[str]] = None,
            source_file_system_arn: Optional[pulumi.Input[str]] = None,
            source_file_system_id: Optional[pulumi.Input[str]] = None,
            source_file_system_region: Optional[pulumi.Input[str]] = None) -> 'ReplicationConfiguration':
        """
        Get an existing ReplicationConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] creation_time: When the replication configuration was created.
               * `destination[0].file_system_id` - The fs ID of the replica.
               * `destination[0].status` - The status of the replication.
        :param pulumi.Input[Union['ReplicationConfigurationDestinationArgs', 'ReplicationConfigurationDestinationArgsDict']] destination: A destination configuration block (documented below).
        :param pulumi.Input[str] original_source_file_system_arn: The Amazon Resource Name (ARN) of the original source Amazon EFS file system in the replication configuration.
        :param pulumi.Input[str] source_file_system_arn: The Amazon Resource Name (ARN) of the current source file system in the replication configuration.
        :param pulumi.Input[str] source_file_system_id: The ID of the file system that is to be replicated.
        :param pulumi.Input[str] source_file_system_region: The AWS Region in which the source Amazon EFS file system is located.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ReplicationConfigurationState.__new__(_ReplicationConfigurationState)

        __props__.__dict__["creation_time"] = creation_time
        __props__.__dict__["destination"] = destination
        __props__.__dict__["original_source_file_system_arn"] = original_source_file_system_arn
        __props__.__dict__["source_file_system_arn"] = source_file_system_arn
        __props__.__dict__["source_file_system_id"] = source_file_system_id
        __props__.__dict__["source_file_system_region"] = source_file_system_region
        return ReplicationConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        When the replication configuration was created.
        * `destination[0].file_system_id` - The fs ID of the replica.
        * `destination[0].status` - The status of the replication.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Output['outputs.ReplicationConfigurationDestination']:
        """
        A destination configuration block (documented below).
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="originalSourceFileSystemArn")
    def original_source_file_system_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the original source Amazon EFS file system in the replication configuration.
        """
        return pulumi.get(self, "original_source_file_system_arn")

    @property
    @pulumi.getter(name="sourceFileSystemArn")
    def source_file_system_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the current source file system in the replication configuration.
        """
        return pulumi.get(self, "source_file_system_arn")

    @property
    @pulumi.getter(name="sourceFileSystemId")
    def source_file_system_id(self) -> pulumi.Output[str]:
        """
        The ID of the file system that is to be replicated.
        """
        return pulumi.get(self, "source_file_system_id")

    @property
    @pulumi.getter(name="sourceFileSystemRegion")
    def source_file_system_region(self) -> pulumi.Output[str]:
        """
        The AWS Region in which the source Amazon EFS file system is located.
        """
        return pulumi.get(self, "source_file_system_region")

