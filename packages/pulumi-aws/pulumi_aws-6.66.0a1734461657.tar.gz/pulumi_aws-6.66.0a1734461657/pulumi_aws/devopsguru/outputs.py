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
    'EventSourcesConfigEventSource',
    'EventSourcesConfigEventSourceAmazonCodeGuruProfiler',
    'NotificationChannelFilters',
    'NotificationChannelSns',
    'ResourceCollectionCloudformation',
    'ResourceCollectionTags',
    'ServiceIntegrationKmsServerSideEncryption',
    'ServiceIntegrationLogsAnomalyDetection',
    'ServiceIntegrationOpsCenter',
    'GetNotificationChannelFilterResult',
    'GetNotificationChannelSnResult',
    'GetResourceCollectionCloudformationResult',
    'GetResourceCollectionTagResult',
]

@pulumi.output_type
class EventSourcesConfigEventSource(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "amazonCodeGuruProfilers":
            suggest = "amazon_code_guru_profilers"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventSourcesConfigEventSource. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventSourcesConfigEventSource.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventSourcesConfigEventSource.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 amazon_code_guru_profilers: Optional[Sequence['outputs.EventSourcesConfigEventSourceAmazonCodeGuruProfiler']] = None):
        """
        :param Sequence['EventSourcesConfigEventSourceAmazonCodeGuruProfilerArgs'] amazon_code_guru_profilers: Stores whether DevOps Guru is configured to consume recommendations which are generated from AWS CodeGuru Profiler. See `amazon_code_guru_profiler` below.
        """
        if amazon_code_guru_profilers is not None:
            pulumi.set(__self__, "amazon_code_guru_profilers", amazon_code_guru_profilers)

    @property
    @pulumi.getter(name="amazonCodeGuruProfilers")
    def amazon_code_guru_profilers(self) -> Optional[Sequence['outputs.EventSourcesConfigEventSourceAmazonCodeGuruProfiler']]:
        """
        Stores whether DevOps Guru is configured to consume recommendations which are generated from AWS CodeGuru Profiler. See `amazon_code_guru_profiler` below.
        """
        return pulumi.get(self, "amazon_code_guru_profilers")


@pulumi.output_type
class EventSourcesConfigEventSourceAmazonCodeGuruProfiler(dict):
    def __init__(__self__, *,
                 status: str):
        """
        :param str status: Status of the CodeGuru Profiler integration. Valid values are `ENABLED` and `DISABLED`.
        """
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the CodeGuru Profiler integration. Valid values are `ENABLED` and `DISABLED`.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class NotificationChannelFilters(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "messageTypes":
            suggest = "message_types"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NotificationChannelFilters. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NotificationChannelFilters.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NotificationChannelFilters.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 message_types: Optional[Sequence[str]] = None,
                 severities: Optional[Sequence[str]] = None):
        """
        :param Sequence[str] message_types: Events to receive notifications for. Valid values are `NEW_INSIGHT`, `CLOSED_INSIGHT`, `NEW_ASSOCIATION`, `SEVERITY_UPGRADED`, and `NEW_RECOMMENDATION`.
        :param Sequence[str] severities: Severity levels to receive notifications for. Valid values are `LOW`, `MEDIUM`, and `HIGH`.
        """
        if message_types is not None:
            pulumi.set(__self__, "message_types", message_types)
        if severities is not None:
            pulumi.set(__self__, "severities", severities)

    @property
    @pulumi.getter(name="messageTypes")
    def message_types(self) -> Optional[Sequence[str]]:
        """
        Events to receive notifications for. Valid values are `NEW_INSIGHT`, `CLOSED_INSIGHT`, `NEW_ASSOCIATION`, `SEVERITY_UPGRADED`, and `NEW_RECOMMENDATION`.
        """
        return pulumi.get(self, "message_types")

    @property
    @pulumi.getter
    def severities(self) -> Optional[Sequence[str]]:
        """
        Severity levels to receive notifications for. Valid values are `LOW`, `MEDIUM`, and `HIGH`.
        """
        return pulumi.get(self, "severities")


