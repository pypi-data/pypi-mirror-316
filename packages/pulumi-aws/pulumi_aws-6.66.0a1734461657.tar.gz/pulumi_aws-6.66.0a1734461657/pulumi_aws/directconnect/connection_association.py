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

__all__ = ['ConnectionAssociationArgs', 'ConnectionAssociation']

@pulumi.input_type
class ConnectionAssociationArgs:
    def __init__(__self__, *,
                 connection_id: pulumi.Input[str],
                 lag_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a ConnectionAssociation resource.
        :param pulumi.Input[str] connection_id: The ID of the connection.
        :param pulumi.Input[str] lag_id: The ID of the LAG with which to associate the connection.
        """
        pulumi.set(__self__, "connection_id", connection_id)
        pulumi.set(__self__, "lag_id", lag_id)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> pulumi.Input[str]:
        """
        The ID of the connection.
        """
        return pulumi.get(self, "connection_id")

    @connection_id.setter
    def connection_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "connection_id", value)

    @property
    @pulumi.getter(name="lagId")
    def lag_id(self) -> pulumi.Input[str]:
        """
        The ID of the LAG with which to associate the connection.
        """
        return pulumi.get(self, "lag_id")

    @lag_id.setter
    def lag_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "lag_id", value)


@pulumi.input_type
class _ConnectionAssociationState:
    def __init__(__self__, *,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 lag_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ConnectionAssociation resources.
        :param pulumi.Input[str] connection_id: The ID of the connection.
        :param pulumi.Input[str] lag_id: The ID of the LAG with which to associate the connection.
        """
        if connection_id is not None:
            pulumi.set(__self__, "connection_id", connection_id)
        if lag_id is not None:
            pulumi.set(__self__, "lag_id", lag_id)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the connection.
        """
        return pulumi.get(self, "connection_id")

    @connection_id.setter
    def connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_id", value)

    @property
    @pulumi.getter(name="lagId")
    def lag_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the LAG with which to associate the connection.
        """
        return pulumi.get(self, "lag_id")

    @lag_id.setter
    def lag_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lag_id", value)


class ConnectionAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 lag_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Associates a Direct Connect Connection with a LAG.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.directconnect.Connection("example",
            name="example",
            bandwidth="1Gbps",
            location="EqSe2-EQ")
        example_link_aggregation_group = aws.directconnect.LinkAggregationGroup("example",
            name="example",
            connections_bandwidth="1Gbps",
            location="EqSe2-EQ")
        example_connection_association = aws.directconnect.ConnectionAssociation("example",
            connection_id=example.id,
            lag_id=example_link_aggregation_group.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_id: The ID of the connection.
        :param pulumi.Input[str] lag_id: The ID of the LAG with which to associate the connection.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConnectionAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Associates a Direct Connect Connection with a LAG.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.directconnect.Connection("example",
            name="example",
            bandwidth="1Gbps",
            location="EqSe2-EQ")
        example_link_aggregation_group = aws.directconnect.LinkAggregationGroup("example",
            name="example",
            connections_bandwidth="1Gbps",
            location="EqSe2-EQ")
        example_connection_association = aws.directconnect.ConnectionAssociation("example",
            connection_id=example.id,
            lag_id=example_link_aggregation_group.id)
        ```

        :param str resource_name: The name of the resource.
        :param ConnectionAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectionAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 lag_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectionAssociationArgs.__new__(ConnectionAssociationArgs)

            if connection_id is None and not opts.urn:
                raise TypeError("Missing required property 'connection_id'")
            __props__.__dict__["connection_id"] = connection_id
            if lag_id is None and not opts.urn:
                raise TypeError("Missing required property 'lag_id'")
            __props__.__dict__["lag_id"] = lag_id
        super(ConnectionAssociation, __self__).__init__(
            'aws:directconnect/connectionAssociation:ConnectionAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            connection_id: Optional[pulumi.Input[str]] = None,
            lag_id: Optional[pulumi.Input[str]] = None) -> 'ConnectionAssociation':
        """
        Get an existing ConnectionAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_id: The ID of the connection.
        :param pulumi.Input[str] lag_id: The ID of the LAG with which to associate the connection.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConnectionAssociationState.__new__(_ConnectionAssociationState)

        __props__.__dict__["connection_id"] = connection_id
        __props__.__dict__["lag_id"] = lag_id
        return ConnectionAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> pulumi.Output[str]:
        """
        The ID of the connection.
        """
        return pulumi.get(self, "connection_id")

    @property
    @pulumi.getter(name="lagId")
    def lag_id(self) -> pulumi.Output[str]:
        """
        The ID of the LAG with which to associate the connection.
        """
        return pulumi.get(self, "lag_id")

