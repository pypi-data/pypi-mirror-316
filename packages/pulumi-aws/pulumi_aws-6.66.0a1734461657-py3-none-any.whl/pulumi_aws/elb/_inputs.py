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

__all__ = [
    'LoadBalancerAccessLogsArgs',
    'LoadBalancerAccessLogsArgsDict',
    'LoadBalancerHealthCheckArgs',
    'LoadBalancerHealthCheckArgsDict',
    'LoadBalancerListenerArgs',
    'LoadBalancerListenerArgsDict',
    'LoadBalancerPolicyPolicyAttributeArgs',
    'LoadBalancerPolicyPolicyAttributeArgsDict',
    'SslNegotiationPolicyAttributeArgs',
    'SslNegotiationPolicyAttributeArgsDict',
]

MYPY = False

if not MYPY:
    class LoadBalancerAccessLogsArgsDict(TypedDict):
        bucket: pulumi.Input[str]
        """
        The S3 bucket name to store the logs in.
        """
        bucket_prefix: NotRequired[pulumi.Input[str]]
        """
        The S3 bucket prefix. Logs are stored in the root if not configured.
        """
        enabled: NotRequired[pulumi.Input[bool]]
        """
        Boolean to enable / disable `access_logs`. Default is `true`
        """
        interval: NotRequired[pulumi.Input[int]]
        """
        The publishing interval in minutes. Valid values: `5` and `60`. Default: `60`
        """
elif False:
    LoadBalancerAccessLogsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LoadBalancerAccessLogsArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 bucket_prefix: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 interval: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] bucket: The S3 bucket name to store the logs in.
        :param pulumi.Input[str] bucket_prefix: The S3 bucket prefix. Logs are stored in the root if not configured.
        :param pulumi.Input[bool] enabled: Boolean to enable / disable `access_logs`. Default is `true`
        :param pulumi.Input[int] interval: The publishing interval in minutes. Valid values: `5` and `60`. Default: `60`
        """
        pulumi.set(__self__, "bucket", bucket)
        if bucket_prefix is not None:
            pulumi.set(__self__, "bucket_prefix", bucket_prefix)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        The S3 bucket name to store the logs in.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The S3 bucket prefix. Logs are stored in the root if not configured.
        """
        return pulumi.get(self, "bucket_prefix")

    @bucket_prefix.setter
    def bucket_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_prefix", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean to enable / disable `access_logs`. Default is `true`
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        """
        The publishing interval in minutes. Valid values: `5` and `60`. Default: `60`
        """
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)


if not MYPY:
    class LoadBalancerHealthCheckArgsDict(TypedDict):
        healthy_threshold: pulumi.Input[int]
        """
        The number of checks before the instance is declared healthy.
        """
        interval: pulumi.Input[int]
        """
        The interval between checks.
        """
        target: pulumi.Input[str]
        """
        The target of the check. Valid pattern is "${PROTOCOL}:${PORT}${PATH}", where PROTOCOL
        values are:
        * `HTTP`, `HTTPS` - PORT and PATH are required
        * `TCP`, `SSL` - PORT is required, PATH is not supported
        """
        timeout: pulumi.Input[int]
        """
        The length of time before the check times out.
        """
        unhealthy_threshold: pulumi.Input[int]
        """
        The number of checks before the instance is declared unhealthy.
        """
elif False:
    LoadBalancerHealthCheckArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LoadBalancerHealthCheckArgs:
    def __init__(__self__, *,
                 healthy_threshold: pulumi.Input[int],
                 interval: pulumi.Input[int],
                 target: pulumi.Input[str],
                 timeout: pulumi.Input[int],
                 unhealthy_threshold: pulumi.Input[int]):
        """
        :param pulumi.Input[int] healthy_threshold: The number of checks before the instance is declared healthy.
        :param pulumi.Input[int] interval: The interval between checks.
        :param pulumi.Input[str] target: The target of the check. Valid pattern is "${PROTOCOL}:${PORT}${PATH}", where PROTOCOL
               values are:
               * `HTTP`, `HTTPS` - PORT and PATH are required
               * `TCP`, `SSL` - PORT is required, PATH is not supported
        :param pulumi.Input[int] timeout: The length of time before the check times out.
        :param pulumi.Input[int] unhealthy_threshold: The number of checks before the instance is declared unhealthy.
        """
        pulumi.set(__self__, "healthy_threshold", healthy_threshold)
        pulumi.set(__self__, "interval", interval)
        pulumi.set(__self__, "target", target)
        pulumi.set(__self__, "timeout", timeout)
        pulumi.set(__self__, "unhealthy_threshold", unhealthy_threshold)

    @property
    @pulumi.getter(name="healthyThreshold")
    def healthy_threshold(self) -> pulumi.Input[int]:
        """
        The number of checks before the instance is declared healthy.
        """
        return pulumi.get(self, "healthy_threshold")

    @healthy_threshold.setter
    def healthy_threshold(self, value: pulumi.Input[int]):
        pulumi.set(self, "healthy_threshold", value)

    @property
    @pulumi.getter
    def interval(self) -> pulumi.Input[int]:
        """
        The interval between checks.
        """
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: pulumi.Input[int]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        """
        The target of the check. Valid pattern is "${PROTOCOL}:${PORT}${PATH}", where PROTOCOL
        values are:
        * `HTTP`, `HTTPS` - PORT and PATH are required
        * `TCP`, `SSL` - PORT is required, PATH is not supported
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter
    def timeout(self) -> pulumi.Input[int]:
        """
        The length of time before the check times out.
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: pulumi.Input[int]):
        pulumi.set(self, "timeout", value)

    @property
    @pulumi.getter(name="unhealthyThreshold")
    def unhealthy_threshold(self) -> pulumi.Input[int]:
        """
        The number of checks before the instance is declared unhealthy.
        """
        return pulumi.get(self, "unhealthy_threshold")

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: pulumi.Input[int]):
        pulumi.set(self, "unhealthy_threshold", value)


