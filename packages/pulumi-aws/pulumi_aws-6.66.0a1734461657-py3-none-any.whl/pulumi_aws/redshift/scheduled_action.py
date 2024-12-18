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

__all__ = ['ScheduledActionArgs', 'ScheduledAction']

@pulumi.input_type
class ScheduledActionArgs:
    def __init__(__self__, *,
                 iam_role: pulumi.Input[str],
                 schedule: pulumi.Input[str],
                 target_action: pulumi.Input['ScheduledActionTargetActionArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 enable: Optional[pulumi.Input[bool]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ScheduledAction resource.
        :param pulumi.Input[str] iam_role: The IAM role to assume to run the scheduled action.
        :param pulumi.Input[str] schedule: The schedule of action. The schedule is defined format of "at expression" or "cron expression", for example `at(2016-03-04T17:27:00)` or `cron(0 10 ? * MON *)`. See [Scheduled Action](https://docs.aws.amazon.com/redshift/latest/APIReference/API_ScheduledAction.html) for more information.
        :param pulumi.Input['ScheduledActionTargetActionArgs'] target_action: Target action. Documented below.
        :param pulumi.Input[str] description: The description of the scheduled action.
        :param pulumi.Input[bool] enable: Whether to enable the scheduled action. Default is `true` .
        :param pulumi.Input[str] end_time: The end time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        :param pulumi.Input[str] name: The scheduled action name.
        :param pulumi.Input[str] start_time: The start time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        """
        pulumi.set(__self__, "iam_role", iam_role)
        pulumi.set(__self__, "schedule", schedule)
        pulumi.set(__self__, "target_action", target_action)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enable is not None:
            pulumi.set(__self__, "enable", enable)
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="iamRole")
    def iam_role(self) -> pulumi.Input[str]:
        """
        The IAM role to assume to run the scheduled action.
        """
        return pulumi.get(self, "iam_role")

    @iam_role.setter
    def iam_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "iam_role", value)

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Input[str]:
        """
        The schedule of action. The schedule is defined format of "at expression" or "cron expression", for example `at(2016-03-04T17:27:00)` or `cron(0 10 ? * MON *)`. See [Scheduled Action](https://docs.aws.amazon.com/redshift/latest/APIReference/API_ScheduledAction.html) for more information.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: pulumi.Input[str]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="targetAction")
    def target_action(self) -> pulumi.Input['ScheduledActionTargetActionArgs']:
        """
        Target action. Documented below.
        """
        return pulumi.get(self, "target_action")

    @target_action.setter
    def target_action(self, value: pulumi.Input['ScheduledActionTargetActionArgs']):
        pulumi.set(self, "target_action", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the scheduled action.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enable(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable the scheduled action. Default is `true` .
        """
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable", value)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        The end time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The scheduled action name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        The start time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_time", value)


@pulumi.input_type
class _ScheduledActionState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 enable: Optional[pulumi.Input[bool]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 iam_role: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 target_action: Optional[pulumi.Input['ScheduledActionTargetActionArgs']] = None):
        """
        Input properties used for looking up and filtering ScheduledAction resources.
        :param pulumi.Input[str] description: The description of the scheduled action.
        :param pulumi.Input[bool] enable: Whether to enable the scheduled action. Default is `true` .
        :param pulumi.Input[str] end_time: The end time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        :param pulumi.Input[str] iam_role: The IAM role to assume to run the scheduled action.
        :param pulumi.Input[str] name: The scheduled action name.
        :param pulumi.Input[str] schedule: The schedule of action. The schedule is defined format of "at expression" or "cron expression", for example `at(2016-03-04T17:27:00)` or `cron(0 10 ? * MON *)`. See [Scheduled Action](https://docs.aws.amazon.com/redshift/latest/APIReference/API_ScheduledAction.html) for more information.
        :param pulumi.Input[str] start_time: The start time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        :param pulumi.Input['ScheduledActionTargetActionArgs'] target_action: Target action. Documented below.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enable is not None:
            pulumi.set(__self__, "enable", enable)
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if iam_role is not None:
            pulumi.set(__self__, "iam_role", iam_role)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)
        if target_action is not None:
            pulumi.set(__self__, "target_action", target_action)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the scheduled action.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enable(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable the scheduled action. Default is `true` .
        """
        return pulumi.get(self, "enable")

    @enable.setter
    def enable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable", value)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[pulumi.Input[str]]:
        """
        The end time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter(name="iamRole")
    def iam_role(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM role to assume to run the scheduled action.
        """
        return pulumi.get(self, "iam_role")

    @iam_role.setter
    def iam_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "iam_role", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The scheduled action name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input[str]]:
        """
        The schedule of action. The schedule is defined format of "at expression" or "cron expression", for example `at(2016-03-04T17:27:00)` or `cron(0 10 ? * MON *)`. See [Scheduled Action](https://docs.aws.amazon.com/redshift/latest/APIReference/API_ScheduledAction.html) for more information.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[pulumi.Input[str]]:
        """
        The start time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_time", value)

    @property
    @pulumi.getter(name="targetAction")
    def target_action(self) -> Optional[pulumi.Input['ScheduledActionTargetActionArgs']]:
        """
        Target action. Documented below.
        """
        return pulumi.get(self, "target_action")

    @target_action.setter
    def target_action(self, value: Optional[pulumi.Input['ScheduledActionTargetActionArgs']]):
        pulumi.set(self, "target_action", value)


class ScheduledAction(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable: Optional[pulumi.Input[bool]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 iam_role: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 target_action: Optional[pulumi.Input[Union['ScheduledActionTargetActionArgs', 'ScheduledActionTargetActionArgsDict']]] = None,
                 __props__=None):
        """
        ## Example Usage

        ### Pause Cluster Action

        ```python
        import pulumi
        import pulumi_aws as aws

        assume_role = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "principals": [{
                "type": "Service",
                "identifiers": ["scheduler.redshift.amazonaws.com"],
            }],
            "actions": ["sts:AssumeRole"],
        }])
        example_role = aws.iam.Role("example",
            name="redshift_scheduled_action",
            assume_role_policy=assume_role.json)
        example = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "actions": [
                "redshift:PauseCluster",
                "redshift:ResumeCluster",
                "redshift:ResizeCluster",
            ],
            "resources": ["*"],
        }])
        example_policy = aws.iam.Policy("example",
            name="redshift_scheduled_action",
            policy=example.json)
        example_role_policy_attachment = aws.iam.RolePolicyAttachment("example",
            policy_arn=example_policy.arn,
            role=example_role.name)
        example_scheduled_action = aws.redshift.ScheduledAction("example",
            name="tf-redshift-scheduled-action",
            schedule="cron(00 23 * * ? *)",
            iam_role=example_role.arn,
            target_action={
                "pause_cluster": {
                    "cluster_identifier": "tf-redshift001",
                },
            })
        ```

        ### Resize Cluster Action

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.redshift.ScheduledAction("example",
            name="tf-redshift-scheduled-action",
            schedule="cron(00 23 * * ? *)",
            iam_role=example_aws_iam_role["arn"],
            target_action={
                "resize_cluster": {
                    "cluster_identifier": "tf-redshift001",
                    "cluster_type": "multi-node",
                    "node_type": "dc1.large",
                    "number_of_nodes": 2,
                },
            })
        ```

        ## Import

        Using `pulumi import`, import Redshift Scheduled Action using the `name`. For example:

        ```sh
        $ pulumi import aws:redshift/scheduledAction:ScheduledAction example tf-redshift-scheduled-action
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the scheduled action.
        :param pulumi.Input[bool] enable: Whether to enable the scheduled action. Default is `true` .
        :param pulumi.Input[str] end_time: The end time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        :param pulumi.Input[str] iam_role: The IAM role to assume to run the scheduled action.
        :param pulumi.Input[str] name: The scheduled action name.
        :param pulumi.Input[str] schedule: The schedule of action. The schedule is defined format of "at expression" or "cron expression", for example `at(2016-03-04T17:27:00)` or `cron(0 10 ? * MON *)`. See [Scheduled Action](https://docs.aws.amazon.com/redshift/latest/APIReference/API_ScheduledAction.html) for more information.
        :param pulumi.Input[str] start_time: The start time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        :param pulumi.Input[Union['ScheduledActionTargetActionArgs', 'ScheduledActionTargetActionArgsDict']] target_action: Target action. Documented below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ScheduledActionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ### Pause Cluster Action

        ```python
        import pulumi
        import pulumi_aws as aws

        assume_role = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "principals": [{
                "type": "Service",
                "identifiers": ["scheduler.redshift.amazonaws.com"],
            }],
            "actions": ["sts:AssumeRole"],
        }])
        example_role = aws.iam.Role("example",
            name="redshift_scheduled_action",
            assume_role_policy=assume_role.json)
        example = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "actions": [
                "redshift:PauseCluster",
                "redshift:ResumeCluster",
                "redshift:ResizeCluster",
            ],
            "resources": ["*"],
        }])
        example_policy = aws.iam.Policy("example",
            name="redshift_scheduled_action",
            policy=example.json)
        example_role_policy_attachment = aws.iam.RolePolicyAttachment("example",
            policy_arn=example_policy.arn,
            role=example_role.name)
        example_scheduled_action = aws.redshift.ScheduledAction("example",
            name="tf-redshift-scheduled-action",
            schedule="cron(00 23 * * ? *)",
            iam_role=example_role.arn,
            target_action={
                "pause_cluster": {
                    "cluster_identifier": "tf-redshift001",
                },
            })
        ```

        ### Resize Cluster Action

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.redshift.ScheduledAction("example",
            name="tf-redshift-scheduled-action",
            schedule="cron(00 23 * * ? *)",
            iam_role=example_aws_iam_role["arn"],
            target_action={
                "resize_cluster": {
                    "cluster_identifier": "tf-redshift001",
                    "cluster_type": "multi-node",
                    "node_type": "dc1.large",
                    "number_of_nodes": 2,
                },
            })
        ```

        ## Import

        Using `pulumi import`, import Redshift Scheduled Action using the `name`. For example:

        ```sh
        $ pulumi import aws:redshift/scheduledAction:ScheduledAction example tf-redshift-scheduled-action
        ```

        :param str resource_name: The name of the resource.
        :param ScheduledActionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScheduledActionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable: Optional[pulumi.Input[bool]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 iam_role: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 target_action: Optional[pulumi.Input[Union['ScheduledActionTargetActionArgs', 'ScheduledActionTargetActionArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ScheduledActionArgs.__new__(ScheduledActionArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["enable"] = enable
            __props__.__dict__["end_time"] = end_time
            if iam_role is None and not opts.urn:
                raise TypeError("Missing required property 'iam_role'")
            __props__.__dict__["iam_role"] = iam_role
            __props__.__dict__["name"] = name
            if schedule is None and not opts.urn:
                raise TypeError("Missing required property 'schedule'")
            __props__.__dict__["schedule"] = schedule
            __props__.__dict__["start_time"] = start_time
            if target_action is None and not opts.urn:
                raise TypeError("Missing required property 'target_action'")
            __props__.__dict__["target_action"] = target_action
        super(ScheduledAction, __self__).__init__(
            'aws:redshift/scheduledAction:ScheduledAction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            enable: Optional[pulumi.Input[bool]] = None,
            end_time: Optional[pulumi.Input[str]] = None,
            iam_role: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            schedule: Optional[pulumi.Input[str]] = None,
            start_time: Optional[pulumi.Input[str]] = None,
            target_action: Optional[pulumi.Input[Union['ScheduledActionTargetActionArgs', 'ScheduledActionTargetActionArgsDict']]] = None) -> 'ScheduledAction':
        """
        Get an existing ScheduledAction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the scheduled action.
        :param pulumi.Input[bool] enable: Whether to enable the scheduled action. Default is `true` .
        :param pulumi.Input[str] end_time: The end time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        :param pulumi.Input[str] iam_role: The IAM role to assume to run the scheduled action.
        :param pulumi.Input[str] name: The scheduled action name.
        :param pulumi.Input[str] schedule: The schedule of action. The schedule is defined format of "at expression" or "cron expression", for example `at(2016-03-04T17:27:00)` or `cron(0 10 ? * MON *)`. See [Scheduled Action](https://docs.aws.amazon.com/redshift/latest/APIReference/API_ScheduledAction.html) for more information.
        :param pulumi.Input[str] start_time: The start time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        :param pulumi.Input[Union['ScheduledActionTargetActionArgs', 'ScheduledActionTargetActionArgsDict']] target_action: Target action. Documented below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ScheduledActionState.__new__(_ScheduledActionState)

        __props__.__dict__["description"] = description
        __props__.__dict__["enable"] = enable
        __props__.__dict__["end_time"] = end_time
        __props__.__dict__["iam_role"] = iam_role
        __props__.__dict__["name"] = name
        __props__.__dict__["schedule"] = schedule
        __props__.__dict__["start_time"] = start_time
        __props__.__dict__["target_action"] = target_action
        return ScheduledAction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the scheduled action.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enable(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to enable the scheduled action. Default is `true` .
        """
        return pulumi.get(self, "enable")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[Optional[str]]:
        """
        The end time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="iamRole")
    def iam_role(self) -> pulumi.Output[str]:
        """
        The IAM role to assume to run the scheduled action.
        """
        return pulumi.get(self, "iam_role")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The scheduled action name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output[str]:
        """
        The schedule of action. The schedule is defined format of "at expression" or "cron expression", for example `at(2016-03-04T17:27:00)` or `cron(0 10 ? * MON *)`. See [Scheduled Action](https://docs.aws.amazon.com/redshift/latest/APIReference/API_ScheduledAction.html) for more information.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        The start time in UTC when the schedule is active, in UTC RFC3339 format(for example, YYYY-MM-DDTHH:MM:SSZ).
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="targetAction")
    def target_action(self) -> pulumi.Output['outputs.ScheduledActionTargetAction']:
        """
        Target action. Documented below.
        """
        return pulumi.get(self, "target_action")

