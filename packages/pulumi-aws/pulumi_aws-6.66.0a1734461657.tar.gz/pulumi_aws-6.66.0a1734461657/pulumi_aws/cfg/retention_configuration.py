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

__all__ = ['RetentionConfigurationArgs', 'RetentionConfiguration']

@pulumi.input_type
class RetentionConfigurationArgs:
    def __init__(__self__, *,
                 retention_period_in_days: pulumi.Input[int]):
        """
        The set of arguments for constructing a RetentionConfiguration resource.
        :param pulumi.Input[int] retention_period_in_days: The number of days AWS Config stores historical information.
        """
        pulumi.set(__self__, "retention_period_in_days", retention_period_in_days)

    @property
    @pulumi.getter(name="retentionPeriodInDays")
    def retention_period_in_days(self) -> pulumi.Input[int]:
        """
        The number of days AWS Config stores historical information.
        """
        return pulumi.get(self, "retention_period_in_days")

    @retention_period_in_days.setter
    def retention_period_in_days(self, value: pulumi.Input[int]):
        pulumi.set(self, "retention_period_in_days", value)


@pulumi.input_type
class _RetentionConfigurationState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 retention_period_in_days: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering RetentionConfiguration resources.
        :param pulumi.Input[str] name: The name of the retention configuration object. The object is always named **default**.
        :param pulumi.Input[int] retention_period_in_days: The number of days AWS Config stores historical information.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if retention_period_in_days is not None:
            pulumi.set(__self__, "retention_period_in_days", retention_period_in_days)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the retention configuration object. The object is always named **default**.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="retentionPeriodInDays")
    def retention_period_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        The number of days AWS Config stores historical information.
        """
        return pulumi.get(self, "retention_period_in_days")

    @retention_period_in_days.setter
    def retention_period_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_period_in_days", value)


class RetentionConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 retention_period_in_days: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a resource to manage the AWS Config retention configuration.
        The retention configuration defines the number of days that AWS Config stores historical information.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cfg.RetentionConfiguration("example", retention_period_in_days=90)
        ```

        ## Import

        Using `pulumi import`, import the AWS Config retention configuration using the `name`. For example:

        ```sh
        $ pulumi import aws:cfg/retentionConfiguration:RetentionConfiguration example default
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] retention_period_in_days: The number of days AWS Config stores historical information.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RetentionConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage the AWS Config retention configuration.
        The retention configuration defines the number of days that AWS Config stores historical information.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cfg.RetentionConfiguration("example", retention_period_in_days=90)
        ```

        ## Import

        Using `pulumi import`, import the AWS Config retention configuration using the `name`. For example:

        ```sh
        $ pulumi import aws:cfg/retentionConfiguration:RetentionConfiguration example default
        ```

        :param str resource_name: The name of the resource.
        :param RetentionConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RetentionConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 retention_period_in_days: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RetentionConfigurationArgs.__new__(RetentionConfigurationArgs)

            if retention_period_in_days is None and not opts.urn:
                raise TypeError("Missing required property 'retention_period_in_days'")
            __props__.__dict__["retention_period_in_days"] = retention_period_in_days
            __props__.__dict__["name"] = None
        super(RetentionConfiguration, __self__).__init__(
            'aws:cfg/retentionConfiguration:RetentionConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            retention_period_in_days: Optional[pulumi.Input[int]] = None) -> 'RetentionConfiguration':
        """
        Get an existing RetentionConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the retention configuration object. The object is always named **default**.
        :param pulumi.Input[int] retention_period_in_days: The number of days AWS Config stores historical information.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RetentionConfigurationState.__new__(_RetentionConfigurationState)

        __props__.__dict__["name"] = name
        __props__.__dict__["retention_period_in_days"] = retention_period_in_days
        return RetentionConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the retention configuration object. The object is always named **default**.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="retentionPeriodInDays")
    def retention_period_in_days(self) -> pulumi.Output[int]:
        """
        The number of days AWS Config stores historical information.
        """
        return pulumi.get(self, "retention_period_in_days")