if not MYPY:
    class LoadBalancerListenerArgsDict(TypedDict):
        instance_port: pulumi.Input[int]
        """
        The port on the instance to route to
        """
        instance_protocol: pulumi.Input[str]
        """
        The protocol to use to the instance. Valid
        values are `HTTP`, `HTTPS`, `TCP`, or `SSL`
        """
        lb_port: pulumi.Input[int]
        """
        The port to listen on for the load balancer
        """
        lb_protocol: pulumi.Input[str]
        """
        The protocol to listen on. Valid values are `HTTP`,
        `HTTPS`, `TCP`, or `SSL`
        """
        ssl_certificate_id: NotRequired[pulumi.Input[str]]
        """
        The ARN of an SSL certificate you have
        uploaded to AWS IAM. **Note ECDSA-specific restrictions below.  Only valid when `lb_protocol` is either HTTPS or SSL**
        """
elif False:
    LoadBalancerListenerArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LoadBalancerListenerArgs:
    def __init__(__self__, *,
                 instance_port: pulumi.Input[int],
                 instance_protocol: pulumi.Input[str],
                 lb_port: pulumi.Input[int],
                 lb_protocol: pulumi.Input[str],
                 ssl_certificate_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[int] instance_port: The port on the instance to route to
        :param pulumi.Input[str] instance_protocol: The protocol to use to the instance. Valid
               values are `HTTP`, `HTTPS`, `TCP`, or `SSL`
        :param pulumi.Input[int] lb_port: The port to listen on for the load balancer
        :param pulumi.Input[str] lb_protocol: The protocol to listen on. Valid values are `HTTP`,
               `HTTPS`, `TCP`, or `SSL`
        :param pulumi.Input[str] ssl_certificate_id: The ARN of an SSL certificate you have
               uploaded to AWS IAM. **Note ECDSA-specific restrictions below.  Only valid when `lb_protocol` is either HTTPS or SSL**
        """
        pulumi.set(__self__, "instance_port", instance_port)
        pulumi.set(__self__, "instance_protocol", instance_protocol)
        pulumi.set(__self__, "lb_port", lb_port)
        pulumi.set(__self__, "lb_protocol", lb_protocol)
        if ssl_certificate_id is not None:
            pulumi.set(__self__, "ssl_certificate_id", ssl_certificate_id)

    @property
    @pulumi.getter(name="instancePort")
    def instance_port(self) -> pulumi.Input[int]:
        """
        The port on the instance to route to
        """
        return pulumi.get(self, "instance_port")

    @instance_port.setter
    def instance_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "instance_port", value)

    @property
    @pulumi.getter(name="instanceProtocol")
    def instance_protocol(self) -> pulumi.Input[str]:
        """
        The protocol to use to the instance. Valid
        values are `HTTP`, `HTTPS`, `TCP`, or `SSL`
        """
        return pulumi.get(self, "instance_protocol")

    @instance_protocol.setter
    def instance_protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_protocol", value)

    @property
    @pulumi.getter(name="lbPort")
    def lb_port(self) -> pulumi.Input[int]:
        """
        The port to listen on for the load balancer
        """
        return pulumi.get(self, "lb_port")

    @lb_port.setter
    def lb_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "lb_port", value)

    @property
    @pulumi.getter(name="lbProtocol")
    def lb_protocol(self) -> pulumi.Input[str]:
        """
        The protocol to listen on. Valid values are `HTTP`,
        `HTTPS`, `TCP`, or `SSL`
        """
        return pulumi.get(self, "lb_protocol")

    @lb_protocol.setter
    def lb_protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "lb_protocol", value)

    @property
    @pulumi.getter(name="sslCertificateId")
    def ssl_certificate_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of an SSL certificate you have
        uploaded to AWS IAM. **Note ECDSA-specific restrictions below.  Only valid when `lb_protocol` is either HTTPS or SSL**
        """
        return pulumi.get(self, "ssl_certificate_id")

    @ssl_certificate_id.setter
    def ssl_certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ssl_certificate_id", value)


if not MYPY:
    class LoadBalancerPolicyPolicyAttributeArgsDict(TypedDict):
        name: NotRequired[pulumi.Input[str]]
        value: NotRequired[pulumi.Input[str]]
elif False:
    LoadBalancerPolicyPolicyAttributeArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class LoadBalancerPolicyPolicyAttributeArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


if not MYPY:
    class SslNegotiationPolicyAttributeArgsDict(TypedDict):
        name: pulumi.Input[str]
        """
        The name of the attribute
        """
        value: pulumi.Input[str]
        """
        The value of the attribute
        """
elif False:
    SslNegotiationPolicyAttributeArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class SslNegotiationPolicyAttributeArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The name of the attribute
        :param pulumi.Input[str] value: The value of the attribute
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the attribute
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the attribute
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


