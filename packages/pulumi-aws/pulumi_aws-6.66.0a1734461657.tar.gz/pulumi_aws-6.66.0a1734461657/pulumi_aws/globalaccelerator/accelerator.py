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

__all__ = ['AcceleratorArgs', 'Accelerator']

@pulumi.input_type
class AcceleratorArgs:
    def __init__(__self__, *,
                 attributes: Optional[pulumi.Input['AcceleratorAttributesArgs']] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 ip_address_type: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Accelerator resource.
        :param pulumi.Input['AcceleratorAttributesArgs'] attributes: The attributes of the accelerator. Fields documented below.
        :param pulumi.Input[bool] enabled: Indicates whether the accelerator is enabled. Defaults to `true`. Valid values: `true`, `false`.
        :param pulumi.Input[str] ip_address_type: The value for the address type. Defaults to `IPV4`. Valid values: `IPV4`, `DUAL_STACK`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        :param pulumi.Input[str] name: The name of the accelerator.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if attributes is not None:
            pulumi.set(__self__, "attributes", attributes)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if ip_address_type is not None:
            pulumi.set(__self__, "ip_address_type", ip_address_type)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def attributes(self) -> Optional[pulumi.Input['AcceleratorAttributesArgs']]:
        """
        The attributes of the accelerator. Fields documented below.
        """
        return pulumi.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: Optional[pulumi.Input['AcceleratorAttributesArgs']]):
        pulumi.set(self, "attributes", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the accelerator is enabled. Defaults to `true`. Valid values: `true`, `false`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> Optional[pulumi.Input[str]]:
        """
        The value for the address type. Defaults to `IPV4`. Valid values: `IPV4`, `DUAL_STACK`.
        """
        return pulumi.get(self, "ip_address_type")

    @ip_address_type.setter
    def ip_address_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address_type", value)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the accelerator.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AcceleratorState:
    def __init__(__self__, *,
                 attributes: Optional[pulumi.Input['AcceleratorAttributesArgs']] = None,
                 dns_name: Optional[pulumi.Input[str]] = None,
                 dual_stack_dns_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 hosted_zone_id: Optional[pulumi.Input[str]] = None,
                 ip_address_type: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_sets: Optional[pulumi.Input[Sequence[pulumi.Input['AcceleratorIpSetArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Accelerator resources.
        :param pulumi.Input['AcceleratorAttributesArgs'] attributes: The attributes of the accelerator. Fields documented below.
        :param pulumi.Input[str] dns_name: The DNS name of the accelerator. For example, `a5d53ff5ee6bca4ce.awsglobalaccelerator.com`.
        :param pulumi.Input[str] dual_stack_dns_name: The Domain Name System (DNS) name that Global Accelerator creates that points to a dual-stack accelerator's four static IP addresses: two IPv4 addresses and two IPv6 addresses. For example, `a1234567890abcdef.dualstack.awsglobalaccelerator.com`.
        :param pulumi.Input[bool] enabled: Indicates whether the accelerator is enabled. Defaults to `true`. Valid values: `true`, `false`.
        :param pulumi.Input[str] hosted_zone_id: -  The Global Accelerator Route 53 zone ID that can be used to
               route an [Alias Resource Record Set](https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html) to the Global Accelerator. This attribute
               is simply an alias for the zone ID `Z2BJ6XQ5FK7U4H`.
        :param pulumi.Input[str] ip_address_type: The value for the address type. Defaults to `IPV4`. Valid values: `IPV4`, `DUAL_STACK`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        :param pulumi.Input[Sequence[pulumi.Input['AcceleratorIpSetArgs']]] ip_sets: IP address set associated with the accelerator.
        :param pulumi.Input[str] name: The name of the accelerator.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if attributes is not None:
            pulumi.set(__self__, "attributes", attributes)
        if dns_name is not None:
            pulumi.set(__self__, "dns_name", dns_name)
        if dual_stack_dns_name is not None:
            pulumi.set(__self__, "dual_stack_dns_name", dual_stack_dns_name)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if hosted_zone_id is not None:
            pulumi.set(__self__, "hosted_zone_id", hosted_zone_id)
        if ip_address_type is not None:
            pulumi.set(__self__, "ip_address_type", ip_address_type)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if ip_sets is not None:
            pulumi.set(__self__, "ip_sets", ip_sets)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def attributes(self) -> Optional[pulumi.Input['AcceleratorAttributesArgs']]:
        """
        The attributes of the accelerator. Fields documented below.
        """
        return pulumi.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: Optional[pulumi.Input['AcceleratorAttributesArgs']]):
        pulumi.set(self, "attributes", value)

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> Optional[pulumi.Input[str]]:
        """
        The DNS name of the accelerator. For example, `a5d53ff5ee6bca4ce.awsglobalaccelerator.com`.
        """
        return pulumi.get(self, "dns_name")

    @dns_name.setter
    def dns_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_name", value)

    @property
    @pulumi.getter(name="dualStackDnsName")
    def dual_stack_dns_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Domain Name System (DNS) name that Global Accelerator creates that points to a dual-stack accelerator's four static IP addresses: two IPv4 addresses and two IPv6 addresses. For example, `a1234567890abcdef.dualstack.awsglobalaccelerator.com`.
        """
        return pulumi.get(self, "dual_stack_dns_name")

    @dual_stack_dns_name.setter
    def dual_stack_dns_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dual_stack_dns_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the accelerator is enabled. Defaults to `true`. Valid values: `true`, `false`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        -  The Global Accelerator Route 53 zone ID that can be used to
        route an [Alias Resource Record Set](https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html) to the Global Accelerator. This attribute
        is simply an alias for the zone ID `Z2BJ6XQ5FK7U4H`.
        """
        return pulumi.get(self, "hosted_zone_id")

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hosted_zone_id", value)

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> Optional[pulumi.Input[str]]:
        """
        The value for the address type. Defaults to `IPV4`. Valid values: `IPV4`, `DUAL_STACK`.
        """
        return pulumi.get(self, "ip_address_type")

    @ip_address_type.setter
    def ip_address_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address_type", value)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)

    @property
    @pulumi.getter(name="ipSets")
    def ip_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AcceleratorIpSetArgs']]]]:
        """
        IP address set associated with the accelerator.
        """
        return pulumi.get(self, "ip_sets")

    @ip_sets.setter
    def ip_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AcceleratorIpSetArgs']]]]):
        pulumi.set(self, "ip_sets", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the accelerator.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    @_utilities.deprecated("""Please use `tags` instead.""")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class Accelerator(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attributes: Optional[pulumi.Input[Union['AcceleratorAttributesArgs', 'AcceleratorAttributesArgsDict']]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 ip_address_type: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Creates a Global Accelerator accelerator.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.globalaccelerator.Accelerator("example",
            name="Example",
            ip_address_type="IPV4",
            ip_addresses=["1.2.3.4"],
            enabled=True,
            attributes={
                "flow_logs_enabled": True,
                "flow_logs_s3_bucket": "example-bucket",
                "flow_logs_s3_prefix": "flow-logs/",
            })
        ```

        ## Import

        Using `pulumi import`, import Global Accelerator accelerators using the `arn`. For example:

        ```sh
        $ pulumi import aws:globalaccelerator/accelerator:Accelerator example arn:aws:globalaccelerator::111111111111:accelerator/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['AcceleratorAttributesArgs', 'AcceleratorAttributesArgsDict']] attributes: The attributes of the accelerator. Fields documented below.
        :param pulumi.Input[bool] enabled: Indicates whether the accelerator is enabled. Defaults to `true`. Valid values: `true`, `false`.
        :param pulumi.Input[str] ip_address_type: The value for the address type. Defaults to `IPV4`. Valid values: `IPV4`, `DUAL_STACK`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        :param pulumi.Input[str] name: The name of the accelerator.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AcceleratorArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a Global Accelerator accelerator.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.globalaccelerator.Accelerator("example",
            name="Example",
            ip_address_type="IPV4",
            ip_addresses=["1.2.3.4"],
            enabled=True,
            attributes={
                "flow_logs_enabled": True,
                "flow_logs_s3_bucket": "example-bucket",
                "flow_logs_s3_prefix": "flow-logs/",
            })
        ```

        ## Import

        Using `pulumi import`, import Global Accelerator accelerators using the `arn`. For example:

        ```sh
        $ pulumi import aws:globalaccelerator/accelerator:Accelerator example arn:aws:globalaccelerator::111111111111:accelerator/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        ```

        :param str resource_name: The name of the resource.
        :param AcceleratorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AcceleratorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attributes: Optional[pulumi.Input[Union['AcceleratorAttributesArgs', 'AcceleratorAttributesArgsDict']]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 ip_address_type: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AcceleratorArgs.__new__(AcceleratorArgs)

            __props__.__dict__["attributes"] = attributes
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["ip_address_type"] = ip_address_type
            __props__.__dict__["ip_addresses"] = ip_addresses
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["dns_name"] = None
            __props__.__dict__["dual_stack_dns_name"] = None
            __props__.__dict__["hosted_zone_id"] = None
            __props__.__dict__["ip_sets"] = None
            __props__.__dict__["tags_all"] = None
        super(Accelerator, __self__).__init__(
            'aws:globalaccelerator/accelerator:Accelerator',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attributes: Optional[pulumi.Input[Union['AcceleratorAttributesArgs', 'AcceleratorAttributesArgsDict']]] = None,
            dns_name: Optional[pulumi.Input[str]] = None,
            dual_stack_dns_name: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            hosted_zone_id: Optional[pulumi.Input[str]] = None,
            ip_address_type: Optional[pulumi.Input[str]] = None,
            ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            ip_sets: Optional[pulumi.Input[Sequence[pulumi.Input[Union['AcceleratorIpSetArgs', 'AcceleratorIpSetArgsDict']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Accelerator':
        """
        Get an existing Accelerator resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['AcceleratorAttributesArgs', 'AcceleratorAttributesArgsDict']] attributes: The attributes of the accelerator. Fields documented below.
        :param pulumi.Input[str] dns_name: The DNS name of the accelerator. For example, `a5d53ff5ee6bca4ce.awsglobalaccelerator.com`.
        :param pulumi.Input[str] dual_stack_dns_name: The Domain Name System (DNS) name that Global Accelerator creates that points to a dual-stack accelerator's four static IP addresses: two IPv4 addresses and two IPv6 addresses. For example, `a1234567890abcdef.dualstack.awsglobalaccelerator.com`.
        :param pulumi.Input[bool] enabled: Indicates whether the accelerator is enabled. Defaults to `true`. Valid values: `true`, `false`.
        :param pulumi.Input[str] hosted_zone_id: -  The Global Accelerator Route 53 zone ID that can be used to
               route an [Alias Resource Record Set](https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html) to the Global Accelerator. This attribute
               is simply an alias for the zone ID `Z2BJ6XQ5FK7U4H`.
        :param pulumi.Input[str] ip_address_type: The value for the address type. Defaults to `IPV4`. Valid values: `IPV4`, `DUAL_STACK`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        :param pulumi.Input[Sequence[pulumi.Input[Union['AcceleratorIpSetArgs', 'AcceleratorIpSetArgsDict']]]] ip_sets: IP address set associated with the accelerator.
        :param pulumi.Input[str] name: The name of the accelerator.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AcceleratorState.__new__(_AcceleratorState)

        __props__.__dict__["attributes"] = attributes
        __props__.__dict__["dns_name"] = dns_name
        __props__.__dict__["dual_stack_dns_name"] = dual_stack_dns_name
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["hosted_zone_id"] = hosted_zone_id
        __props__.__dict__["ip_address_type"] = ip_address_type
        __props__.__dict__["ip_addresses"] = ip_addresses
        __props__.__dict__["ip_sets"] = ip_sets
        __props__.__dict__["name"] = name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Accelerator(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def attributes(self) -> pulumi.Output[Optional['outputs.AcceleratorAttributes']]:
        """
        The attributes of the accelerator. Fields documented below.
        """
        return pulumi.get(self, "attributes")

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> pulumi.Output[str]:
        """
        The DNS name of the accelerator. For example, `a5d53ff5ee6bca4ce.awsglobalaccelerator.com`.
        """
        return pulumi.get(self, "dns_name")

    @property
    @pulumi.getter(name="dualStackDnsName")
    def dual_stack_dns_name(self) -> pulumi.Output[str]:
        """
        The Domain Name System (DNS) name that Global Accelerator creates that points to a dual-stack accelerator's four static IP addresses: two IPv4 addresses and two IPv6 addresses. For example, `a1234567890abcdef.dualstack.awsglobalaccelerator.com`.
        """
        return pulumi.get(self, "dual_stack_dns_name")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether the accelerator is enabled. Defaults to `true`. Valid values: `true`, `false`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> pulumi.Output[str]:
        """
        -  The Global Accelerator Route 53 zone ID that can be used to
        route an [Alias Resource Record Set](https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html) to the Global Accelerator. This attribute
        is simply an alias for the zone ID `Z2BJ6XQ5FK7U4H`.
        """
        return pulumi.get(self, "hosted_zone_id")

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> pulumi.Output[Optional[str]]:
        """
        The value for the address type. Defaults to `IPV4`. Valid values: `IPV4`, `DUAL_STACK`.
        """
        return pulumi.get(self, "ip_address_type")

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The IP addresses to use for BYOIP accelerators. If not specified, the service assigns IP addresses. Valid values: 1 or 2 IPv4 addresses.
        """
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter(name="ipSets")
    def ip_sets(self) -> pulumi.Output[Sequence['outputs.AcceleratorIpSet']]:
        """
        IP address set associated with the accelerator.
        """
        return pulumi.get(self, "ip_sets")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the accelerator.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    @_utilities.deprecated("""Please use `tags` instead.""")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

