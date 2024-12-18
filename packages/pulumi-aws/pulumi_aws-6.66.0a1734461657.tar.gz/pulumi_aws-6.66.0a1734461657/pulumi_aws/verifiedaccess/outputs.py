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

__all__ = [
    'EndpointLoadBalancerOptions',
    'EndpointNetworkInterfaceOptions',
    'EndpointSseSpecification',
    'GroupSseConfiguration',
    'InstanceLoggingConfigurationAccessLogs',
    'InstanceLoggingConfigurationAccessLogsCloudwatchLogs',
    'InstanceLoggingConfigurationAccessLogsKinesisDataFirehose',
    'InstanceLoggingConfigurationAccessLogsS3',
    'InstanceVerifiedAccessTrustProvider',
    'TrustProviderDeviceOptions',
    'TrustProviderOidcOptions',
]

@pulumi.output_type
class EndpointLoadBalancerOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "loadBalancerArn":
            suggest = "load_balancer_arn"
        elif key == "subnetIds":
            suggest = "subnet_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointLoadBalancerOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointLoadBalancerOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointLoadBalancerOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 load_balancer_arn: Optional[str] = None,
                 port: Optional[int] = None,
                 protocol: Optional[str] = None,
                 subnet_ids: Optional[Sequence[str]] = None):
        if load_balancer_arn is not None:
            pulumi.set(__self__, "load_balancer_arn", load_balancer_arn)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="loadBalancerArn")
    def load_balancer_arn(self) -> Optional[str]:
        return pulumi.get(self, "load_balancer_arn")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> Optional[str]:
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "subnet_ids")


@pulumi.output_type
class EndpointNetworkInterfaceOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "networkInterfaceId":
            suggest = "network_interface_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointNetworkInterfaceOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointNetworkInterfaceOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointNetworkInterfaceOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 network_interface_id: Optional[str] = None,
                 port: Optional[int] = None,
                 protocol: Optional[str] = None):
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[str]:
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> Optional[str]:
        return pulumi.get(self, "protocol")


@pulumi.output_type
class EndpointSseSpecification(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "customerManagedKeyEnabled":
            suggest = "customer_managed_key_enabled"
        elif key == "kmsKeyArn":
            suggest = "kms_key_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointSseSpecification. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointSseSpecification.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointSseSpecification.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 customer_managed_key_enabled: Optional[bool] = None,
                 kms_key_arn: Optional[str] = None):
        if customer_managed_key_enabled is not None:
            pulumi.set(__self__, "customer_managed_key_enabled", customer_managed_key_enabled)
        if kms_key_arn is not None:
            pulumi.set(__self__, "kms_key_arn", kms_key_arn)

    @property
    @pulumi.getter(name="customerManagedKeyEnabled")
    def customer_managed_key_enabled(self) -> Optional[bool]:
        return pulumi.get(self, "customer_managed_key_enabled")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[str]:
        return pulumi.get(self, "kms_key_arn")


@pulumi.output_type
class GroupSseConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "customerManagedKeyEnabled":
            suggest = "customer_managed_key_enabled"
        elif key == "kmsKeyArn":
            suggest = "kms_key_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GroupSseConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GroupSseConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GroupSseConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 customer_managed_key_enabled: Optional[bool] = None,
                 kms_key_arn: Optional[str] = None):
        """
        :param str kms_key_arn: ARN of the KMS key to use.
        """
        if customer_managed_key_enabled is not None:
            pulumi.set(__self__, "customer_managed_key_enabled", customer_managed_key_enabled)
        if kms_key_arn is not None:
            pulumi.set(__self__, "kms_key_arn", kms_key_arn)

    @property
    @pulumi.getter(name="customerManagedKeyEnabled")
    def customer_managed_key_enabled(self) -> Optional[bool]:
        return pulumi.get(self, "customer_managed_key_enabled")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[str]:
        """
        ARN of the KMS key to use.
        """
        return pulumi.get(self, "kms_key_arn")


