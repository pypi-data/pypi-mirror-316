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

__all__ = ['SelectionArgs', 'Selection']

@pulumi.input_type
class SelectionArgs:
    def __init__(__self__, *,
                 iam_role_arn: pulumi.Input[str],
                 plan_id: pulumi.Input[str],
                 conditions: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 selection_tags: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionSelectionTagArgs']]]] = None):
        """
        The set of arguments for constructing a Selection resource.
        :param pulumi.Input[str] iam_role_arn: The ARN of the IAM role that AWS Backup uses to authenticate when restoring and backing up the target resource. See the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/access-control.html#managed-policies) for additional information about using AWS managed policies or creating custom policies attached to the IAM role.
        :param pulumi.Input[str] plan_id: The backup plan ID to be associated with the selection of resources.
        :param pulumi.Input[Sequence[pulumi.Input['SelectionConditionArgs']]] conditions: A list of conditions that you define to assign resources to your backup plans using tags.
        :param pulumi.Input[str] name: The display name of a resource selection document.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_resources: An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to exclude from a backup plan.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to assign to a backup plan.
        :param pulumi.Input[Sequence[pulumi.Input['SelectionSelectionTagArgs']]] selection_tags: Tag-based conditions used to specify a set of resources to assign to a backup plan.
        """
        pulumi.set(__self__, "iam_role_arn", iam_role_arn)
        pulumi.set(__self__, "plan_id", plan_id)
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if not_resources is not None:
            pulumi.set(__self__, "not_resources", not_resources)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)
        if selection_tags is not None:
            pulumi.set(__self__, "selection_tags", selection_tags)

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the IAM role that AWS Backup uses to authenticate when restoring and backing up the target resource. See the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/access-control.html#managed-policies) for additional information about using AWS managed policies or creating custom policies attached to the IAM role.
        """
        return pulumi.get(self, "iam_role_arn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "iam_role_arn", value)

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> pulumi.Input[str]:
        """
        The backup plan ID to be associated with the selection of resources.
        """
        return pulumi.get(self, "plan_id")

    @plan_id.setter
    def plan_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "plan_id", value)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionArgs']]]]:
        """
        A list of conditions that you define to assign resources to your backup plans using tags.
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionArgs']]]]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name of a resource selection document.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notResources")
    def not_resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to exclude from a backup plan.
        """
        return pulumi.get(self, "not_resources")

    @not_resources.setter
    def not_resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_resources", value)

    @property
    @pulumi.getter
    def resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to assign to a backup plan.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resources", value)

    @property
    @pulumi.getter(name="selectionTags")
    def selection_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectionSelectionTagArgs']]]]:
        """
        Tag-based conditions used to specify a set of resources to assign to a backup plan.
        """
        return pulumi.get(self, "selection_tags")

    @selection_tags.setter
    def selection_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionSelectionTagArgs']]]]):
        pulumi.set(self, "selection_tags", value)


@pulumi.input_type
class _SelectionState:
    def __init__(__self__, *,
                 conditions: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionArgs']]]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 plan_id: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 selection_tags: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionSelectionTagArgs']]]] = None):
        """
        Input properties used for looking up and filtering Selection resources.
        :param pulumi.Input[Sequence[pulumi.Input['SelectionConditionArgs']]] conditions: A list of conditions that you define to assign resources to your backup plans using tags.
        :param pulumi.Input[str] iam_role_arn: The ARN of the IAM role that AWS Backup uses to authenticate when restoring and backing up the target resource. See the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/access-control.html#managed-policies) for additional information about using AWS managed policies or creating custom policies attached to the IAM role.
        :param pulumi.Input[str] name: The display name of a resource selection document.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_resources: An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to exclude from a backup plan.
        :param pulumi.Input[str] plan_id: The backup plan ID to be associated with the selection of resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to assign to a backup plan.
        :param pulumi.Input[Sequence[pulumi.Input['SelectionSelectionTagArgs']]] selection_tags: Tag-based conditions used to specify a set of resources to assign to a backup plan.
        """
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)
        if iam_role_arn is not None:
            pulumi.set(__self__, "iam_role_arn", iam_role_arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if not_resources is not None:
            pulumi.set(__self__, "not_resources", not_resources)
        if plan_id is not None:
            pulumi.set(__self__, "plan_id", plan_id)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)
        if selection_tags is not None:
            pulumi.set(__self__, "selection_tags", selection_tags)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionArgs']]]]:
        """
        A list of conditions that you define to assign resources to your backup plans using tags.
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionConditionArgs']]]]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the IAM role that AWS Backup uses to authenticate when restoring and backing up the target resource. See the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/access-control.html#managed-policies) for additional information about using AWS managed policies or creating custom policies attached to the IAM role.
        """
        return pulumi.get(self, "iam_role_arn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "iam_role_arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name of a resource selection document.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notResources")
    def not_resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to exclude from a backup plan.
        """
        return pulumi.get(self, "not_resources")

    @not_resources.setter
    def not_resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_resources", value)

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> Optional[pulumi.Input[str]]:
        """
        The backup plan ID to be associated with the selection of resources.
        """
        return pulumi.get(self, "plan_id")

    @plan_id.setter
    def plan_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "plan_id", value)

    @property
    @pulumi.getter
    def resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to assign to a backup plan.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resources", value)

    @property
    @pulumi.getter(name="selectionTags")
    def selection_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectionSelectionTagArgs']]]]:
        """
        Tag-based conditions used to specify a set of resources to assign to a backup plan.
        """
        return pulumi.get(self, "selection_tags")

    @selection_tags.setter
    def selection_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectionSelectionTagArgs']]]]):
        pulumi.set(self, "selection_tags", value)


