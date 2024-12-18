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

__all__ = ['IntegrationArgs', 'Integration']

@pulumi.input_type
class IntegrationArgs:
    def __init__(__self__, *,
                 integration_name: pulumi.Input[str],
                 source_arn: pulumi.Input[str],
                 target_arn: pulumi.Input[str],
                 additional_encryption_context: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timeouts: Optional[pulumi.Input['IntegrationTimeoutsArgs']] = None):
        """
        The set of arguments for constructing a Integration resource.
        :param pulumi.Input[str] integration_name: Name of the integration.
        :param pulumi.Input[str] source_arn: ARN of the database to use as the source for replication.
        :param pulumi.Input[str] target_arn: ARN of the Redshift data warehouse to use as the target for replication.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] additional_encryption_context: Set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see the [User Guide](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context). You can only include this parameter if you specify the `kms_key_id` parameter.
        :param pulumi.Input[str] kms_key_id: KMS key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key. If you use the default AWS owned key, you should ignore `kms_key_id` parameter by using `lifecycle` parameter to avoid unintended change after the first creation.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "integration_name", integration_name)
        pulumi.set(__self__, "source_arn", source_arn)
        pulumi.set(__self__, "target_arn", target_arn)
        if additional_encryption_context is not None:
            pulumi.set(__self__, "additional_encryption_context", additional_encryption_context)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="integrationName")
    def integration_name(self) -> pulumi.Input[str]:
        """
        Name of the integration.
        """
        return pulumi.get(self, "integration_name")

    @integration_name.setter
    def integration_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "integration_name", value)

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> pulumi.Input[str]:
        """
        ARN of the database to use as the source for replication.
        """
        return pulumi.get(self, "source_arn")

    @source_arn.setter
    def source_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_arn", value)

    @property
    @pulumi.getter(name="targetArn")
    def target_arn(self) -> pulumi.Input[str]:
        """
        ARN of the Redshift data warehouse to use as the target for replication.

        The following arguments are optional:
        """
        return pulumi.get(self, "target_arn")

    @target_arn.setter
    def target_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_arn", value)

    @property
    @pulumi.getter(name="additionalEncryptionContext")
    def additional_encryption_context(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see the [User Guide](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context). You can only include this parameter if you specify the `kms_key_id` parameter.
        """
        return pulumi.get(self, "additional_encryption_context")

    @additional_encryption_context.setter
    def additional_encryption_context(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "additional_encryption_context", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        KMS key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key. If you use the default AWS owned key, you should ignore `kms_key_id` parameter by using `lifecycle` parameter to avoid unintended change after the first creation.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['IntegrationTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['IntegrationTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


@pulumi.input_type
class _IntegrationState:
    def __init__(__self__, *,
                 additional_encryption_context: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 integration_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_arn: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input['IntegrationTimeoutsArgs']] = None):
        """
        Input properties used for looking up and filtering Integration resources.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] additional_encryption_context: Set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see the [User Guide](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context). You can only include this parameter if you specify the `kms_key_id` parameter.
        :param pulumi.Input[str] arn: ARN of the Integration.
        :param pulumi.Input[str] integration_name: Name of the integration.
        :param pulumi.Input[str] kms_key_id: KMS key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key. If you use the default AWS owned key, you should ignore `kms_key_id` parameter by using `lifecycle` parameter to avoid unintended change after the first creation.
        :param pulumi.Input[str] source_arn: ARN of the database to use as the source for replication.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] target_arn: ARN of the Redshift data warehouse to use as the target for replication.
               
               The following arguments are optional:
        """
        if additional_encryption_context is not None:
            pulumi.set(__self__, "additional_encryption_context", additional_encryption_context)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if integration_name is not None:
            pulumi.set(__self__, "integration_name", integration_name)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if source_arn is not None:
            pulumi.set(__self__, "source_arn", source_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if target_arn is not None:
            pulumi.set(__self__, "target_arn", target_arn)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="additionalEncryptionContext")
    def additional_encryption_context(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see the [User Guide](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context). You can only include this parameter if you specify the `kms_key_id` parameter.
        """
        return pulumi.get(self, "additional_encryption_context")

    @additional_encryption_context.setter
    def additional_encryption_context(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "additional_encryption_context", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Integration.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="integrationName")
    def integration_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the integration.
        """
        return pulumi.get(self, "integration_name")

    @integration_name.setter
    def integration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_name", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        KMS key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key. If you use the default AWS owned key, you should ignore `kms_key_id` parameter by using `lifecycle` parameter to avoid unintended change after the first creation.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the database to use as the source for replication.
        """
        return pulumi.get(self, "source_arn")

    @source_arn.setter
    def source_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    @_utilities.deprecated("""Please use `tags` instead.""")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="targetArn")
    def target_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Redshift data warehouse to use as the target for replication.

        The following arguments are optional:
        """
        return pulumi.get(self, "target_arn")

    @target_arn.setter
    def target_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_arn", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['IntegrationTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['IntegrationTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


class Integration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_encryption_context: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 integration_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_arn: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[Union['IntegrationTimeoutsArgs', 'IntegrationTimeoutsArgsDict']]] = None,
                 __props__=None):
        """
        Resource for managing an AWS RDS (Relational Database) zero-ETL integration. You can refer to the [User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/zero-etl.setting-up.html).

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.redshiftserverless.Namespace("example", namespace_name="redshift-example")
        example_workgroup = aws.redshiftserverless.Workgroup("example",
            namespace_name=example.namespace_name,
            workgroup_name="example-workspace",
            base_capacity=8,
            publicly_accessible=False,
            subnet_ids=[
                example1["id"],
                example2["id"],
                example3["id"],
            ],
            config_parameters=[{
                "parameter_key": "enable_case_sensitive_identifier",
                "parameter_value": "true",
            }])
        example_integration = aws.rds.Integration("example",
            integration_name="example",
            source_arn=example_aws_rds_cluster["arn"],
            target_arn=example.arn)
        ```

        ### Use own KMS key

        ```python
        import pulumi
        import pulumi_aws as aws

        current = aws.get_caller_identity()
        key_policy = aws.iam.get_policy_document(statements=[
            {
                "actions": ["kms:*"],
                "resources": ["*"],
                "principals": [{
                    "type": "AWS",
                    "identifiers": [f"arn:aws:iam::{current.account_id}:root"],
                }],
            },
            {
                "actions": ["kms:CreateGrant"],
                "resources": ["*"],
                "principals": [{
                    "type": "Service",
                    "identifiers": ["redshift.amazonaws.com"],
                }],
            },
        ])
        example = aws.kms.Key("example",
            deletion_window_in_days=10,
            policy=key_policy.json)
        example_integration = aws.rds.Integration("example",
            integration_name="example",
            source_arn=example_aws_rds_cluster["arn"],
            target_arn=example_aws_redshiftserverless_namespace["arn"],
            kms_key_id=example.arn,
            additional_encryption_context={
                "example": "test",
            })
        ```

        ## Import

        Using `pulumi import`, import RDS (Relational Database) Integration using the `arn`. For example:

        ```sh
        $ pulumi import aws:rds/integration:Integration example arn:aws:rds:us-west-2:123456789012:integration:abcdefgh-0000-1111-2222-123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] additional_encryption_context: Set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see the [User Guide](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context). You can only include this parameter if you specify the `kms_key_id` parameter.
        :param pulumi.Input[str] integration_name: Name of the integration.
        :param pulumi.Input[str] kms_key_id: KMS key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key. If you use the default AWS owned key, you should ignore `kms_key_id` parameter by using `lifecycle` parameter to avoid unintended change after the first creation.
        :param pulumi.Input[str] source_arn: ARN of the database to use as the source for replication.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] target_arn: ARN of the Redshift data warehouse to use as the target for replication.
               
               The following arguments are optional:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IntegrationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS RDS (Relational Database) zero-ETL integration. You can refer to the [User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/zero-etl.setting-up.html).

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.redshiftserverless.Namespace("example", namespace_name="redshift-example")
        example_workgroup = aws.redshiftserverless.Workgroup("example",
            namespace_name=example.namespace_name,
            workgroup_name="example-workspace",
            base_capacity=8,
            publicly_accessible=False,
            subnet_ids=[
                example1["id"],
                example2["id"],
                example3["id"],
            ],
            config_parameters=[{
                "parameter_key": "enable_case_sensitive_identifier",
                "parameter_value": "true",
            }])
        example_integration = aws.rds.Integration("example",
            integration_name="example",
            source_arn=example_aws_rds_cluster["arn"],
            target_arn=example.arn)
        ```

        ### Use own KMS key

        ```python
        import pulumi
        import pulumi_aws as aws

        current = aws.get_caller_identity()
        key_policy = aws.iam.get_policy_document(statements=[
            {
                "actions": ["kms:*"],
                "resources": ["*"],
                "principals": [{
                    "type": "AWS",
                    "identifiers": [f"arn:aws:iam::{current.account_id}:root"],
                }],
            },
            {
                "actions": ["kms:CreateGrant"],
                "resources": ["*"],
                "principals": [{
                    "type": "Service",
                    "identifiers": ["redshift.amazonaws.com"],
                }],
            },
        ])
        example = aws.kms.Key("example",
            deletion_window_in_days=10,
            policy=key_policy.json)
        example_integration = aws.rds.Integration("example",
            integration_name="example",
            source_arn=example_aws_rds_cluster["arn"],
            target_arn=example_aws_redshiftserverless_namespace["arn"],
            kms_key_id=example.arn,
            additional_encryption_context={
                "example": "test",
            })
        ```

        ## Import

        Using `pulumi import`, import RDS (Relational Database) Integration using the `arn`. For example:

        ```sh
        $ pulumi import aws:rds/integration:Integration example arn:aws:rds:us-west-2:123456789012:integration:abcdefgh-0000-1111-2222-123456789012
        ```

        :param str resource_name: The name of the resource.
        :param IntegrationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IntegrationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_encryption_context: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 integration_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_arn: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[Union['IntegrationTimeoutsArgs', 'IntegrationTimeoutsArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IntegrationArgs.__new__(IntegrationArgs)

            __props__.__dict__["additional_encryption_context"] = additional_encryption_context
            if integration_name is None and not opts.urn:
                raise TypeError("Missing required property 'integration_name'")
            __props__.__dict__["integration_name"] = integration_name
            __props__.__dict__["kms_key_id"] = kms_key_id
            if source_arn is None and not opts.urn:
                raise TypeError("Missing required property 'source_arn'")
            __props__.__dict__["source_arn"] = source_arn
            __props__.__dict__["tags"] = tags
            if target_arn is None and not opts.urn:
                raise TypeError("Missing required property 'target_arn'")
            __props__.__dict__["target_arn"] = target_arn
            __props__.__dict__["timeouts"] = timeouts
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(Integration, __self__).__init__(
            'aws:rds/integration:Integration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            additional_encryption_context: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            integration_name: Optional[pulumi.Input[str]] = None,
            kms_key_id: Optional[pulumi.Input[str]] = None,
            source_arn: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            target_arn: Optional[pulumi.Input[str]] = None,
            timeouts: Optional[pulumi.Input[Union['IntegrationTimeoutsArgs', 'IntegrationTimeoutsArgsDict']]] = None) -> 'Integration':
        """
        Get an existing Integration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] additional_encryption_context: Set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see the [User Guide](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context). You can only include this parameter if you specify the `kms_key_id` parameter.
        :param pulumi.Input[str] arn: ARN of the Integration.
        :param pulumi.Input[str] integration_name: Name of the integration.
        :param pulumi.Input[str] kms_key_id: KMS key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key. If you use the default AWS owned key, you should ignore `kms_key_id` parameter by using `lifecycle` parameter to avoid unintended change after the first creation.
        :param pulumi.Input[str] source_arn: ARN of the database to use as the source for replication.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] target_arn: ARN of the Redshift data warehouse to use as the target for replication.
               
               The following arguments are optional:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IntegrationState.__new__(_IntegrationState)

        __props__.__dict__["additional_encryption_context"] = additional_encryption_context
        __props__.__dict__["arn"] = arn
        __props__.__dict__["integration_name"] = integration_name
        __props__.__dict__["kms_key_id"] = kms_key_id
        __props__.__dict__["source_arn"] = source_arn
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["target_arn"] = target_arn
        __props__.__dict__["timeouts"] = timeouts
        return Integration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="additionalEncryptionContext")
    def additional_encryption_context(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see the [User Guide](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context). You can only include this parameter if you specify the `kms_key_id` parameter.
        """
        return pulumi.get(self, "additional_encryption_context")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Integration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="integrationName")
    def integration_name(self) -> pulumi.Output[str]:
        """
        Name of the integration.
        """
        return pulumi.get(self, "integration_name")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[str]:
        """
        KMS key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key. If you use the default AWS owned key, you should ignore `kms_key_id` parameter by using `lifecycle` parameter to avoid unintended change after the first creation.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> pulumi.Output[str]:
        """
        ARN of the database to use as the source for replication.
        """
        return pulumi.get(self, "source_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    @_utilities.deprecated("""Please use `tags` instead.""")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="targetArn")
    def target_arn(self) -> pulumi.Output[str]:
        """
        ARN of the Redshift data warehouse to use as the target for replication.

        The following arguments are optional:
        """
        return pulumi.get(self, "target_arn")

    @property
    @pulumi.getter
    def timeouts(self) -> pulumi.Output[Optional['outputs.IntegrationTimeouts']]:
        return pulumi.get(self, "timeouts")

