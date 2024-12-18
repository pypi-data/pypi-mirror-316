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

__all__ = ['KinesisStreamingDestinationArgs', 'KinesisStreamingDestination']

@pulumi.input_type
class KinesisStreamingDestinationArgs:
    def __init__(__self__, *,
                 stream_arn: pulumi.Input[str],
                 table_name: pulumi.Input[str],
                 approximate_creation_date_time_precision: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a KinesisStreamingDestination resource.
        :param pulumi.Input[str] stream_arn: The ARN for a Kinesis data stream. This must exist in the same account and region as the DynamoDB table.
        :param pulumi.Input[str] table_name: The name of the DynamoDB table. There can only be one Kinesis streaming destination for a given DynamoDB table.
        :param pulumi.Input[str] approximate_creation_date_time_precision: Toggle for the precision of Kinesis data stream timestamp. Valid values: `MILLISECOND` and `MICROSECOND`.
        """
        pulumi.set(__self__, "stream_arn", stream_arn)
        pulumi.set(__self__, "table_name", table_name)
        if approximate_creation_date_time_precision is not None:
            pulumi.set(__self__, "approximate_creation_date_time_precision", approximate_creation_date_time_precision)

    @property
    @pulumi.getter(name="streamArn")
    def stream_arn(self) -> pulumi.Input[str]:
        """
        The ARN for a Kinesis data stream. This must exist in the same account and region as the DynamoDB table.
        """
        return pulumi.get(self, "stream_arn")

    @stream_arn.setter
    def stream_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "stream_arn", value)

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> pulumi.Input[str]:
        """
        The name of the DynamoDB table. There can only be one Kinesis streaming destination for a given DynamoDB table.
        """
        return pulumi.get(self, "table_name")

    @table_name.setter
    def table_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "table_name", value)

    @property
    @pulumi.getter(name="approximateCreationDateTimePrecision")
    def approximate_creation_date_time_precision(self) -> Optional[pulumi.Input[str]]:
        """
        Toggle for the precision of Kinesis data stream timestamp. Valid values: `MILLISECOND` and `MICROSECOND`.
        """
        return pulumi.get(self, "approximate_creation_date_time_precision")

    @approximate_creation_date_time_precision.setter
    def approximate_creation_date_time_precision(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "approximate_creation_date_time_precision", value)


@pulumi.input_type
class _KinesisStreamingDestinationState:
    def __init__(__self__, *,
                 approximate_creation_date_time_precision: Optional[pulumi.Input[str]] = None,
                 stream_arn: Optional[pulumi.Input[str]] = None,
                 table_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering KinesisStreamingDestination resources.
        :param pulumi.Input[str] approximate_creation_date_time_precision: Toggle for the precision of Kinesis data stream timestamp. Valid values: `MILLISECOND` and `MICROSECOND`.
        :param pulumi.Input[str] stream_arn: The ARN for a Kinesis data stream. This must exist in the same account and region as the DynamoDB table.
        :param pulumi.Input[str] table_name: The name of the DynamoDB table. There can only be one Kinesis streaming destination for a given DynamoDB table.
        """
        if approximate_creation_date_time_precision is not None:
            pulumi.set(__self__, "approximate_creation_date_time_precision", approximate_creation_date_time_precision)
        if stream_arn is not None:
            pulumi.set(__self__, "stream_arn", stream_arn)
        if table_name is not None:
            pulumi.set(__self__, "table_name", table_name)

    @property
    @pulumi.getter(name="approximateCreationDateTimePrecision")
    def approximate_creation_date_time_precision(self) -> Optional[pulumi.Input[str]]:
        """
        Toggle for the precision of Kinesis data stream timestamp. Valid values: `MILLISECOND` and `MICROSECOND`.
        """
        return pulumi.get(self, "approximate_creation_date_time_precision")

    @approximate_creation_date_time_precision.setter
    def approximate_creation_date_time_precision(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "approximate_creation_date_time_precision", value)

    @property
    @pulumi.getter(name="streamArn")
    def stream_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN for a Kinesis data stream. This must exist in the same account and region as the DynamoDB table.
        """
        return pulumi.get(self, "stream_arn")

    @stream_arn.setter
    def stream_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stream_arn", value)

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the DynamoDB table. There can only be one Kinesis streaming destination for a given DynamoDB table.
        """
        return pulumi.get(self, "table_name")

    @table_name.setter
    def table_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table_name", value)


class KinesisStreamingDestination(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 approximate_creation_date_time_precision: Optional[pulumi.Input[str]] = None,
                 stream_arn: Optional[pulumi.Input[str]] = None,
                 table_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Enables a [Kinesis streaming destination](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/kds.html) for data replication of a DynamoDB table.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.dynamodb.Table("example",
            name="orders",
            hash_key="id",
            attributes=[{
                "name": "id",
                "type": "S",
            }])
        example_stream = aws.kinesis.Stream("example",
            name="order_item_changes",
            shard_count=1)
        example_kinesis_streaming_destination = aws.dynamodb.KinesisStreamingDestination("example",
            stream_arn=example_stream.arn,
            table_name=example.name,
            approximate_creation_date_time_precision="MICROSECOND")
        ```

        ## Import

        Using `pulumi import`, import DynamoDB Kinesis Streaming Destinations using the `table_name` and `stream_arn` separated by `,`. For example:

        ```sh
        $ pulumi import aws:dynamodb/kinesisStreamingDestination:KinesisStreamingDestination example example,arn:aws:kinesis:us-east-1:111122223333:exampleStreamName
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] approximate_creation_date_time_precision: Toggle for the precision of Kinesis data stream timestamp. Valid values: `MILLISECOND` and `MICROSECOND`.
        :param pulumi.Input[str] stream_arn: The ARN for a Kinesis data stream. This must exist in the same account and region as the DynamoDB table.
        :param pulumi.Input[str] table_name: The name of the DynamoDB table. There can only be one Kinesis streaming destination for a given DynamoDB table.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KinesisStreamingDestinationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Enables a [Kinesis streaming destination](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/kds.html) for data replication of a DynamoDB table.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.dynamodb.Table("example",
            name="orders",
            hash_key="id",
            attributes=[{
                "name": "id",
                "type": "S",
            }])
        example_stream = aws.kinesis.Stream("example",
            name="order_item_changes",
            shard_count=1)
        example_kinesis_streaming_destination = aws.dynamodb.KinesisStreamingDestination("example",
            stream_arn=example_stream.arn,
            table_name=example.name,
            approximate_creation_date_time_precision="MICROSECOND")
        ```

        ## Import

        Using `pulumi import`, import DynamoDB Kinesis Streaming Destinations using the `table_name` and `stream_arn` separated by `,`. For example:

        ```sh
        $ pulumi import aws:dynamodb/kinesisStreamingDestination:KinesisStreamingDestination example example,arn:aws:kinesis:us-east-1:111122223333:exampleStreamName
        ```

        :param str resource_name: The name of the resource.
        :param KinesisStreamingDestinationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KinesisStreamingDestinationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 approximate_creation_date_time_precision: Optional[pulumi.Input[str]] = None,
                 stream_arn: Optional[pulumi.Input[str]] = None,
                 table_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KinesisStreamingDestinationArgs.__new__(KinesisStreamingDestinationArgs)

            __props__.__dict__["approximate_creation_date_time_precision"] = approximate_creation_date_time_precision
            if stream_arn is None and not opts.urn:
                raise TypeError("Missing required property 'stream_arn'")
            __props__.__dict__["stream_arn"] = stream_arn
            if table_name is None and not opts.urn:
                raise TypeError("Missing required property 'table_name'")
            __props__.__dict__["table_name"] = table_name
        super(KinesisStreamingDestination, __self__).__init__(
            'aws:dynamodb/kinesisStreamingDestination:KinesisStreamingDestination',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            approximate_creation_date_time_precision: Optional[pulumi.Input[str]] = None,
            stream_arn: Optional[pulumi.Input[str]] = None,
            table_name: Optional[pulumi.Input[str]] = None) -> 'KinesisStreamingDestination':
        """
        Get an existing KinesisStreamingDestination resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] approximate_creation_date_time_precision: Toggle for the precision of Kinesis data stream timestamp. Valid values: `MILLISECOND` and `MICROSECOND`.
        :param pulumi.Input[str] stream_arn: The ARN for a Kinesis data stream. This must exist in the same account and region as the DynamoDB table.
        :param pulumi.Input[str] table_name: The name of the DynamoDB table. There can only be one Kinesis streaming destination for a given DynamoDB table.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KinesisStreamingDestinationState.__new__(_KinesisStreamingDestinationState)

        __props__.__dict__["approximate_creation_date_time_precision"] = approximate_creation_date_time_precision
        __props__.__dict__["stream_arn"] = stream_arn
        __props__.__dict__["table_name"] = table_name
        return KinesisStreamingDestination(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="approximateCreationDateTimePrecision")
    def approximate_creation_date_time_precision(self) -> pulumi.Output[str]:
        """
        Toggle for the precision of Kinesis data stream timestamp. Valid values: `MILLISECOND` and `MICROSECOND`.
        """
        return pulumi.get(self, "approximate_creation_date_time_precision")

    @property
    @pulumi.getter(name="streamArn")
    def stream_arn(self) -> pulumi.Output[str]:
        """
        The ARN for a Kinesis data stream. This must exist in the same account and region as the DynamoDB table.
        """
        return pulumi.get(self, "stream_arn")

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> pulumi.Output[str]:
        """
        The name of the DynamoDB table. There can only be one Kinesis streaming destination for a given DynamoDB table.
        """
        return pulumi.get(self, "table_name")

