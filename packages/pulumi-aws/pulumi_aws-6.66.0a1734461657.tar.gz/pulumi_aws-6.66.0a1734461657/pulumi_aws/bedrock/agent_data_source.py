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

__all__ = ['AgentDataSourceArgs', 'AgentDataSource']

@pulumi.input_type
class AgentDataSourceArgs:
    def __init__(__self__, *,
                 knowledge_base_id: pulumi.Input[str],
                 data_deletion_policy: Optional[pulumi.Input[str]] = None,
                 data_source_configuration: Optional[pulumi.Input['AgentDataSourceDataSourceConfigurationArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_side_encryption_configuration: Optional[pulumi.Input['AgentDataSourceServerSideEncryptionConfigurationArgs']] = None,
                 timeouts: Optional[pulumi.Input['AgentDataSourceTimeoutsArgs']] = None,
                 vector_ingestion_configuration: Optional[pulumi.Input['AgentDataSourceVectorIngestionConfigurationArgs']] = None):
        """
        The set of arguments for constructing a AgentDataSource resource.
        :param pulumi.Input[str] knowledge_base_id: Unique identifier of the knowledge base to which the data source belongs.
        :param pulumi.Input[str] data_deletion_policy: Data deletion policy for a data source. Valid values: `RETAIN`, `DELETE`.
        :param pulumi.Input['AgentDataSourceDataSourceConfigurationArgs'] data_source_configuration: Details about how the data source is stored. See `data_source_configuration` block for details.
        :param pulumi.Input[str] description: Description of the data source.
        :param pulumi.Input[str] name: Name of the data source.
               
               The following arguments are optional:
        :param pulumi.Input['AgentDataSourceServerSideEncryptionConfigurationArgs'] server_side_encryption_configuration: Details about the configuration of the server-side encryption. See `server_side_encryption_configuration` block for details.
        :param pulumi.Input['AgentDataSourceVectorIngestionConfigurationArgs'] vector_ingestion_configuration: Details about the configuration of the server-side encryption. See `vector_ingestion_configuration` block for details.
        """
        pulumi.set(__self__, "knowledge_base_id", knowledge_base_id)
        if data_deletion_policy is not None:
            pulumi.set(__self__, "data_deletion_policy", data_deletion_policy)
        if data_source_configuration is not None:
            pulumi.set(__self__, "data_source_configuration", data_source_configuration)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if server_side_encryption_configuration is not None:
            pulumi.set(__self__, "server_side_encryption_configuration", server_side_encryption_configuration)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)
        if vector_ingestion_configuration is not None:
            pulumi.set(__self__, "vector_ingestion_configuration", vector_ingestion_configuration)

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> pulumi.Input[str]:
        """
        Unique identifier of the knowledge base to which the data source belongs.
        """
        return pulumi.get(self, "knowledge_base_id")

    @knowledge_base_id.setter
    def knowledge_base_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "knowledge_base_id", value)

    @property
    @pulumi.getter(name="dataDeletionPolicy")
    def data_deletion_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Data deletion policy for a data source. Valid values: `RETAIN`, `DELETE`.
        """
        return pulumi.get(self, "data_deletion_policy")

    @data_deletion_policy.setter
    def data_deletion_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_deletion_policy", value)

    @property
    @pulumi.getter(name="dataSourceConfiguration")
    def data_source_configuration(self) -> Optional[pulumi.Input['AgentDataSourceDataSourceConfigurationArgs']]:
        """
        Details about how the data source is stored. See `data_source_configuration` block for details.
        """
        return pulumi.get(self, "data_source_configuration")

    @data_source_configuration.setter
    def data_source_configuration(self, value: Optional[pulumi.Input['AgentDataSourceDataSourceConfigurationArgs']]):
        pulumi.set(self, "data_source_configuration", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the data source.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the data source.

        The following arguments are optional:
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(self) -> Optional[pulumi.Input['AgentDataSourceServerSideEncryptionConfigurationArgs']]:
        """
        Details about the configuration of the server-side encryption. See `server_side_encryption_configuration` block for details.
        """
        return pulumi.get(self, "server_side_encryption_configuration")

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(self, value: Optional[pulumi.Input['AgentDataSourceServerSideEncryptionConfigurationArgs']]):
        pulumi.set(self, "server_side_encryption_configuration", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['AgentDataSourceTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['AgentDataSourceTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)

    @property
    @pulumi.getter(name="vectorIngestionConfiguration")
    def vector_ingestion_configuration(self) -> Optional[pulumi.Input['AgentDataSourceVectorIngestionConfigurationArgs']]:
        """
        Details about the configuration of the server-side encryption. See `vector_ingestion_configuration` block for details.
        """
        return pulumi.get(self, "vector_ingestion_configuration")

    @vector_ingestion_configuration.setter
    def vector_ingestion_configuration(self, value: Optional[pulumi.Input['AgentDataSourceVectorIngestionConfigurationArgs']]):
        pulumi.set(self, "vector_ingestion_configuration", value)


@pulumi.input_type
class _AgentDataSourceState:
    def __init__(__self__, *,
                 data_deletion_policy: Optional[pulumi.Input[str]] = None,
                 data_source_configuration: Optional[pulumi.Input['AgentDataSourceDataSourceConfigurationArgs']] = None,
                 data_source_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 knowledge_base_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_side_encryption_configuration: Optional[pulumi.Input['AgentDataSourceServerSideEncryptionConfigurationArgs']] = None,
                 timeouts: Optional[pulumi.Input['AgentDataSourceTimeoutsArgs']] = None,
                 vector_ingestion_configuration: Optional[pulumi.Input['AgentDataSourceVectorIngestionConfigurationArgs']] = None):
        """
        Input properties used for looking up and filtering AgentDataSource resources.
        :param pulumi.Input[str] data_deletion_policy: Data deletion policy for a data source. Valid values: `RETAIN`, `DELETE`.
        :param pulumi.Input['AgentDataSourceDataSourceConfigurationArgs'] data_source_configuration: Details about how the data source is stored. See `data_source_configuration` block for details.
        :param pulumi.Input[str] data_source_id: Unique identifier of the data source.
        :param pulumi.Input[str] description: Description of the data source.
        :param pulumi.Input[str] knowledge_base_id: Unique identifier of the knowledge base to which the data source belongs.
        :param pulumi.Input[str] name: Name of the data source.
               
               The following arguments are optional:
        :param pulumi.Input['AgentDataSourceServerSideEncryptionConfigurationArgs'] server_side_encryption_configuration: Details about the configuration of the server-side encryption. See `server_side_encryption_configuration` block for details.
        :param pulumi.Input['AgentDataSourceVectorIngestionConfigurationArgs'] vector_ingestion_configuration: Details about the configuration of the server-side encryption. See `vector_ingestion_configuration` block for details.
        """
        if data_deletion_policy is not None:
            pulumi.set(__self__, "data_deletion_policy", data_deletion_policy)
        if data_source_configuration is not None:
            pulumi.set(__self__, "data_source_configuration", data_source_configuration)
        if data_source_id is not None:
            pulumi.set(__self__, "data_source_id", data_source_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if knowledge_base_id is not None:
            pulumi.set(__self__, "knowledge_base_id", knowledge_base_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if server_side_encryption_configuration is not None:
            pulumi.set(__self__, "server_side_encryption_configuration", server_side_encryption_configuration)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)
        if vector_ingestion_configuration is not None:
            pulumi.set(__self__, "vector_ingestion_configuration", vector_ingestion_configuration)

    @property
    @pulumi.getter(name="dataDeletionPolicy")
    def data_deletion_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Data deletion policy for a data source. Valid values: `RETAIN`, `DELETE`.
        """
        return pulumi.get(self, "data_deletion_policy")

    @data_deletion_policy.setter
    def data_deletion_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_deletion_policy", value)

    @property
    @pulumi.getter(name="dataSourceConfiguration")
    def data_source_configuration(self) -> Optional[pulumi.Input['AgentDataSourceDataSourceConfigurationArgs']]:
        """
        Details about how the data source is stored. See `data_source_configuration` block for details.
        """
        return pulumi.get(self, "data_source_configuration")

    @data_source_configuration.setter
    def data_source_configuration(self, value: Optional[pulumi.Input['AgentDataSourceDataSourceConfigurationArgs']]):
        pulumi.set(self, "data_source_configuration", value)

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the data source.
        """
        return pulumi.get(self, "data_source_id")

    @data_source_id.setter
    def data_source_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_source_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the data source.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the knowledge base to which the data source belongs.
        """
        return pulumi.get(self, "knowledge_base_id")

    @knowledge_base_id.setter
    def knowledge_base_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "knowledge_base_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the data source.

        The following arguments are optional:
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(self) -> Optional[pulumi.Input['AgentDataSourceServerSideEncryptionConfigurationArgs']]:
        """
        Details about the configuration of the server-side encryption. See `server_side_encryption_configuration` block for details.
        """
        return pulumi.get(self, "server_side_encryption_configuration")

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(self, value: Optional[pulumi.Input['AgentDataSourceServerSideEncryptionConfigurationArgs']]):
        pulumi.set(self, "server_side_encryption_configuration", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['AgentDataSourceTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['AgentDataSourceTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)

    @property
    @pulumi.getter(name="vectorIngestionConfiguration")
    def vector_ingestion_configuration(self) -> Optional[pulumi.Input['AgentDataSourceVectorIngestionConfigurationArgs']]:
        """
        Details about the configuration of the server-side encryption. See `vector_ingestion_configuration` block for details.
        """
        return pulumi.get(self, "vector_ingestion_configuration")

    @vector_ingestion_configuration.setter
    def vector_ingestion_configuration(self, value: Optional[pulumi.Input['AgentDataSourceVectorIngestionConfigurationArgs']]):
        pulumi.set(self, "vector_ingestion_configuration", value)


class AgentDataSource(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_deletion_policy: Optional[pulumi.Input[str]] = None,
                 data_source_configuration: Optional[pulumi.Input[Union['AgentDataSourceDataSourceConfigurationArgs', 'AgentDataSourceDataSourceConfigurationArgsDict']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 knowledge_base_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_side_encryption_configuration: Optional[pulumi.Input[Union['AgentDataSourceServerSideEncryptionConfigurationArgs', 'AgentDataSourceServerSideEncryptionConfigurationArgsDict']]] = None,
                 timeouts: Optional[pulumi.Input[Union['AgentDataSourceTimeoutsArgs', 'AgentDataSourceTimeoutsArgsDict']]] = None,
                 vector_ingestion_configuration: Optional[pulumi.Input[Union['AgentDataSourceVectorIngestionConfigurationArgs', 'AgentDataSourceVectorIngestionConfigurationArgsDict']]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Agents for Amazon Bedrock Data Source.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.bedrock.AgentDataSource("example",
            knowledge_base_id="EMDPPAYPZI",
            name="example",
            data_source_configuration={
                "type": "S3",
                "s3_configuration": {
                    "bucket_arn": "arn:aws:s3:::example-bucket",
                },
            })
        ```

        ## Import

        Using `pulumi import`, import Agents for Amazon Bedrock Data Source using the data source ID and the knowledge base ID. For example:

        ```sh
        $ pulumi import aws:bedrock/agentDataSource:AgentDataSource example GWCMFMQF6T,EMDPPAYPZI
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_deletion_policy: Data deletion policy for a data source. Valid values: `RETAIN`, `DELETE`.
        :param pulumi.Input[Union['AgentDataSourceDataSourceConfigurationArgs', 'AgentDataSourceDataSourceConfigurationArgsDict']] data_source_configuration: Details about how the data source is stored. See `data_source_configuration` block for details.
        :param pulumi.Input[str] description: Description of the data source.
        :param pulumi.Input[str] knowledge_base_id: Unique identifier of the knowledge base to which the data source belongs.
        :param pulumi.Input[str] name: Name of the data source.
               
               The following arguments are optional:
        :param pulumi.Input[Union['AgentDataSourceServerSideEncryptionConfigurationArgs', 'AgentDataSourceServerSideEncryptionConfigurationArgsDict']] server_side_encryption_configuration: Details about the configuration of the server-side encryption. See `server_side_encryption_configuration` block for details.
        :param pulumi.Input[Union['AgentDataSourceVectorIngestionConfigurationArgs', 'AgentDataSourceVectorIngestionConfigurationArgsDict']] vector_ingestion_configuration: Details about the configuration of the server-side encryption. See `vector_ingestion_configuration` block for details.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AgentDataSourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Agents for Amazon Bedrock Data Source.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.bedrock.AgentDataSource("example",
            knowledge_base_id="EMDPPAYPZI",
            name="example",
            data_source_configuration={
                "type": "S3",
                "s3_configuration": {
                    "bucket_arn": "arn:aws:s3:::example-bucket",
                },
            })
        ```

        ## Import

        Using `pulumi import`, import Agents for Amazon Bedrock Data Source using the data source ID and the knowledge base ID. For example:

        ```sh
        $ pulumi import aws:bedrock/agentDataSource:AgentDataSource example GWCMFMQF6T,EMDPPAYPZI
        ```

        :param str resource_name: The name of the resource.
        :param AgentDataSourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AgentDataSourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_deletion_policy: Optional[pulumi.Input[str]] = None,
                 data_source_configuration: Optional[pulumi.Input[Union['AgentDataSourceDataSourceConfigurationArgs', 'AgentDataSourceDataSourceConfigurationArgsDict']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 knowledge_base_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_side_encryption_configuration: Optional[pulumi.Input[Union['AgentDataSourceServerSideEncryptionConfigurationArgs', 'AgentDataSourceServerSideEncryptionConfigurationArgsDict']]] = None,
                 timeouts: Optional[pulumi.Input[Union['AgentDataSourceTimeoutsArgs', 'AgentDataSourceTimeoutsArgsDict']]] = None,
                 vector_ingestion_configuration: Optional[pulumi.Input[Union['AgentDataSourceVectorIngestionConfigurationArgs', 'AgentDataSourceVectorIngestionConfigurationArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AgentDataSourceArgs.__new__(AgentDataSourceArgs)

            __props__.__dict__["data_deletion_policy"] = data_deletion_policy
            __props__.__dict__["data_source_configuration"] = data_source_configuration
            __props__.__dict__["description"] = description
            if knowledge_base_id is None and not opts.urn:
                raise TypeError("Missing required property 'knowledge_base_id'")
            __props__.__dict__["knowledge_base_id"] = knowledge_base_id
            __props__.__dict__["name"] = name
            __props__.__dict__["server_side_encryption_configuration"] = server_side_encryption_configuration
            __props__.__dict__["timeouts"] = timeouts
            __props__.__dict__["vector_ingestion_configuration"] = vector_ingestion_configuration
            __props__.__dict__["data_source_id"] = None
        super(AgentDataSource, __self__).__init__(
            'aws:bedrock/agentDataSource:AgentDataSource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            data_deletion_policy: Optional[pulumi.Input[str]] = None,
            data_source_configuration: Optional[pulumi.Input[Union['AgentDataSourceDataSourceConfigurationArgs', 'AgentDataSourceDataSourceConfigurationArgsDict']]] = None,
            data_source_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            knowledge_base_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            server_side_encryption_configuration: Optional[pulumi.Input[Union['AgentDataSourceServerSideEncryptionConfigurationArgs', 'AgentDataSourceServerSideEncryptionConfigurationArgsDict']]] = None,
            timeouts: Optional[pulumi.Input[Union['AgentDataSourceTimeoutsArgs', 'AgentDataSourceTimeoutsArgsDict']]] = None,
            vector_ingestion_configuration: Optional[pulumi.Input[Union['AgentDataSourceVectorIngestionConfigurationArgs', 'AgentDataSourceVectorIngestionConfigurationArgsDict']]] = None) -> 'AgentDataSource':
        """
        Get an existing AgentDataSource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_deletion_policy: Data deletion policy for a data source. Valid values: `RETAIN`, `DELETE`.
        :param pulumi.Input[Union['AgentDataSourceDataSourceConfigurationArgs', 'AgentDataSourceDataSourceConfigurationArgsDict']] data_source_configuration: Details about how the data source is stored. See `data_source_configuration` block for details.
        :param pulumi.Input[str] data_source_id: Unique identifier of the data source.
        :param pulumi.Input[str] description: Description of the data source.
        :param pulumi.Input[str] knowledge_base_id: Unique identifier of the knowledge base to which the data source belongs.
        :param pulumi.Input[str] name: Name of the data source.
               
               The following arguments are optional:
        :param pulumi.Input[Union['AgentDataSourceServerSideEncryptionConfigurationArgs', 'AgentDataSourceServerSideEncryptionConfigurationArgsDict']] server_side_encryption_configuration: Details about the configuration of the server-side encryption. See `server_side_encryption_configuration` block for details.
        :param pulumi.Input[Union['AgentDataSourceVectorIngestionConfigurationArgs', 'AgentDataSourceVectorIngestionConfigurationArgsDict']] vector_ingestion_configuration: Details about the configuration of the server-side encryption. See `vector_ingestion_configuration` block for details.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AgentDataSourceState.__new__(_AgentDataSourceState)

        __props__.__dict__["data_deletion_policy"] = data_deletion_policy
        __props__.__dict__["data_source_configuration"] = data_source_configuration
        __props__.__dict__["data_source_id"] = data_source_id
        __props__.__dict__["description"] = description
        __props__.__dict__["knowledge_base_id"] = knowledge_base_id
        __props__.__dict__["name"] = name
        __props__.__dict__["server_side_encryption_configuration"] = server_side_encryption_configuration
        __props__.__dict__["timeouts"] = timeouts
        __props__.__dict__["vector_ingestion_configuration"] = vector_ingestion_configuration
        return AgentDataSource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataDeletionPolicy")
    def data_deletion_policy(self) -> pulumi.Output[str]:
        """
        Data deletion policy for a data source. Valid values: `RETAIN`, `DELETE`.
        """
        return pulumi.get(self, "data_deletion_policy")

    @property
    @pulumi.getter(name="dataSourceConfiguration")
    def data_source_configuration(self) -> pulumi.Output[Optional['outputs.AgentDataSourceDataSourceConfiguration']]:
        """
        Details about how the data source is stored. See `data_source_configuration` block for details.
        """
        return pulumi.get(self, "data_source_configuration")

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> pulumi.Output[str]:
        """
        Unique identifier of the data source.
        """
        return pulumi.get(self, "data_source_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the data source.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="knowledgeBaseId")
    def knowledge_base_id(self) -> pulumi.Output[str]:
        """
        Unique identifier of the knowledge base to which the data source belongs.
        """
        return pulumi.get(self, "knowledge_base_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the data source.

        The following arguments are optional:
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(self) -> pulumi.Output[Optional['outputs.AgentDataSourceServerSideEncryptionConfiguration']]:
        """
        Details about the configuration of the server-side encryption. See `server_side_encryption_configuration` block for details.
        """
        return pulumi.get(self, "server_side_encryption_configuration")

    @property
    @pulumi.getter
    def timeouts(self) -> pulumi.Output[Optional['outputs.AgentDataSourceTimeouts']]:
        return pulumi.get(self, "timeouts")

    @property
    @pulumi.getter(name="vectorIngestionConfiguration")
    def vector_ingestion_configuration(self) -> pulumi.Output[Optional['outputs.AgentDataSourceVectorIngestionConfiguration']]:
        """
        Details about the configuration of the server-side encryption. See `vector_ingestion_configuration` block for details.
        """
        return pulumi.get(self, "vector_ingestion_configuration")

