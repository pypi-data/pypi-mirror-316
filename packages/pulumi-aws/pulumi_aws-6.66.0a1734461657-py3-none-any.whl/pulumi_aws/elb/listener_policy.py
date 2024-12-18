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

__all__ = ['ListenerPolicyArgs', 'ListenerPolicy']

@pulumi.input_type
class ListenerPolicyArgs:
    def __init__(__self__, *,
                 load_balancer_name: pulumi.Input[str],
                 load_balancer_port: pulumi.Input[int],
                 policy_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ListenerPolicy resource.
        :param pulumi.Input[str] load_balancer_name: The load balancer to attach the policy to.
        :param pulumi.Input[int] load_balancer_port: The load balancer listener port to apply the policy to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] policy_names: List of Policy Names to apply to the backend server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger an update.
        """
        pulumi.set(__self__, "load_balancer_name", load_balancer_name)
        pulumi.set(__self__, "load_balancer_port", load_balancer_port)
        if policy_names is not None:
            pulumi.set(__self__, "policy_names", policy_names)
        if triggers is not None:
            pulumi.set(__self__, "triggers", triggers)

    @property
    @pulumi.getter(name="loadBalancerName")
    def load_balancer_name(self) -> pulumi.Input[str]:
        """
        The load balancer to attach the policy to.
        """
        return pulumi.get(self, "load_balancer_name")

    @load_balancer_name.setter
    def load_balancer_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "load_balancer_name", value)

    @property
    @pulumi.getter(name="loadBalancerPort")
    def load_balancer_port(self) -> pulumi.Input[int]:
        """
        The load balancer listener port to apply the policy to.
        """
        return pulumi.get(self, "load_balancer_port")

    @load_balancer_port.setter
    def load_balancer_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "load_balancer_port", value)

    @property
    @pulumi.getter(name="policyNames")
    def policy_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Policy Names to apply to the backend server.
        """
        return pulumi.get(self, "policy_names")

    @policy_names.setter
    def policy_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "policy_names", value)

    @property
    @pulumi.getter
    def triggers(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger an update.
        """
        return pulumi.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "triggers", value)


@pulumi.input_type
class _ListenerPolicyState:
    def __init__(__self__, *,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 load_balancer_port: Optional[pulumi.Input[int]] = None,
                 policy_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering ListenerPolicy resources.
        :param pulumi.Input[str] load_balancer_name: The load balancer to attach the policy to.
        :param pulumi.Input[int] load_balancer_port: The load balancer listener port to apply the policy to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] policy_names: List of Policy Names to apply to the backend server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger an update.
        """
        if load_balancer_name is not None:
            pulumi.set(__self__, "load_balancer_name", load_balancer_name)
        if load_balancer_port is not None:
            pulumi.set(__self__, "load_balancer_port", load_balancer_port)
        if policy_names is not None:
            pulumi.set(__self__, "policy_names", policy_names)
        if triggers is not None:
            pulumi.set(__self__, "triggers", triggers)

    @property
    @pulumi.getter(name="loadBalancerName")
    def load_balancer_name(self) -> Optional[pulumi.Input[str]]:
        """
        The load balancer to attach the policy to.
        """
        return pulumi.get(self, "load_balancer_name")

    @load_balancer_name.setter
    def load_balancer_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "load_balancer_name", value)

    @property
    @pulumi.getter(name="loadBalancerPort")
    def load_balancer_port(self) -> Optional[pulumi.Input[int]]:
        """
        The load balancer listener port to apply the policy to.
        """
        return pulumi.get(self, "load_balancer_port")

    @load_balancer_port.setter
    def load_balancer_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "load_balancer_port", value)

    @property
    @pulumi.getter(name="policyNames")
    def policy_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Policy Names to apply to the backend server.
        """
        return pulumi.get(self, "policy_names")

    @policy_names.setter
    def policy_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "policy_names", value)

    @property
    @pulumi.getter
    def triggers(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger an update.
        """
        return pulumi.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "triggers", value)


class ListenerPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 load_balancer_port: Optional[pulumi.Input[int]] = None,
                 policy_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Attaches a load balancer policy to an ELB Listener.

        ## Example Usage

        ### Custom Policy

        ```python
        import pulumi
        import pulumi_aws as aws

        wu_tang = aws.elb.LoadBalancer("wu-tang",
            name="wu-tang",
            availability_zones=["us-east-1a"],
            listeners=[{
                "instance_port": 443,
                "instance_protocol": "http",
                "lb_port": 443,
                "lb_protocol": "https",
                "ssl_certificate_id": "arn:aws:iam::000000000000:server-certificate/wu-tang.net",
            }],
            tags={
                "Name": "wu-tang",
            })
        wu_tang_ssl = aws.elb.LoadBalancerPolicy("wu-tang-ssl",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ssl",
            policy_type_name="SSLNegotiationPolicyType",
            policy_attributes=[
                {
                    "name": "ECDHE-ECDSA-AES128-GCM-SHA256",
                    "value": "true",
                },
                {
                    "name": "Protocol-TLSv1.2",
                    "value": "true",
                },
            ])
        wu_tang_listener_policies_443 = aws.elb.ListenerPolicy("wu-tang-listener-policies-443",
            load_balancer_name=wu_tang.name,
            load_balancer_port=443,
            policy_names=[wu_tang_ssl.policy_name])
        ```

        This example shows how to customize the TLS settings of an HTTPS listener.

        ### AWS Predefined Security Policy

        ```python
        import pulumi
        import pulumi_aws as aws

        wu_tang = aws.elb.LoadBalancer("wu-tang",
            name="wu-tang",
            availability_zones=["us-east-1a"],
            listeners=[{
                "instance_port": 443,
                "instance_protocol": "http",
                "lb_port": 443,
                "lb_protocol": "https",
                "ssl_certificate_id": "arn:aws:iam::000000000000:server-certificate/wu-tang.net",
            }],
            tags={
                "Name": "wu-tang",
            })
        wu_tang_ssl_tls_1_1 = aws.elb.LoadBalancerPolicy("wu-tang-ssl-tls-1-1",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ssl",
            policy_type_name="SSLNegotiationPolicyType",
            policy_attributes=[{
                "name": "Reference-Security-Policy",
                "value": "ELBSecurityPolicy-TLS-1-1-2017-01",
            }])
        wu_tang_listener_policies_443 = aws.elb.ListenerPolicy("wu-tang-listener-policies-443",
            load_balancer_name=wu_tang.name,
            load_balancer_port=443,
            policy_names=[wu_tang_ssl_tls_1_1.policy_name])
        ```

        This example shows how to add a [Predefined Security Policy for ELBs](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-security-policy-table.html)

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] load_balancer_name: The load balancer to attach the policy to.
        :param pulumi.Input[int] load_balancer_port: The load balancer listener port to apply the policy to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] policy_names: List of Policy Names to apply to the backend server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger an update.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ListenerPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches a load balancer policy to an ELB Listener.

        ## Example Usage

        ### Custom Policy

        ```python
        import pulumi
        import pulumi_aws as aws

        wu_tang = aws.elb.LoadBalancer("wu-tang",
            name="wu-tang",
            availability_zones=["us-east-1a"],
            listeners=[{
                "instance_port": 443,
                "instance_protocol": "http",
                "lb_port": 443,
                "lb_protocol": "https",
                "ssl_certificate_id": "arn:aws:iam::000000000000:server-certificate/wu-tang.net",
            }],
            tags={
                "Name": "wu-tang",
            })
        wu_tang_ssl = aws.elb.LoadBalancerPolicy("wu-tang-ssl",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ssl",
            policy_type_name="SSLNegotiationPolicyType",
            policy_attributes=[
                {
                    "name": "ECDHE-ECDSA-AES128-GCM-SHA256",
                    "value": "true",
                },
                {
                    "name": "Protocol-TLSv1.2",
                    "value": "true",
                },
            ])
        wu_tang_listener_policies_443 = aws.elb.ListenerPolicy("wu-tang-listener-policies-443",
            load_balancer_name=wu_tang.name,
            load_balancer_port=443,
            policy_names=[wu_tang_ssl.policy_name])
        ```

        This example shows how to customize the TLS settings of an HTTPS listener.

        ### AWS Predefined Security Policy

        ```python
        import pulumi
        import pulumi_aws as aws

        wu_tang = aws.elb.LoadBalancer("wu-tang",
            name="wu-tang",
            availability_zones=["us-east-1a"],
            listeners=[{
                "instance_port": 443,
                "instance_protocol": "http",
                "lb_port": 443,
                "lb_protocol": "https",
                "ssl_certificate_id": "arn:aws:iam::000000000000:server-certificate/wu-tang.net",
            }],
            tags={
                "Name": "wu-tang",
            })
        wu_tang_ssl_tls_1_1 = aws.elb.LoadBalancerPolicy("wu-tang-ssl-tls-1-1",
            load_balancer_name=wu_tang.name,
            policy_name="wu-tang-ssl",
            policy_type_name="SSLNegotiationPolicyType",
            policy_attributes=[{
                "name": "Reference-Security-Policy",
                "value": "ELBSecurityPolicy-TLS-1-1-2017-01",
            }])
        wu_tang_listener_policies_443 = aws.elb.ListenerPolicy("wu-tang-listener-policies-443",
            load_balancer_name=wu_tang.name,
            load_balancer_port=443,
            policy_names=[wu_tang_ssl_tls_1_1.policy_name])
        ```

        This example shows how to add a [Predefined Security Policy for ELBs](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-security-policy-table.html)

        :param str resource_name: The name of the resource.
        :param ListenerPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ListenerPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 load_balancer_port: Optional[pulumi.Input[int]] = None,
                 policy_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ListenerPolicyArgs.__new__(ListenerPolicyArgs)

            if load_balancer_name is None and not opts.urn:
                raise TypeError("Missing required property 'load_balancer_name'")
            __props__.__dict__["load_balancer_name"] = load_balancer_name
            if load_balancer_port is None and not opts.urn:
                raise TypeError("Missing required property 'load_balancer_port'")
            __props__.__dict__["load_balancer_port"] = load_balancer_port
            __props__.__dict__["policy_names"] = policy_names
            __props__.__dict__["triggers"] = triggers
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="aws:elasticloadbalancing/listenerPolicy:ListenerPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ListenerPolicy, __self__).__init__(
            'aws:elb/listenerPolicy:ListenerPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            load_balancer_name: Optional[pulumi.Input[str]] = None,
            load_balancer_port: Optional[pulumi.Input[int]] = None,
            policy_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'ListenerPolicy':
        """
        Get an existing ListenerPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] load_balancer_name: The load balancer to attach the policy to.
        :param pulumi.Input[int] load_balancer_port: The load balancer listener port to apply the policy to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] policy_names: List of Policy Names to apply to the backend server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger an update.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ListenerPolicyState.__new__(_ListenerPolicyState)

        __props__.__dict__["load_balancer_name"] = load_balancer_name
        __props__.__dict__["load_balancer_port"] = load_balancer_port
        __props__.__dict__["policy_names"] = policy_names
        __props__.__dict__["triggers"] = triggers
        return ListenerPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="loadBalancerName")
    def load_balancer_name(self) -> pulumi.Output[str]:
        """
        The load balancer to attach the policy to.
        """
        return pulumi.get(self, "load_balancer_name")

    @property
    @pulumi.getter(name="loadBalancerPort")
    def load_balancer_port(self) -> pulumi.Output[int]:
        """
        The load balancer listener port to apply the policy to.
        """
        return pulumi.get(self, "load_balancer_port")

    @property
    @pulumi.getter(name="policyNames")
    def policy_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of Policy Names to apply to the backend server.
        """
        return pulumi.get(self, "policy_names")

    @property
    @pulumi.getter
    def triggers(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger an update.
        """
        return pulumi.get(self, "triggers")

