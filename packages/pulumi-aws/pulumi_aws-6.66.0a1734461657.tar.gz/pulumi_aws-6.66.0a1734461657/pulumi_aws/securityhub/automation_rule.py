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

__all__ = ['AutomationRuleArgs', 'AutomationRule']

@pulumi.input_type
class AutomationRuleArgs:
    def __init__(__self__, *,
                 description: pulumi.Input[str],
                 rule_name: pulumi.Input[str],
                 rule_order: pulumi.Input[int],
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRuleActionArgs']]]] = None,
                 criteria: Optional[pulumi.Input['AutomationRuleCriteriaArgs']] = None,
                 is_terminal: Optional[pulumi.Input[bool]] = None,
                 rule_status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AutomationRule resource.
        :param pulumi.Input[str] description: The description of the rule.
        :param pulumi.Input[str] rule_name: The name of the rule.
        :param pulumi.Input[int] rule_order: An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings. Security Hub applies rules with lower values for this parameter first.
        :param pulumi.Input[Sequence[pulumi.Input['AutomationRuleActionArgs']]] actions: A block that specifies one or more actions to update finding fields if a finding matches the conditions specified in `Criteria`. Documented below.
        :param pulumi.Input['AutomationRuleCriteriaArgs'] criteria: A block that specifies a set of ASFF finding field attributes and corresponding expected values that Security Hub uses to filter findings. Documented below.
        :param pulumi.Input[bool] is_terminal: Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria. Defaults to `false`.
        :param pulumi.Input[str] rule_status: Whether the rule is active after it is created.
        """
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "rule_name", rule_name)
        pulumi.set(__self__, "rule_order", rule_order)
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if criteria is not None:
            pulumi.set(__self__, "criteria", criteria)
        if is_terminal is not None:
            pulumi.set(__self__, "is_terminal", is_terminal)
        if rule_status is not None:
            pulumi.set(__self__, "rule_status", rule_status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        The description of the rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Input[str]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter(name="ruleOrder")
    def rule_order(self) -> pulumi.Input[int]:
        """
        An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings. Security Hub applies rules with lower values for this parameter first.
        """
        return pulumi.get(self, "rule_order")

    @rule_order.setter
    def rule_order(self, value: pulumi.Input[int]):
        pulumi.set(self, "rule_order", value)

    @property
    @pulumi.getter
    def actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRuleActionArgs']]]]:
        """
        A block that specifies one or more actions to update finding fields if a finding matches the conditions specified in `Criteria`. Documented below.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRuleActionArgs']]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter
    def criteria(self) -> Optional[pulumi.Input['AutomationRuleCriteriaArgs']]:
        """
        A block that specifies a set of ASFF finding field attributes and corresponding expected values that Security Hub uses to filter findings. Documented below.
        """
        return pulumi.get(self, "criteria")

    @criteria.setter
    def criteria(self, value: Optional[pulumi.Input['AutomationRuleCriteriaArgs']]):
        pulumi.set(self, "criteria", value)

    @property
    @pulumi.getter(name="isTerminal")
    def is_terminal(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria. Defaults to `false`.
        """
        return pulumi.get(self, "is_terminal")

    @is_terminal.setter
    def is_terminal(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_terminal", value)

    @property
    @pulumi.getter(name="ruleStatus")
    def rule_status(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the rule is active after it is created.
        """
        return pulumi.get(self, "rule_status")

    @rule_status.setter
    def rule_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AutomationRuleState:
    def __init__(__self__, *,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRuleActionArgs']]]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 criteria: Optional[pulumi.Input['AutomationRuleCriteriaArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_terminal: Optional[pulumi.Input[bool]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 rule_order: Optional[pulumi.Input[int]] = None,
                 rule_status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering AutomationRule resources.
        :param pulumi.Input[Sequence[pulumi.Input['AutomationRuleActionArgs']]] actions: A block that specifies one or more actions to update finding fields if a finding matches the conditions specified in `Criteria`. Documented below.
        :param pulumi.Input[str] arn: The ARN of the Security Hub automation rule.
        :param pulumi.Input['AutomationRuleCriteriaArgs'] criteria: A block that specifies a set of ASFF finding field attributes and corresponding expected values that Security Hub uses to filter findings. Documented below.
        :param pulumi.Input[str] description: The description of the rule.
        :param pulumi.Input[bool] is_terminal: Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria. Defaults to `false`.
        :param pulumi.Input[str] rule_name: The name of the rule.
        :param pulumi.Input[int] rule_order: An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings. Security Hub applies rules with lower values for this parameter first.
        :param pulumi.Input[str] rule_status: Whether the rule is active after it is created.
        """
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if criteria is not None:
            pulumi.set(__self__, "criteria", criteria)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if is_terminal is not None:
            pulumi.set(__self__, "is_terminal", is_terminal)
        if rule_name is not None:
            pulumi.set(__self__, "rule_name", rule_name)
        if rule_order is not None:
            pulumi.set(__self__, "rule_order", rule_order)
        if rule_status is not None:
            pulumi.set(__self__, "rule_status", rule_status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRuleActionArgs']]]]:
        """
        A block that specifies one or more actions to update finding fields if a finding matches the conditions specified in `Criteria`. Documented below.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRuleActionArgs']]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the Security Hub automation rule.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def criteria(self) -> Optional[pulumi.Input['AutomationRuleCriteriaArgs']]:
        """
        A block that specifies a set of ASFF finding field attributes and corresponding expected values that Security Hub uses to filter findings. Documented below.
        """
        return pulumi.get(self, "criteria")

    @criteria.setter
    def criteria(self, value: Optional[pulumi.Input['AutomationRuleCriteriaArgs']]):
        pulumi.set(self, "criteria", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="isTerminal")
    def is_terminal(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria. Defaults to `false`.
        """
        return pulumi.get(self, "is_terminal")

    @is_terminal.setter
    def is_terminal(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_terminal", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter(name="ruleOrder")
    def rule_order(self) -> Optional[pulumi.Input[int]]:
        """
        An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings. Security Hub applies rules with lower values for this parameter first.
        """
        return pulumi.get(self, "rule_order")

    @rule_order.setter
    def rule_order(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "rule_order", value)

    @property
    @pulumi.getter(name="ruleStatus")
    def rule_status(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the rule is active after it is created.
        """
        return pulumi.get(self, "rule_status")

    @rule_status.setter
    def rule_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    @_utilities.deprecated("""Please use `tags` instead.""")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class AutomationRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['AutomationRuleActionArgs', 'AutomationRuleActionArgsDict']]]]] = None,
                 criteria: Optional[pulumi.Input[Union['AutomationRuleCriteriaArgs', 'AutomationRuleCriteriaArgsDict']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_terminal: Optional[pulumi.Input[bool]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 rule_order: Optional[pulumi.Input[int]] = None,
                 rule_status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Security Hub Automation Rule.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.securityhub.AutomationRule("example",
            description="Elevate finding severity to CRITICAL when specific resources such as an S3 bucket is at risk",
            rule_name="Elevate severity of findings that relate to important resources",
            rule_order=1,
            actions=[{
                "finding_fields_update": {
                    "severity": {
                        "label": "CRITICAL",
                        "product": 0,
                    },
                    "note": {
                        "text": "This is a critical resource. Please review ASAP.",
                        "updated_by": "sechub-automation",
                    },
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards"],
                    "user_defined_fields": {
                        "key": "value",
                    },
                },
                "type": "FINDING_FIELDS_UPDATE",
            }],
            criteria={
                "resource_ids": [{
                    "comparison": "EQUALS",
                    "value": "arn:aws:s3:::examplebucket/*",
                }],
            })
        ```

        ## Import

        Using `pulumi import`, import Security Hub automation rule using their ARN. For example:

        ```sh
        $ pulumi import aws:securityhub/automationRule:AutomationRule example arn:aws:securityhub:us-west-2:123456789012:automation-rule/473eddde-f5c4-4ae5-85c7-e922f271fffc
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['AutomationRuleActionArgs', 'AutomationRuleActionArgsDict']]]] actions: A block that specifies one or more actions to update finding fields if a finding matches the conditions specified in `Criteria`. Documented below.
        :param pulumi.Input[Union['AutomationRuleCriteriaArgs', 'AutomationRuleCriteriaArgsDict']] criteria: A block that specifies a set of ASFF finding field attributes and corresponding expected values that Security Hub uses to filter findings. Documented below.
        :param pulumi.Input[str] description: The description of the rule.
        :param pulumi.Input[bool] is_terminal: Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria. Defaults to `false`.
        :param pulumi.Input[str] rule_name: The name of the rule.
        :param pulumi.Input[int] rule_order: An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings. Security Hub applies rules with lower values for this parameter first.
        :param pulumi.Input[str] rule_status: Whether the rule is active after it is created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AutomationRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Security Hub Automation Rule.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.securityhub.AutomationRule("example",
            description="Elevate finding severity to CRITICAL when specific resources such as an S3 bucket is at risk",
            rule_name="Elevate severity of findings that relate to important resources",
            rule_order=1,
            actions=[{
                "finding_fields_update": {
                    "severity": {
                        "label": "CRITICAL",
                        "product": 0,
                    },
                    "note": {
                        "text": "This is a critical resource. Please review ASAP.",
                        "updated_by": "sechub-automation",
                    },
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards"],
                    "user_defined_fields": {
                        "key": "value",
                    },
                },
                "type": "FINDING_FIELDS_UPDATE",
            }],
            criteria={
                "resource_ids": [{
                    "comparison": "EQUALS",
                    "value": "arn:aws:s3:::examplebucket/*",
                }],
            })
        ```

        ## Import

        Using `pulumi import`, import Security Hub automation rule using their ARN. For example:

        ```sh
        $ pulumi import aws:securityhub/automationRule:AutomationRule example arn:aws:securityhub:us-west-2:123456789012:automation-rule/473eddde-f5c4-4ae5-85c7-e922f271fffc
        ```

        :param str resource_name: The name of the resource.
        :param AutomationRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AutomationRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['AutomationRuleActionArgs', 'AutomationRuleActionArgsDict']]]]] = None,
                 criteria: Optional[pulumi.Input[Union['AutomationRuleCriteriaArgs', 'AutomationRuleCriteriaArgsDict']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_terminal: Optional[pulumi.Input[bool]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 rule_order: Optional[pulumi.Input[int]] = None,
                 rule_status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AutomationRuleArgs.__new__(AutomationRuleArgs)

            __props__.__dict__["actions"] = actions
            __props__.__dict__["criteria"] = criteria
            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            __props__.__dict__["is_terminal"] = is_terminal
            if rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'rule_name'")
            __props__.__dict__["rule_name"] = rule_name
            if rule_order is None and not opts.urn:
                raise TypeError("Missing required property 'rule_order'")
            __props__.__dict__["rule_order"] = rule_order
            __props__.__dict__["rule_status"] = rule_status
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(AutomationRule, __self__).__init__(
            'aws:securityhub/automationRule:AutomationRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            actions: Optional[pulumi.Input[Sequence[pulumi.Input[Union['AutomationRuleActionArgs', 'AutomationRuleActionArgsDict']]]]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            criteria: Optional[pulumi.Input[Union['AutomationRuleCriteriaArgs', 'AutomationRuleCriteriaArgsDict']]] = None,
            description: Optional[pulumi.Input[str]] = None,
            is_terminal: Optional[pulumi.Input[bool]] = None,
            rule_name: Optional[pulumi.Input[str]] = None,
            rule_order: Optional[pulumi.Input[int]] = None,
            rule_status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'AutomationRule':
        """
        Get an existing AutomationRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['AutomationRuleActionArgs', 'AutomationRuleActionArgsDict']]]] actions: A block that specifies one or more actions to update finding fields if a finding matches the conditions specified in `Criteria`. Documented below.
        :param pulumi.Input[str] arn: The ARN of the Security Hub automation rule.
        :param pulumi.Input[Union['AutomationRuleCriteriaArgs', 'AutomationRuleCriteriaArgsDict']] criteria: A block that specifies a set of ASFF finding field attributes and corresponding expected values that Security Hub uses to filter findings. Documented below.
        :param pulumi.Input[str] description: The description of the rule.
        :param pulumi.Input[bool] is_terminal: Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria. Defaults to `false`.
        :param pulumi.Input[str] rule_name: The name of the rule.
        :param pulumi.Input[int] rule_order: An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings. Security Hub applies rules with lower values for this parameter first.
        :param pulumi.Input[str] rule_status: Whether the rule is active after it is created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AutomationRuleState.__new__(_AutomationRuleState)

        __props__.__dict__["actions"] = actions
        __props__.__dict__["arn"] = arn
        __props__.__dict__["criteria"] = criteria
        __props__.__dict__["description"] = description
        __props__.__dict__["is_terminal"] = is_terminal
        __props__.__dict__["rule_name"] = rule_name
        __props__.__dict__["rule_order"] = rule_order
        __props__.__dict__["rule_status"] = rule_status
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return AutomationRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Output[Optional[Sequence['outputs.AutomationRuleAction']]]:
        """
        A block that specifies one or more actions to update finding fields if a finding matches the conditions specified in `Criteria`. Documented below.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Security Hub automation rule.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def criteria(self) -> pulumi.Output[Optional['outputs.AutomationRuleCriteria']]:
        """
        A block that specifies a set of ASFF finding field attributes and corresponding expected values that Security Hub uses to filter findings. Documented below.
        """
        return pulumi.get(self, "criteria")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        The description of the rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="isTerminal")
    def is_terminal(self) -> pulumi.Output[bool]:
        """
        Specifies whether a rule is the last to be applied with respect to a finding that matches the rule criteria. Defaults to `false`.
        """
        return pulumi.get(self, "is_terminal")

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> pulumi.Output[str]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "rule_name")

    @property
    @pulumi.getter(name="ruleOrder")
    def rule_order(self) -> pulumi.Output[int]:
        """
        An integer ranging from 1 to 1000 that represents the order in which the rule action is applied to findings. Security Hub applies rules with lower values for this parameter first.
        """
        return pulumi.get(self, "rule_order")

    @property
    @pulumi.getter(name="ruleStatus")
    def rule_status(self) -> pulumi.Output[str]:
        """
        Whether the rule is active after it is created.
        """
        return pulumi.get(self, "rule_status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    @_utilities.deprecated("""Please use `tags` instead.""")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "tags_all")

