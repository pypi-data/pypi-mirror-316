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

__all__ = ['OrganizationConfigurationFeatureArgs', 'OrganizationConfigurationFeature']

@pulumi.input_type
class OrganizationConfigurationFeatureArgs:
    def __init__(__self__, *,
                 auto_enable: pulumi.Input[str],
                 detector_id: pulumi.Input[str],
                 additional_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationConfigurationFeatureAdditionalConfigurationArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OrganizationConfigurationFeature resource.
        :param pulumi.Input[str] auto_enable: The status of the feature that is configured for the member accounts within the organization. Valid values: `NEW`, `ALL`, `NONE`.
        :param pulumi.Input[str] detector_id: The ID of the detector that configures the delegated administrator.
        :param pulumi.Input[Sequence[pulumi.Input['OrganizationConfigurationFeatureAdditionalConfigurationArgs']]] additional_configurations: Additional feature configuration block for features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING`. See below.
        :param pulumi.Input[str] name: The name of the feature that will be configured for the organization. Valid values: `S3_DATA_EVENTS`, `EKS_AUDIT_LOGS`, `EBS_MALWARE_PROTECTION`, `RDS_LOGIN_EVENTS`, `EKS_RUNTIME_MONITORING`, `LAMBDA_NETWORK_LOGS`, `RUNTIME_MONITORING`. Only one of two features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING` can be added, adding both features will cause an error. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html) for the current list of supported values.
        """
        pulumi.set(__self__, "auto_enable", auto_enable)
        pulumi.set(__self__, "detector_id", detector_id)
        if additional_configurations is not None:
            pulumi.set(__self__, "additional_configurations", additional_configurations)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> pulumi.Input[str]:
        """
        The status of the feature that is configured for the member accounts within the organization. Valid values: `NEW`, `ALL`, `NONE`.
        """
        return pulumi.get(self, "auto_enable")

    @auto_enable.setter
    def auto_enable(self, value: pulumi.Input[str]):
        pulumi.set(self, "auto_enable", value)

    @property
    @pulumi.getter(name="detectorId")
    def detector_id(self) -> pulumi.Input[str]:
        """
        The ID of the detector that configures the delegated administrator.
        """
        return pulumi.get(self, "detector_id")

    @detector_id.setter
    def detector_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "detector_id", value)

    @property
    @pulumi.getter(name="additionalConfigurations")
    def additional_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationConfigurationFeatureAdditionalConfigurationArgs']]]]:
        """
        Additional feature configuration block for features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING`. See below.
        """
        return pulumi.get(self, "additional_configurations")

    @additional_configurations.setter
    def additional_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationConfigurationFeatureAdditionalConfigurationArgs']]]]):
        pulumi.set(self, "additional_configurations", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the feature that will be configured for the organization. Valid values: `S3_DATA_EVENTS`, `EKS_AUDIT_LOGS`, `EBS_MALWARE_PROTECTION`, `RDS_LOGIN_EVENTS`, `EKS_RUNTIME_MONITORING`, `LAMBDA_NETWORK_LOGS`, `RUNTIME_MONITORING`. Only one of two features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING` can be added, adding both features will cause an error. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html) for the current list of supported values.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _OrganizationConfigurationFeatureState:
    def __init__(__self__, *,
                 additional_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationConfigurationFeatureAdditionalConfigurationArgs']]]] = None,
                 auto_enable: Optional[pulumi.Input[str]] = None,
                 detector_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OrganizationConfigurationFeature resources.
        :param pulumi.Input[Sequence[pulumi.Input['OrganizationConfigurationFeatureAdditionalConfigurationArgs']]] additional_configurations: Additional feature configuration block for features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING`. See below.
        :param pulumi.Input[str] auto_enable: The status of the feature that is configured for the member accounts within the organization. Valid values: `NEW`, `ALL`, `NONE`.
        :param pulumi.Input[str] detector_id: The ID of the detector that configures the delegated administrator.
        :param pulumi.Input[str] name: The name of the feature that will be configured for the organization. Valid values: `S3_DATA_EVENTS`, `EKS_AUDIT_LOGS`, `EBS_MALWARE_PROTECTION`, `RDS_LOGIN_EVENTS`, `EKS_RUNTIME_MONITORING`, `LAMBDA_NETWORK_LOGS`, `RUNTIME_MONITORING`. Only one of two features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING` can be added, adding both features will cause an error. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html) for the current list of supported values.
        """
        if additional_configurations is not None:
            pulumi.set(__self__, "additional_configurations", additional_configurations)
        if auto_enable is not None:
            pulumi.set(__self__, "auto_enable", auto_enable)
        if detector_id is not None:
            pulumi.set(__self__, "detector_id", detector_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="additionalConfigurations")
    def additional_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationConfigurationFeatureAdditionalConfigurationArgs']]]]:
        """
        Additional feature configuration block for features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING`. See below.
        """
        return pulumi.get(self, "additional_configurations")

    @additional_configurations.setter
    def additional_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationConfigurationFeatureAdditionalConfigurationArgs']]]]):
        pulumi.set(self, "additional_configurations", value)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the feature that is configured for the member accounts within the organization. Valid values: `NEW`, `ALL`, `NONE`.
        """
        return pulumi.get(self, "auto_enable")

    @auto_enable.setter
    def auto_enable(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auto_enable", value)

    @property
    @pulumi.getter(name="detectorId")
    def detector_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the detector that configures the delegated administrator.
        """
        return pulumi.get(self, "detector_id")

    @detector_id.setter
    def detector_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "detector_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the feature that will be configured for the organization. Valid values: `S3_DATA_EVENTS`, `EKS_AUDIT_LOGS`, `EBS_MALWARE_PROTECTION`, `RDS_LOGIN_EVENTS`, `EKS_RUNTIME_MONITORING`, `LAMBDA_NETWORK_LOGS`, `RUNTIME_MONITORING`. Only one of two features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING` can be added, adding both features will cause an error. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html) for the current list of supported values.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class OrganizationConfigurationFeature(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OrganizationConfigurationFeatureAdditionalConfigurationArgs', 'OrganizationConfigurationFeatureAdditionalConfigurationArgsDict']]]]] = None,
                 auto_enable: Optional[pulumi.Input[str]] = None,
                 detector_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage a single Amazon GuardDuty [organization configuration feature](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-features-activation-model.html#guardduty-features).

        > **NOTE:** Deleting this resource does not disable the organization configuration feature, the resource in simply removed from state instead.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.guardduty.Detector("example", enable=True)
        eks_runtime_monitoring = aws.guardduty.OrganizationConfigurationFeature("eks_runtime_monitoring",
            detector_id=example.id,
            name="EKS_RUNTIME_MONITORING",
            auto_enable="ALL",
            additional_configurations=[{
                "name": "EKS_ADDON_MANAGEMENT",
                "auto_enable": "NEW",
            }])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['OrganizationConfigurationFeatureAdditionalConfigurationArgs', 'OrganizationConfigurationFeatureAdditionalConfigurationArgsDict']]]] additional_configurations: Additional feature configuration block for features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING`. See below.
        :param pulumi.Input[str] auto_enable: The status of the feature that is configured for the member accounts within the organization. Valid values: `NEW`, `ALL`, `NONE`.
        :param pulumi.Input[str] detector_id: The ID of the detector that configures the delegated administrator.
        :param pulumi.Input[str] name: The name of the feature that will be configured for the organization. Valid values: `S3_DATA_EVENTS`, `EKS_AUDIT_LOGS`, `EBS_MALWARE_PROTECTION`, `RDS_LOGIN_EVENTS`, `EKS_RUNTIME_MONITORING`, `LAMBDA_NETWORK_LOGS`, `RUNTIME_MONITORING`. Only one of two features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING` can be added, adding both features will cause an error. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html) for the current list of supported values.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OrganizationConfigurationFeatureArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage a single Amazon GuardDuty [organization configuration feature](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-features-activation-model.html#guardduty-features).

        > **NOTE:** Deleting this resource does not disable the organization configuration feature, the resource in simply removed from state instead.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.guardduty.Detector("example", enable=True)
        eks_runtime_monitoring = aws.guardduty.OrganizationConfigurationFeature("eks_runtime_monitoring",
            detector_id=example.id,
            name="EKS_RUNTIME_MONITORING",
            auto_enable="ALL",
            additional_configurations=[{
                "name": "EKS_ADDON_MANAGEMENT",
                "auto_enable": "NEW",
            }])
        ```

        :param str resource_name: The name of the resource.
        :param OrganizationConfigurationFeatureArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OrganizationConfigurationFeatureArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OrganizationConfigurationFeatureAdditionalConfigurationArgs', 'OrganizationConfigurationFeatureAdditionalConfigurationArgsDict']]]]] = None,
                 auto_enable: Optional[pulumi.Input[str]] = None,
                 detector_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OrganizationConfigurationFeatureArgs.__new__(OrganizationConfigurationFeatureArgs)

            __props__.__dict__["additional_configurations"] = additional_configurations
            if auto_enable is None and not opts.urn:
                raise TypeError("Missing required property 'auto_enable'")
            __props__.__dict__["auto_enable"] = auto_enable
            if detector_id is None and not opts.urn:
                raise TypeError("Missing required property 'detector_id'")
            __props__.__dict__["detector_id"] = detector_id
            __props__.__dict__["name"] = name
        super(OrganizationConfigurationFeature, __self__).__init__(
            'aws:guardduty/organizationConfigurationFeature:OrganizationConfigurationFeature',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            additional_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OrganizationConfigurationFeatureAdditionalConfigurationArgs', 'OrganizationConfigurationFeatureAdditionalConfigurationArgsDict']]]]] = None,
            auto_enable: Optional[pulumi.Input[str]] = None,
            detector_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'OrganizationConfigurationFeature':
        """
        Get an existing OrganizationConfigurationFeature resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['OrganizationConfigurationFeatureAdditionalConfigurationArgs', 'OrganizationConfigurationFeatureAdditionalConfigurationArgsDict']]]] additional_configurations: Additional feature configuration block for features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING`. See below.
        :param pulumi.Input[str] auto_enable: The status of the feature that is configured for the member accounts within the organization. Valid values: `NEW`, `ALL`, `NONE`.
        :param pulumi.Input[str] detector_id: The ID of the detector that configures the delegated administrator.
        :param pulumi.Input[str] name: The name of the feature that will be configured for the organization. Valid values: `S3_DATA_EVENTS`, `EKS_AUDIT_LOGS`, `EBS_MALWARE_PROTECTION`, `RDS_LOGIN_EVENTS`, `EKS_RUNTIME_MONITORING`, `LAMBDA_NETWORK_LOGS`, `RUNTIME_MONITORING`. Only one of two features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING` can be added, adding both features will cause an error. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html) for the current list of supported values.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OrganizationConfigurationFeatureState.__new__(_OrganizationConfigurationFeatureState)

        __props__.__dict__["additional_configurations"] = additional_configurations
        __props__.__dict__["auto_enable"] = auto_enable
        __props__.__dict__["detector_id"] = detector_id
        __props__.__dict__["name"] = name
        return OrganizationConfigurationFeature(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="additionalConfigurations")
    def additional_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.OrganizationConfigurationFeatureAdditionalConfiguration']]]:
        """
        Additional feature configuration block for features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING`. See below.
        """
        return pulumi.get(self, "additional_configurations")

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> pulumi.Output[str]:
        """
        The status of the feature that is configured for the member accounts within the organization. Valid values: `NEW`, `ALL`, `NONE`.
        """
        return pulumi.get(self, "auto_enable")

    @property
    @pulumi.getter(name="detectorId")
    def detector_id(self) -> pulumi.Output[str]:
        """
        The ID of the detector that configures the delegated administrator.
        """
        return pulumi.get(self, "detector_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the feature that will be configured for the organization. Valid values: `S3_DATA_EVENTS`, `EKS_AUDIT_LOGS`, `EBS_MALWARE_PROTECTION`, `RDS_LOGIN_EVENTS`, `EKS_RUNTIME_MONITORING`, `LAMBDA_NETWORK_LOGS`, `RUNTIME_MONITORING`. Only one of two features `EKS_RUNTIME_MONITORING` or `RUNTIME_MONITORING` can be added, adding both features will cause an error. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorFeatureConfiguration.html) for the current list of supported values.
        """
        return pulumi.get(self, "name")