@pulumi.output_type
class NotificationChannelSns(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "topicArn":
            suggest = "topic_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NotificationChannelSns. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NotificationChannelSns.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NotificationChannelSns.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 topic_arn: str):
        """
        :param str topic_arn: Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.
        """
        pulumi.set(__self__, "topic_arn", topic_arn)

    @property
    @pulumi.getter(name="topicArn")
    def topic_arn(self) -> str:
        """
        Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.
        """
        return pulumi.get(self, "topic_arn")


@pulumi.output_type
class ResourceCollectionCloudformation(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "stackNames":
            suggest = "stack_names"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResourceCollectionCloudformation. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResourceCollectionCloudformation.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResourceCollectionCloudformation.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 stack_names: Sequence[str]):
        """
        :param Sequence[str] stack_names: Array of the names of the AWS CloudFormation stacks. If `type` is `AWS_SERVICE` (all acccount resources) this array should be a single item containing a wildcard (`"*"`).
        """
        pulumi.set(__self__, "stack_names", stack_names)

    @property
    @pulumi.getter(name="stackNames")
    def stack_names(self) -> Sequence[str]:
        """
        Array of the names of the AWS CloudFormation stacks. If `type` is `AWS_SERVICE` (all acccount resources) this array should be a single item containing a wildcard (`"*"`).
        """
        return pulumi.get(self, "stack_names")


@pulumi.output_type
class ResourceCollectionTags(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "appBoundaryKey":
            suggest = "app_boundary_key"
        elif key == "tagValues":
            suggest = "tag_values"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResourceCollectionTags. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResourceCollectionTags.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResourceCollectionTags.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 app_boundary_key: str,
                 tag_values: Sequence[str]):
        """
        :param str app_boundary_key: An AWS tag key that is used to identify the AWS resources that DevOps Guru analyzes. All AWS resources in your account and Region tagged with this key make up your DevOps Guru application and analysis boundary. The key must begin with the prefix `DevOps-Guru-`. Any casing can be used for the prefix, but the associated tags __must use the same casing__ in their tag key.
        :param Sequence[str] tag_values: Array of tag values. These can be used to further filter for specific resources within the application boundary. To analyze all resources tagged with the `app_boundary_key` regardless of the corresponding tag value, this array should be a single item containing a wildcard (`"*"`).
        """
        pulumi.set(__self__, "app_boundary_key", app_boundary_key)
        pulumi.set(__self__, "tag_values", tag_values)

    @property
    @pulumi.getter(name="appBoundaryKey")
    def app_boundary_key(self) -> str:
        """
        An AWS tag key that is used to identify the AWS resources that DevOps Guru analyzes. All AWS resources in your account and Region tagged with this key make up your DevOps Guru application and analysis boundary. The key must begin with the prefix `DevOps-Guru-`. Any casing can be used for the prefix, but the associated tags __must use the same casing__ in their tag key.
        """
        return pulumi.get(self, "app_boundary_key")

    @property
    @pulumi.getter(name="tagValues")
    def tag_values(self) -> Sequence[str]:
        """
        Array of tag values. These can be used to further filter for specific resources within the application boundary. To analyze all resources tagged with the `app_boundary_key` regardless of the corresponding tag value, this array should be a single item containing a wildcard (`"*"`).
        """
        return pulumi.get(self, "tag_values")


@pulumi.output_type
class ServiceIntegrationKmsServerSideEncryption(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "kmsKeyId":
            suggest = "kms_key_id"
        elif key == "optInStatus":
            suggest = "opt_in_status"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServiceIntegrationKmsServerSideEncryption. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServiceIntegrationKmsServerSideEncryption.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServiceIntegrationKmsServerSideEncryption.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kms_key_id: Optional[str] = None,
                 opt_in_status: Optional[str] = None,
                 type: Optional[str] = None):
        """
        :param str kms_key_id: KMS key ID. This value can be a key ID, key ARN, alias name, or alias ARN.
        :param str opt_in_status: Specifies whether KMS integration is enabled. Valid values are `DISABLED` and `ENABLED`.
        :param str type: Type of KMS key used. Valid values are `CUSTOMER_MANAGED_KEY` and `AWS_OWNED_KMS_KEY`.
        """
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if opt_in_status is not None:
            pulumi.set(__self__, "opt_in_status", opt_in_status)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[str]:
        """
        KMS key ID. This value can be a key ID, key ARN, alias name, or alias ARN.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="optInStatus")
    def opt_in_status(self) -> Optional[str]:
        """
        Specifies whether KMS integration is enabled. Valid values are `DISABLED` and `ENABLED`.
        """
        return pulumi.get(self, "opt_in_status")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Type of KMS key used. Valid values are `CUSTOMER_MANAGED_KEY` and `AWS_OWNED_KMS_KEY`.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class ServiceIntegrationLogsAnomalyDetection(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "optInStatus":
            suggest = "opt_in_status"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServiceIntegrationLogsAnomalyDetection. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServiceIntegrationLogsAnomalyDetection.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServiceIntegrationLogsAnomalyDetection.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 opt_in_status: Optional[str] = None):
        """
        :param str opt_in_status: Specifies if DevOps Guru is configured to perform log anomaly detection on CloudWatch log groups. Valid values are `DISABLED` and `ENABLED`.
        """
        if opt_in_status is not None:
            pulumi.set(__self__, "opt_in_status", opt_in_status)

    @property
    @pulumi.getter(name="optInStatus")
    def opt_in_status(self) -> Optional[str]:
        """
        Specifies if DevOps Guru is configured to perform log anomaly detection on CloudWatch log groups. Valid values are `DISABLED` and `ENABLED`.
        """
        return pulumi.get(self, "opt_in_status")


@pulumi.output_type
class ServiceIntegrationOpsCenter(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "optInStatus":
            suggest = "opt_in_status"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ServiceIntegrationOpsCenter. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ServiceIntegrationOpsCenter.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ServiceIntegrationOpsCenter.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 opt_in_status: Optional[str] = None):
        """
        :param str opt_in_status: Specifies if DevOps Guru is enabled to create an AWS Systems Manager OpsItem for each created insight. Valid values are `DISABLED` and `ENABLED`.
        """
        if opt_in_status is not None:
            pulumi.set(__self__, "opt_in_status", opt_in_status)

    @property
    @pulumi.getter(name="optInStatus")
    def opt_in_status(self) -> Optional[str]:
        """
        Specifies if DevOps Guru is enabled to create an AWS Systems Manager OpsItem for each created insight. Valid values are `DISABLED` and `ENABLED`.
        """
        return pulumi.get(self, "opt_in_status")


@pulumi.output_type
class GetNotificationChannelFilterResult(dict):
    def __init__(__self__, *,
                 message_types: Sequence[str],
                 severities: Sequence[str]):
        """
        :param Sequence[str] message_types: Events to receive notifications for.
        :param Sequence[str] severities: Severity levels to receive notifications for.
        """
        pulumi.set(__self__, "message_types", message_types)
        pulumi.set(__self__, "severities", severities)

    @property
    @pulumi.getter(name="messageTypes")
    def message_types(self) -> Sequence[str]:
        """
        Events to receive notifications for.
        """
        return pulumi.get(self, "message_types")

    @property
    @pulumi.getter
    def severities(self) -> Sequence[str]:
        """
        Severity levels to receive notifications for.
        """
        return pulumi.get(self, "severities")


@pulumi.output_type
class GetNotificationChannelSnResult(dict):
    def __init__(__self__, *,
                 topic_arn: str):
        """
        :param str topic_arn: Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.
        """
        pulumi.set(__self__, "topic_arn", topic_arn)

    @property
    @pulumi.getter(name="topicArn")
    def topic_arn(self) -> str:
        """
        Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.
        """
        return pulumi.get(self, "topic_arn")


@pulumi.output_type
class GetResourceCollectionCloudformationResult(dict):
    def __init__(__self__, *,
                 stack_names: Sequence[str]):
        """
        :param Sequence[str] stack_names: Array of the names of the AWS CloudFormation stacks.
        """
        pulumi.set(__self__, "stack_names", stack_names)

    @property
    @pulumi.getter(name="stackNames")
    def stack_names(self) -> Sequence[str]:
        """
        Array of the names of the AWS CloudFormation stacks.
        """
        return pulumi.get(self, "stack_names")


@pulumi.output_type
class GetResourceCollectionTagResult(dict):
    def __init__(__self__, *,
                 app_boundary_key: str,
                 tag_values: Sequence[str]):
        """
        :param str app_boundary_key: An AWS tag key that is used to identify the AWS resources that DevOps Guru analyzes.
        :param Sequence[str] tag_values: Array of tag values.
        """
        pulumi.set(__self__, "app_boundary_key", app_boundary_key)
        pulumi.set(__self__, "tag_values", tag_values)

    @property
    @pulumi.getter(name="appBoundaryKey")
    def app_boundary_key(self) -> str:
        """
        An AWS tag key that is used to identify the AWS resources that DevOps Guru analyzes.
        """
        return pulumi.get(self, "app_boundary_key")

    @property
    @pulumi.getter(name="tagValues")
    def tag_values(self) -> Sequence[str]:
        """
        Array of tag values.
        """
        return pulumi.get(self, "tag_values")