class Selection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 conditions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['SelectionConditionArgs', 'SelectionConditionArgsDict']]]]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 plan_id: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 selection_tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['SelectionSelectionTagArgs', 'SelectionSelectionTagArgsDict']]]]] = None,
                 __props__=None):
        """
        Manages selection conditions for AWS Backup plan resources.

        ## Example Usage

        ### IAM Role

        > For more information about creating and managing IAM Roles for backups and restores, see the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/iam-service-roles.html).

        The below example creates an IAM role with the default managed IAM Policy for allowing AWS Backup to create backups.

        ```python
        import pulumi
        import pulumi_aws as aws

        assume_role = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "principals": [{
                "type": "Service",
                "identifiers": ["backup.amazonaws.com"],
            }],
            "actions": ["sts:AssumeRole"],
        }])
        example = aws.iam.Role("example",
            name="example",
            assume_role_policy=assume_role.json)
        example_role_policy_attachment = aws.iam.RolePolicyAttachment("example",
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup",
            role=example.name)
        example_selection = aws.backup.Selection("example", iam_role_arn=example.arn)
        ```

        ### Selecting Backups By Tag

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.backup.Selection("example",
            iam_role_arn=example_aws_iam_role["arn"],
            name="my_example_backup_selection",
            plan_id=example_aws_backup_plan["id"],
            selection_tags=[{
                "type": "STRINGEQUALS",
                "key": "foo",
                "value": "bar",
            }])
        ```

        ### Selecting Backups By Conditions

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.backup.Selection("example",
            iam_role_arn=example_aws_iam_role["arn"],
            name="my_example_backup_selection",
            plan_id=example_aws_backup_plan["id"],
            resources=["*"],
            conditions=[{
                "string_equals": [{
                    "key": "aws:ResourceTag/Component",
                    "value": "rds",
                }],
                "string_likes": [{
                    "key": "aws:ResourceTag/Application",
                    "value": "app*",
                }],
                "string_not_equals": [{
                    "key": "aws:ResourceTag/Backup",
                    "value": "false",
                }],
                "string_not_likes": [{
                    "key": "aws:ResourceTag/Environment",
                    "value": "test*",
                }],
            }])
        ```

        ### Selecting Backups By Resource

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.backup.Selection("example",
            iam_role_arn=example_aws_iam_role["arn"],
            name="my_example_backup_selection",
            plan_id=example_aws_backup_plan["id"],
            resources=[
                example_aws_db_instance["arn"],
                example_aws_ebs_volume["arn"],
                example_aws_efs_file_system["arn"],
            ])
        ```

        ### Selecting Backups By Not Resource

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.backup.Selection("example",
            iam_role_arn=example_aws_iam_role["arn"],
            name="my_example_backup_selection",
            plan_id=example_aws_backup_plan["id"],
            not_resources=[
                example_aws_db_instance["arn"],
                example_aws_ebs_volume["arn"],
                example_aws_efs_file_system["arn"],
            ])
        ```

        ## Import

        Using `pulumi import`, import Backup selection using the role plan_id and id separated by `|`. For example:

        ```sh
        $ pulumi import aws:backup/selection:Selection example plan-id|selection-id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['SelectionConditionArgs', 'SelectionConditionArgsDict']]]] conditions: A list of conditions that you define to assign resources to your backup plans using tags.
        :param pulumi.Input[str] iam_role_arn: The ARN of the IAM role that AWS Backup uses to authenticate when restoring and backing up the target resource. See the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/access-control.html#managed-policies) for additional information about using AWS managed policies or creating custom policies attached to the IAM role.
        :param pulumi.Input[str] name: The display name of a resource selection document.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_resources: An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to exclude from a backup plan.
        :param pulumi.Input[str] plan_id: The backup plan ID to be associated with the selection of resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to assign to a backup plan.
        :param pulumi.Input[Sequence[pulumi.Input[Union['SelectionSelectionTagArgs', 'SelectionSelectionTagArgsDict']]]] selection_tags: Tag-based conditions used to specify a set of resources to assign to a backup plan.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SelectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages selection conditions for AWS Backup plan resources.

        ## Example Usage

        ### IAM Role

        > For more information about creating and managing IAM Roles for backups and restores, see the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/iam-service-roles.html).

        The below example creates an IAM role with the default managed IAM Policy for allowing AWS Backup to create backups.

        ```python
        import pulumi
        import pulumi_aws as aws

        assume_role = aws.iam.get_policy_document(statements=[{
            "effect": "Allow",
            "principals": [{
                "type": "Service",
                "identifiers": ["backup.amazonaws.com"],
            }],
            "actions": ["sts:AssumeRole"],
        }])
        example = aws.iam.Role("example",
            name="example",
            assume_role_policy=assume_role.json)
        example_role_policy_attachment = aws.iam.RolePolicyAttachment("example",
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup",
            role=example.name)
        example_selection = aws.backup.Selection("example", iam_role_arn=example.arn)
        ```

        ### Selecting Backups By Tag

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.backup.Selection("example",
            iam_role_arn=example_aws_iam_role["arn"],
            name="my_example_backup_selection",
            plan_id=example_aws_backup_plan["id"],
            selection_tags=[{
                "type": "STRINGEQUALS",
                "key": "foo",
                "value": "bar",
            }])
        ```

        ### Selecting Backups By Conditions

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.backup.Selection("example",
            iam_role_arn=example_aws_iam_role["arn"],
            name="my_example_backup_selection",
            plan_id=example_aws_backup_plan["id"],
            resources=["*"],
            conditions=[{
                "string_equals": [{
                    "key": "aws:ResourceTag/Component",
                    "value": "rds",
                }],
                "string_likes": [{
                    "key": "aws:ResourceTag/Application",
                    "value": "app*",
                }],
                "string_not_equals": [{
                    "key": "aws:ResourceTag/Backup",
                    "value": "false",
                }],
                "string_not_likes": [{
                    "key": "aws:ResourceTag/Environment",
                    "value": "test*",
                }],
            }])
        ```

        ### Selecting Backups By Resource

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.backup.Selection("example",
            iam_role_arn=example_aws_iam_role["arn"],
            name="my_example_backup_selection",
            plan_id=example_aws_backup_plan["id"],
            resources=[
                example_aws_db_instance["arn"],
                example_aws_ebs_volume["arn"],
                example_aws_efs_file_system["arn"],
            ])
        ```

        ### Selecting Backups By Not Resource

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.backup.Selection("example",
            iam_role_arn=example_aws_iam_role["arn"],
            name="my_example_backup_selection",
            plan_id=example_aws_backup_plan["id"],
            not_resources=[
                example_aws_db_instance["arn"],
                example_aws_ebs_volume["arn"],
                example_aws_efs_file_system["arn"],
            ])
        ```

        ## Import

        Using `pulumi import`, import Backup selection using the role plan_id and id separated by `|`. For example:

        ```sh
        $ pulumi import aws:backup/selection:Selection example plan-id|selection-id
        ```

        :param str resource_name: The name of the resource.
        :param SelectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SelectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 conditions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['SelectionConditionArgs', 'SelectionConditionArgsDict']]]]] = None,
                 iam_role_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 plan_id: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 selection_tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['SelectionSelectionTagArgs', 'SelectionSelectionTagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SelectionArgs.__new__(SelectionArgs)

            __props__.__dict__["conditions"] = conditions
            if iam_role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'iam_role_arn'")
            __props__.__dict__["iam_role_arn"] = iam_role_arn
            __props__.__dict__["name"] = name
            __props__.__dict__["not_resources"] = not_resources
            if plan_id is None and not opts.urn:
                raise TypeError("Missing required property 'plan_id'")
            __props__.__dict__["plan_id"] = plan_id
            __props__.__dict__["resources"] = resources
            __props__.__dict__["selection_tags"] = selection_tags
        super(Selection, __self__).__init__(
            'aws:backup/selection:Selection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            conditions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['SelectionConditionArgs', 'SelectionConditionArgsDict']]]]] = None,
            iam_role_arn: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            not_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            plan_id: Optional[pulumi.Input[str]] = None,
            resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            selection_tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['SelectionSelectionTagArgs', 'SelectionSelectionTagArgsDict']]]]] = None) -> 'Selection':
        """
        Get an existing Selection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['SelectionConditionArgs', 'SelectionConditionArgsDict']]]] conditions: A list of conditions that you define to assign resources to your backup plans using tags.
        :param pulumi.Input[str] iam_role_arn: The ARN of the IAM role that AWS Backup uses to authenticate when restoring and backing up the target resource. See the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/access-control.html#managed-policies) for additional information about using AWS managed policies or creating custom policies attached to the IAM role.
        :param pulumi.Input[str] name: The display name of a resource selection document.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_resources: An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to exclude from a backup plan.
        :param pulumi.Input[str] plan_id: The backup plan ID to be associated with the selection of resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to assign to a backup plan.
        :param pulumi.Input[Sequence[pulumi.Input[Union['SelectionSelectionTagArgs', 'SelectionSelectionTagArgsDict']]]] selection_tags: Tag-based conditions used to specify a set of resources to assign to a backup plan.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SelectionState.__new__(_SelectionState)

        __props__.__dict__["conditions"] = conditions
        __props__.__dict__["iam_role_arn"] = iam_role_arn
        __props__.__dict__["name"] = name
        __props__.__dict__["not_resources"] = not_resources
        __props__.__dict__["plan_id"] = plan_id
        __props__.__dict__["resources"] = resources
        __props__.__dict__["selection_tags"] = selection_tags
        return Selection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def conditions(self) -> pulumi.Output[Sequence['outputs.SelectionCondition']]:
        """
        A list of conditions that you define to assign resources to your backup plans using tags.
        """
        return pulumi.get(self, "conditions")

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the IAM role that AWS Backup uses to authenticate when restoring and backing up the target resource. See the [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/access-control.html#managed-policies) for additional information about using AWS managed policies or creating custom policies attached to the IAM role.
        """
        return pulumi.get(self, "iam_role_arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The display name of a resource selection document.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notResources")
    def not_resources(self) -> pulumi.Output[Sequence[str]]:
        """
        An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to exclude from a backup plan.
        """
        return pulumi.get(self, "not_resources")

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> pulumi.Output[str]:
        """
        The backup plan ID to be associated with the selection of resources.
        """
        return pulumi.get(self, "plan_id")

    @property
    @pulumi.getter
    def resources(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        An array of strings that either contain Amazon Resource Names (ARNs) or match patterns of resources to assign to a backup plan.
        """
        return pulumi.get(self, "resources")

    @property
    @pulumi.getter(name="selectionTags")
    def selection_tags(self) -> pulumi.Output[Optional[Sequence['outputs.SelectionSelectionTag']]]:
        """
        Tag-based conditions used to specify a set of resources to assign to a backup plan.
        """
        return pulumi.get(self, "selection_tags")