@pulumi.output_type
class InstanceLoggingConfigurationAccessLogs(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudwatchLogs":
            suggest = "cloudwatch_logs"
        elif key == "includeTrustContext":
            suggest = "include_trust_context"
        elif key == "kinesisDataFirehose":
            suggest = "kinesis_data_firehose"
        elif key == "logVersion":
            suggest = "log_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceLoggingConfigurationAccessLogs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceLoggingConfigurationAccessLogs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceLoggingConfigurationAccessLogs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloudwatch_logs: Optional['outputs.InstanceLoggingConfigurationAccessLogsCloudwatchLogs'] = None,
                 include_trust_context: Optional[bool] = None,
                 kinesis_data_firehose: Optional['outputs.InstanceLoggingConfigurationAccessLogsKinesisDataFirehose'] = None,
                 log_version: Optional[str] = None,
                 s3: Optional['outputs.InstanceLoggingConfigurationAccessLogsS3'] = None):
        """
        :param 'InstanceLoggingConfigurationAccessLogsCloudwatchLogsArgs' cloudwatch_logs: A block that specifies configures sending Verified Access logs to CloudWatch Logs. Detailed below.
        :param bool include_trust_context: Include trust data sent by trust providers into the logs.
        :param 'InstanceLoggingConfigurationAccessLogsKinesisDataFirehoseArgs' kinesis_data_firehose: A block that specifies configures sending Verified Access logs to Kinesis. Detailed below.
        :param str log_version: The logging version to use. Refer to [VerifiedAccessLogOptions](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_VerifiedAccessLogOptions.html) for the allowed values.
        :param 'InstanceLoggingConfigurationAccessLogsS3Args' s3: A block that specifies configures sending Verified Access logs to S3. Detailed below.
        """
        if cloudwatch_logs is not None:
            pulumi.set(__self__, "cloudwatch_logs", cloudwatch_logs)
        if include_trust_context is not None:
            pulumi.set(__self__, "include_trust_context", include_trust_context)
        if kinesis_data_firehose is not None:
            pulumi.set(__self__, "kinesis_data_firehose", kinesis_data_firehose)
        if log_version is not None:
            pulumi.set(__self__, "log_version", log_version)
        if s3 is not None:
            pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter(name="cloudwatchLogs")
    def cloudwatch_logs(self) -> Optional['outputs.InstanceLoggingConfigurationAccessLogsCloudwatchLogs']:
        """
        A block that specifies configures sending Verified Access logs to CloudWatch Logs. Detailed below.
        """
        return pulumi.get(self, "cloudwatch_logs")

    @property
    @pulumi.getter(name="includeTrustContext")
    def include_trust_context(self) -> Optional[bool]:
        """
        Include trust data sent by trust providers into the logs.
        """
        return pulumi.get(self, "include_trust_context")

    @property
    @pulumi.getter(name="kinesisDataFirehose")
    def kinesis_data_firehose(self) -> Optional['outputs.InstanceLoggingConfigurationAccessLogsKinesisDataFirehose']:
        """
        A block that specifies configures sending Verified Access logs to Kinesis. Detailed below.
        """
        return pulumi.get(self, "kinesis_data_firehose")

    @property
    @pulumi.getter(name="logVersion")
    def log_version(self) -> Optional[str]:
        """
        The logging version to use. Refer to [VerifiedAccessLogOptions](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_VerifiedAccessLogOptions.html) for the allowed values.
        """
        return pulumi.get(self, "log_version")

    @property
    @pulumi.getter
    def s3(self) -> Optional['outputs.InstanceLoggingConfigurationAccessLogsS3']:
        """
        A block that specifies configures sending Verified Access logs to S3. Detailed below.
        """
        return pulumi.get(self, "s3")


@pulumi.output_type
class InstanceLoggingConfigurationAccessLogsCloudwatchLogs(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroup":
            suggest = "log_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceLoggingConfigurationAccessLogsCloudwatchLogs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceLoggingConfigurationAccessLogsCloudwatchLogs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceLoggingConfigurationAccessLogsCloudwatchLogs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: bool,
                 log_group: Optional[str] = None):
        """
        :param bool enabled: Indicates whether logging is enabled.
        :param str log_group: The name of the CloudWatch Logs Log Group.
        """
        pulumi.set(__self__, "enabled", enabled)
        if log_group is not None:
            pulumi.set(__self__, "log_group", log_group)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Indicates whether logging is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="logGroup")
    def log_group(self) -> Optional[str]:
        """
        The name of the CloudWatch Logs Log Group.
        """
        return pulumi.get(self, "log_group")


@pulumi.output_type
class InstanceLoggingConfigurationAccessLogsKinesisDataFirehose(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deliveryStream":
            suggest = "delivery_stream"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceLoggingConfigurationAccessLogsKinesisDataFirehose. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceLoggingConfigurationAccessLogsKinesisDataFirehose.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceLoggingConfigurationAccessLogsKinesisDataFirehose.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: bool,
                 delivery_stream: Optional[str] = None):
        """
        :param bool enabled: Indicates whether logging is enabled.
        :param str delivery_stream: The name of the delivery stream.
        """
        pulumi.set(__self__, "enabled", enabled)
        if delivery_stream is not None:
            pulumi.set(__self__, "delivery_stream", delivery_stream)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Indicates whether logging is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="deliveryStream")
    def delivery_stream(self) -> Optional[str]:
        """
        The name of the delivery stream.
        """
        return pulumi.get(self, "delivery_stream")


