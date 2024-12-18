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

__all__ = ['DomainArgs', 'Domain']

@pulumi.input_type
class DomainArgs:
    def __init__(__self__, *,
                 domain_execution_role: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 kms_key_identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 single_sign_on: Optional[pulumi.Input['DomainSingleSignOnArgs']] = None,
                 skip_deletion_check: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeouts: Optional[pulumi.Input['DomainTimeoutsArgs']] = None):
        """
        The set of arguments for constructing a Domain resource.
        :param pulumi.Input[str] domain_execution_role: ARN of the role used by DataZone to configure the Domain.
               
               The following arguments are optional:
        :param pulumi.Input[str] description: Description of the Domain.
        :param pulumi.Input[str] kms_key_identifier: ARN of the KMS key used to encrypt the Amazon DataZone domain, metadata and reporting data.
        :param pulumi.Input[str] name: Name of the Domain.
        :param pulumi.Input['DomainSingleSignOnArgs'] single_sign_on: Single sign on options, used to [enable AWS IAM Identity Center](https://docs.aws.amazon.com/datazone/latest/userguide/enable-IAM-identity-center-for-datazone.html) for DataZone.
        :param pulumi.Input[bool] skip_deletion_check: Whether to skip the deletion check for the Domain.
        """
        pulumi.set(__self__, "domain_execution_role", domain_execution_role)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kms_key_identifier is not None:
            pulumi.set(__self__, "kms_key_identifier", kms_key_identifier)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if single_sign_on is not None:
            pulumi.set(__self__, "single_sign_on", single_sign_on)
        if skip_deletion_check is not None:
            pulumi.set(__self__, "skip_deletion_check", skip_deletion_check)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="domainExecutionRole")
    def domain_execution_role(self) -> pulumi.Input[str]:
        """
        ARN of the role used by DataZone to configure the Domain.

        The following arguments are optional:
        """
        return pulumi.get(self, "domain_execution_role")

    @domain_execution_role.setter
    def domain_execution_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_execution_role", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the Domain.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the KMS key used to encrypt the Amazon DataZone domain, metadata and reporting data.
        """
        return pulumi.get(self, "kms_key_identifier")

    @kms_key_identifier.setter
    def kms_key_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_identifier", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Domain.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="singleSignOn")
    def single_sign_on(self) -> Optional[pulumi.Input['DomainSingleSignOnArgs']]:
        """
        Single sign on options, used to [enable AWS IAM Identity Center](https://docs.aws.amazon.com/datazone/latest/userguide/enable-IAM-identity-center-for-datazone.html) for DataZone.
        """
        return pulumi.get(self, "single_sign_on")

    @single_sign_on.setter
    def single_sign_on(self, value: Optional[pulumi.Input['DomainSingleSignOnArgs']]):
        pulumi.set(self, "single_sign_on", value)

    @property
    @pulumi.getter(name="skipDeletionCheck")
    def skip_deletion_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to skip the deletion check for the Domain.
        """
        return pulumi.get(self, "skip_deletion_check")

    @skip_deletion_check.setter
    def skip_deletion_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_deletion_check", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['DomainTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['DomainTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


@pulumi.input_type
class _DomainState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain_execution_role: Optional[pulumi.Input[str]] = None,
                 kms_key_identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 portal_url: Optional[pulumi.Input[str]] = None,
                 single_sign_on: Optional[pulumi.Input['DomainSingleSignOnArgs']] = None,
                 skip_deletion_check: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeouts: Optional[pulumi.Input['DomainTimeoutsArgs']] = None):
        """
        Input properties used for looking up and filtering Domain resources.
        :param pulumi.Input[str] arn: ARN of the Domain.
        :param pulumi.Input[str] description: Description of the Domain.
        :param pulumi.Input[str] domain_execution_role: ARN of the role used by DataZone to configure the Domain.
               
               The following arguments are optional:
        :param pulumi.Input[str] kms_key_identifier: ARN of the KMS key used to encrypt the Amazon DataZone domain, metadata and reporting data.
        :param pulumi.Input[str] name: Name of the Domain.
        :param pulumi.Input[str] portal_url: URL of the data portal for the Domain.
        :param pulumi.Input['DomainSingleSignOnArgs'] single_sign_on: Single sign on options, used to [enable AWS IAM Identity Center](https://docs.aws.amazon.com/datazone/latest/userguide/enable-IAM-identity-center-for-datazone.html) for DataZone.
        :param pulumi.Input[bool] skip_deletion_check: Whether to skip the deletion check for the Domain.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if domain_execution_role is not None:
            pulumi.set(__self__, "domain_execution_role", domain_execution_role)
        if kms_key_identifier is not None:
            pulumi.set(__self__, "kms_key_identifier", kms_key_identifier)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if portal_url is not None:
            pulumi.set(__self__, "portal_url", portal_url)
        if single_sign_on is not None:
            pulumi.set(__self__, "single_sign_on", single_sign_on)
        if skip_deletion_check is not None:
            pulumi.set(__self__, "skip_deletion_check", skip_deletion_check)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Domain.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the Domain.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="domainExecutionRole")
    def domain_execution_role(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the role used by DataZone to configure the Domain.

        The following arguments are optional:
        """
        return pulumi.get(self, "domain_execution_role")

    @domain_execution_role.setter
    def domain_execution_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_execution_role", value)

    @property
    @pulumi.getter(name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the KMS key used to encrypt the Amazon DataZone domain, metadata and reporting data.
        """
        return pulumi.get(self, "kms_key_identifier")

    @kms_key_identifier.setter
    def kms_key_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_identifier", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Domain.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="portalUrl")
    def portal_url(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the data portal for the Domain.
        """
        return pulumi.get(self, "portal_url")

    @portal_url.setter
    def portal_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "portal_url", value)

    @property
    @pulumi.getter(name="singleSignOn")
    def single_sign_on(self) -> Optional[pulumi.Input['DomainSingleSignOnArgs']]:
        """
        Single sign on options, used to [enable AWS IAM Identity Center](https://docs.aws.amazon.com/datazone/latest/userguide/enable-IAM-identity-center-for-datazone.html) for DataZone.
        """
        return pulumi.get(self, "single_sign_on")

    @single_sign_on.setter
    def single_sign_on(self, value: Optional[pulumi.Input['DomainSingleSignOnArgs']]):
        pulumi.set(self, "single_sign_on", value)

    @property
    @pulumi.getter(name="skipDeletionCheck")
    def skip_deletion_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to skip the deletion check for the Domain.
        """
        return pulumi.get(self, "skip_deletion_check")

    @skip_deletion_check.setter
    def skip_deletion_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_deletion_check", value)

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
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['DomainTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['DomainTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


class Domain(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain_execution_role: Optional[pulumi.Input[str]] = None,
                 kms_key_identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 single_sign_on: Optional[pulumi.Input[Union['DomainSingleSignOnArgs', 'DomainSingleSignOnArgsDict']]] = None,
                 skip_deletion_check: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeouts: Optional[pulumi.Input[Union['DomainTimeoutsArgs', 'DomainTimeoutsArgsDict']]] = None,
                 __props__=None):
        """
        Resource for managing an AWS DataZone Domain.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        domain_execution_role = aws.iam.Role("domain_execution_role",
            name="my_domain_execution_role",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": [
                            "sts:AssumeRole",
                            "sts:TagSession",
                        ],
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "datazone.amazonaws.com",
                        },
                    },
                    {
                        "Action": [
                            "sts:AssumeRole",
                            "sts:TagSession",
                        ],
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "cloudformation.amazonaws.com",
                        },
                    },
                ],
            }),
            inline_policies=[{
                "name": "domain_execution_policy",
                "policy": json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Action": [
                            "datazone:*",
                            "ram:*",
                            "sso:*",
                            "kms:*",
                        ],
                        "Effect": "Allow",
                        "Resource": "*",
                    }],
                }),
            }])
        example = aws.datazone.Domain("example",
            name="example",
            domain_execution_role=domain_execution_role.arn)
        ```

        ## Import

        Using `pulumi import`, import DataZone Domain using the `domain_id`. For example:

        ```sh
        $ pulumi import aws:datazone/domain:Domain example domain-id-12345678
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the Domain.
        :param pulumi.Input[str] domain_execution_role: ARN of the role used by DataZone to configure the Domain.
               
               The following arguments are optional:
        :param pulumi.Input[str] kms_key_identifier: ARN of the KMS key used to encrypt the Amazon DataZone domain, metadata and reporting data.
        :param pulumi.Input[str] name: Name of the Domain.
        :param pulumi.Input[Union['DomainSingleSignOnArgs', 'DomainSingleSignOnArgsDict']] single_sign_on: Single sign on options, used to [enable AWS IAM Identity Center](https://docs.aws.amazon.com/datazone/latest/userguide/enable-IAM-identity-center-for-datazone.html) for DataZone.
        :param pulumi.Input[bool] skip_deletion_check: Whether to skip the deletion check for the Domain.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DomainArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS DataZone Domain.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        domain_execution_role = aws.iam.Role("domain_execution_role",
            name="my_domain_execution_role",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": [
                            "sts:AssumeRole",
                            "sts:TagSession",
                        ],
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "datazone.amazonaws.com",
                        },
                    },
                    {
                        "Action": [
                            "sts:AssumeRole",
                            "sts:TagSession",
                        ],
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "cloudformation.amazonaws.com",
                        },
                    },
                ],
            }),
            inline_policies=[{
                "name": "domain_execution_policy",
                "policy": json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Action": [
                            "datazone:*",
                            "ram:*",
                            "sso:*",
                            "kms:*",
                        ],
                        "Effect": "Allow",
                        "Resource": "*",
                    }],
                }),
            }])
        example = aws.datazone.Domain("example",
            name="example",
            domain_execution_role=domain_execution_role.arn)
        ```

        ## Import

        Using `pulumi import`, import DataZone Domain using the `domain_id`. For example:

        ```sh
        $ pulumi import aws:datazone/domain:Domain example domain-id-12345678
        ```

        :param str resource_name: The name of the resource.
        :param DomainArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DomainArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain_execution_role: Optional[pulumi.Input[str]] = None,
                 kms_key_identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 single_sign_on: Optional[pulumi.Input[Union['DomainSingleSignOnArgs', 'DomainSingleSignOnArgsDict']]] = None,
                 skip_deletion_check: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeouts: Optional[pulumi.Input[Union['DomainTimeoutsArgs', 'DomainTimeoutsArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DomainArgs.__new__(DomainArgs)

            __props__.__dict__["description"] = description
            if domain_execution_role is None and not opts.urn:
                raise TypeError("Missing required property 'domain_execution_role'")
            __props__.__dict__["domain_execution_role"] = domain_execution_role
            __props__.__dict__["kms_key_identifier"] = kms_key_identifier
            __props__.__dict__["name"] = name
            __props__.__dict__["single_sign_on"] = single_sign_on
            __props__.__dict__["skip_deletion_check"] = skip_deletion_check
            __props__.__dict__["tags"] = tags
            __props__.__dict__["timeouts"] = timeouts
            __props__.__dict__["arn"] = None
            __props__.__dict__["portal_url"] = None
            __props__.__dict__["tags_all"] = None
        super(Domain, __self__).__init__(
            'aws:datazone/domain:Domain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            domain_execution_role: Optional[pulumi.Input[str]] = None,
            kms_key_identifier: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            portal_url: Optional[pulumi.Input[str]] = None,
            single_sign_on: Optional[pulumi.Input[Union['DomainSingleSignOnArgs', 'DomainSingleSignOnArgsDict']]] = None,
            skip_deletion_check: Optional[pulumi.Input[bool]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            timeouts: Optional[pulumi.Input[Union['DomainTimeoutsArgs', 'DomainTimeoutsArgsDict']]] = None) -> 'Domain':
        """
        Get an existing Domain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the Domain.
        :param pulumi.Input[str] description: Description of the Domain.
        :param pulumi.Input[str] domain_execution_role: ARN of the role used by DataZone to configure the Domain.
               
               The following arguments are optional:
        :param pulumi.Input[str] kms_key_identifier: ARN of the KMS key used to encrypt the Amazon DataZone domain, metadata and reporting data.
        :param pulumi.Input[str] name: Name of the Domain.
        :param pulumi.Input[str] portal_url: URL of the data portal for the Domain.
        :param pulumi.Input[Union['DomainSingleSignOnArgs', 'DomainSingleSignOnArgsDict']] single_sign_on: Single sign on options, used to [enable AWS IAM Identity Center](https://docs.aws.amazon.com/datazone/latest/userguide/enable-IAM-identity-center-for-datazone.html) for DataZone.
        :param pulumi.Input[bool] skip_deletion_check: Whether to skip the deletion check for the Domain.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DomainState.__new__(_DomainState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["description"] = description
        __props__.__dict__["domain_execution_role"] = domain_execution_role
        __props__.__dict__["kms_key_identifier"] = kms_key_identifier
        __props__.__dict__["name"] = name
        __props__.__dict__["portal_url"] = portal_url
        __props__.__dict__["single_sign_on"] = single_sign_on
        __props__.__dict__["skip_deletion_check"] = skip_deletion_check
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["timeouts"] = timeouts
        return Domain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Domain.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the Domain.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="domainExecutionRole")
    def domain_execution_role(self) -> pulumi.Output[str]:
        """
        ARN of the role used by DataZone to configure the Domain.

        The following arguments are optional:
        """
        return pulumi.get(self, "domain_execution_role")

    @property
    @pulumi.getter(name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        ARN of the KMS key used to encrypt the Amazon DataZone domain, metadata and reporting data.
        """
        return pulumi.get(self, "kms_key_identifier")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the Domain.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="portalUrl")
    def portal_url(self) -> pulumi.Output[str]:
        """
        URL of the data portal for the Domain.
        """
        return pulumi.get(self, "portal_url")

    @property
    @pulumi.getter(name="singleSignOn")
    def single_sign_on(self) -> pulumi.Output[Optional['outputs.DomainSingleSignOn']]:
        """
        Single sign on options, used to [enable AWS IAM Identity Center](https://docs.aws.amazon.com/datazone/latest/userguide/enable-IAM-identity-center-for-datazone.html) for DataZone.
        """
        return pulumi.get(self, "single_sign_on")

    @property
    @pulumi.getter(name="skipDeletionCheck")
    def skip_deletion_check(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to skip the deletion check for the Domain.
        """
        return pulumi.get(self, "skip_deletion_check")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    @_utilities.deprecated("""Please use `tags` instead.""")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def timeouts(self) -> pulumi.Output[Optional['outputs.DomainTimeouts']]:
        return pulumi.get(self, "timeouts")