@pulumi.output_type
class InstanceLoggingConfigurationAccessLogsS3(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"
        elif key == "bucketOwner":
            suggest = "bucket_owner"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceLoggingConfigurationAccessLogsS3. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceLoggingConfigurationAccessLogsS3.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceLoggingConfigurationAccessLogsS3.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: bool,
                 bucket_name: Optional[str] = None,
                 bucket_owner: Optional[str] = None,
                 prefix: Optional[str] = None):
        """
        :param bool enabled: Indicates whether logging is enabled.
        :param str bucket_name: The name of S3 bucket.
        :param str bucket_owner: The ID of the AWS account that owns the Amazon S3 bucket.
        :param str prefix: The bucket prefix.
        """
        pulumi.set(__self__, "enabled", enabled)
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if bucket_owner is not None:
            pulumi.set(__self__, "bucket_owner", bucket_owner)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Indicates whether logging is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[str]:
        """
        The name of S3 bucket.
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="bucketOwner")
    def bucket_owner(self) -> Optional[str]:
        """
        The ID of the AWS account that owns the Amazon S3 bucket.
        """
        return pulumi.get(self, "bucket_owner")

    @property
    @pulumi.getter
    def prefix(self) -> Optional[str]:
        """
        The bucket prefix.
        """
        return pulumi.get(self, "prefix")


@pulumi.output_type
class InstanceVerifiedAccessTrustProvider(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deviceTrustProviderType":
            suggest = "device_trust_provider_type"
        elif key == "trustProviderType":
            suggest = "trust_provider_type"
        elif key == "userTrustProviderType":
            suggest = "user_trust_provider_type"
        elif key == "verifiedAccessTrustProviderId":
            suggest = "verified_access_trust_provider_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceVerifiedAccessTrustProvider. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceVerifiedAccessTrustProvider.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceVerifiedAccessTrustProvider.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 description: Optional[str] = None,
                 device_trust_provider_type: Optional[str] = None,
                 trust_provider_type: Optional[str] = None,
                 user_trust_provider_type: Optional[str] = None,
                 verified_access_trust_provider_id: Optional[str] = None):
        """
        :param str description: A description for the AWS Verified Access Instance.
        :param str device_trust_provider_type: The type of device-based trust provider.
        :param str trust_provider_type: The type of trust provider (user- or device-based).
        :param str user_trust_provider_type: The type of user-based trust provider.
        :param str verified_access_trust_provider_id: The ID of the trust provider.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if device_trust_provider_type is not None:
            pulumi.set(__self__, "device_trust_provider_type", device_trust_provider_type)
        if trust_provider_type is not None:
            pulumi.set(__self__, "trust_provider_type", trust_provider_type)
        if user_trust_provider_type is not None:
            pulumi.set(__self__, "user_trust_provider_type", user_trust_provider_type)
        if verified_access_trust_provider_id is not None:
            pulumi.set(__self__, "verified_access_trust_provider_id", verified_access_trust_provider_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description for the AWS Verified Access Instance.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="deviceTrustProviderType")
    def device_trust_provider_type(self) -> Optional[str]:
        """
        The type of device-based trust provider.
        """
        return pulumi.get(self, "device_trust_provider_type")

    @property
    @pulumi.getter(name="trustProviderType")
    def trust_provider_type(self) -> Optional[str]:
        """
        The type of trust provider (user- or device-based).
        """
        return pulumi.get(self, "trust_provider_type")

    @property
    @pulumi.getter(name="userTrustProviderType")
    def user_trust_provider_type(self) -> Optional[str]:
        """
        The type of user-based trust provider.
        """
        return pulumi.get(self, "user_trust_provider_type")

    @property
    @pulumi.getter(name="verifiedAccessTrustProviderId")
    def verified_access_trust_provider_id(self) -> Optional[str]:
        """
        The ID of the trust provider.
        """
        return pulumi.get(self, "verified_access_trust_provider_id")


@pulumi.output_type
class TrustProviderDeviceOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrustProviderDeviceOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrustProviderDeviceOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrustProviderDeviceOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 tenant_id: Optional[str] = None):
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class TrustProviderOidcOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientSecret":
            suggest = "client_secret"
        elif key == "authorizationEndpoint":
            suggest = "authorization_endpoint"
        elif key == "clientId":
            suggest = "client_id"
        elif key == "tokenEndpoint":
            suggest = "token_endpoint"
        elif key == "userInfoEndpoint":
            suggest = "user_info_endpoint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TrustProviderOidcOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TrustProviderOidcOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TrustProviderOidcOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_secret: str,
                 authorization_endpoint: Optional[str] = None,
                 client_id: Optional[str] = None,
                 issuer: Optional[str] = None,
                 scope: Optional[str] = None,
                 token_endpoint: Optional[str] = None,
                 user_info_endpoint: Optional[str] = None):
        pulumi.set(__self__, "client_secret", client_secret)
        if authorization_endpoint is not None:
            pulumi.set(__self__, "authorization_endpoint", authorization_endpoint)
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if issuer is not None:
            pulumi.set(__self__, "issuer", issuer)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)
        if token_endpoint is not None:
            pulumi.set(__self__, "token_endpoint", token_endpoint)
        if user_info_endpoint is not None:
            pulumi.set(__self__, "user_info_endpoint", user_info_endpoint)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> str:
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="authorizationEndpoint")
    def authorization_endpoint(self) -> Optional[str]:
        return pulumi.get(self, "authorization_endpoint")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[str]:
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter
    def issuer(self) -> Optional[str]:
        return pulumi.get(self, "issuer")

    @property
    @pulumi.getter
    def scope(self) -> Optional[str]:
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter(name="tokenEndpoint")
    def token_endpoint(self) -> Optional[str]:
        return pulumi.get(self, "token_endpoint")

    @property
    @pulumi.getter(name="userInfoEndpoint")
    def user_info_endpoint(self) -> Optional[str]:
        return pulumi.get(self, "user_info_endpoint")


