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

__all__ = [
    'GetTrafficPolicyDocumentResult',
    'AwaitableGetTrafficPolicyDocumentResult',
    'get_traffic_policy_document',
    'get_traffic_policy_document_output',
]

@pulumi.output_type
class GetTrafficPolicyDocumentResult:
    """
    A collection of values returned by getTrafficPolicyDocument.
    """
    def __init__(__self__, endpoints=None, id=None, json=None, record_type=None, rules=None, start_endpoint=None, start_rule=None, version=None):
        if endpoints and not isinstance(endpoints, list):
            raise TypeError("Expected argument 'endpoints' to be a list")
        pulumi.set(__self__, "endpoints", endpoints)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if json and not isinstance(json, str):
            raise TypeError("Expected argument 'json' to be a str")
        pulumi.set(__self__, "json", json)
        if record_type and not isinstance(record_type, str):
            raise TypeError("Expected argument 'record_type' to be a str")
        pulumi.set(__self__, "record_type", record_type)
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, "rules", rules)
        if start_endpoint and not isinstance(start_endpoint, str):
            raise TypeError("Expected argument 'start_endpoint' to be a str")
        pulumi.set(__self__, "start_endpoint", start_endpoint)
        if start_rule and not isinstance(start_rule, str):
            raise TypeError("Expected argument 'start_rule' to be a str")
        pulumi.set(__self__, "start_rule", start_rule)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def endpoints(self) -> Optional[Sequence['outputs.GetTrafficPolicyDocumentEndpointResult']]:
        return pulumi.get(self, "endpoints")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def json(self) -> str:
        """
        Standard JSON policy document rendered based on the arguments above.
        """
        return pulumi.get(self, "json")

    @property
    @pulumi.getter(name="recordType")
    def record_type(self) -> Optional[str]:
        return pulumi.get(self, "record_type")

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.GetTrafficPolicyDocumentRuleResult']]:
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="startEndpoint")
    def start_endpoint(self) -> Optional[str]:
        return pulumi.get(self, "start_endpoint")

    @property
    @pulumi.getter(name="startRule")
    def start_rule(self) -> Optional[str]:
        return pulumi.get(self, "start_rule")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        return pulumi.get(self, "version")


class AwaitableGetTrafficPolicyDocumentResult(GetTrafficPolicyDocumentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTrafficPolicyDocumentResult(
            endpoints=self.endpoints,
            id=self.id,
            json=self.json,
            record_type=self.record_type,
            rules=self.rules,
            start_endpoint=self.start_endpoint,
            start_rule=self.start_rule,
            version=self.version)


def get_traffic_policy_document(endpoints: Optional[Sequence[Union['GetTrafficPolicyDocumentEndpointArgs', 'GetTrafficPolicyDocumentEndpointArgsDict']]] = None,
                                record_type: Optional[str] = None,
                                rules: Optional[Sequence[Union['GetTrafficPolicyDocumentRuleArgs', 'GetTrafficPolicyDocumentRuleArgsDict']]] = None,
                                start_endpoint: Optional[str] = None,
                                start_rule: Optional[str] = None,
                                version: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTrafficPolicyDocumentResult:
    """
    Generates an Route53 traffic policy document in JSON format for use with resources that expect policy documents such as `route53.TrafficPolicy`.

    ## Example Usage

    ### Basic Example

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.get_region()
    example = aws.route53.get_traffic_policy_document(record_type="A",
        start_rule="site_switch",
        endpoints=[
            {
                "id": "my_elb",
                "type": "elastic-load-balancer",
                "value": f"elb-111111.{current.name}.elb.amazonaws.com",
            },
            {
                "id": "site_down_banner",
                "type": "s3-website",
                "region": current.name,
                "value": "www.example.com",
            },
        ],
        rules=[{
            "id": "site_switch",
            "type": "failover",
            "primary": {
                "endpoint_reference": "my_elb",
            },
            "secondary": {
                "endpoint_reference": "site_down_banner",
            },
        }])
    example_traffic_policy = aws.route53.TrafficPolicy("example",
        name="example",
        comment="example comment",
        document=example.json)
    ```

    ### Complex Example

    The following example showcases the use of nested rules within the traffic policy document and introduces the `geoproximity` rule type.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.route53.get_traffic_policy_document(record_type="A",
        start_rule="geoproximity_rule",
        endpoints=[
            {
                "id": "na_endpoint_a",
                "type": "elastic-load-balancer",
                "value": "elb-111111.us-west-1.elb.amazonaws.com",
            },
            {
                "id": "na_endpoint_b",
                "type": "elastic-load-balancer",
                "value": "elb-222222.us-west-1.elb.amazonaws.com",
            },
            {
                "id": "eu_endpoint",
                "type": "elastic-load-balancer",
                "value": "elb-333333.eu-west-1.elb.amazonaws.com",
            },
            {
                "id": "ap_endpoint",
                "type": "elastic-load-balancer",
                "value": "elb-444444.ap-northeast-2.elb.amazonaws.com",
            },
        ],
        rules=[
            {
                "id": "na_rule",
                "type": "failover",
                "primary": {
                    "endpoint_reference": "na_endpoint_a",
                },
                "secondary": {
                    "endpoint_reference": "na_endpoint_b",
                },
            },
            {
                "id": "geoproximity_rule",
                "type": "geoproximity",
                "geo_proximity_locations": [
                    {
                        "region": "aws:route53:us-west-1",
                        "bias": "10",
                        "evaluate_target_health": True,
                        "rule_reference": "na_rule",
                    },
                    {
                        "region": "aws:route53:eu-west-1",
                        "bias": "10",
                        "evaluate_target_health": True,
                        "endpoint_reference": "eu_endpoint",
                    },
                    {
                        "region": "aws:route53:ap-northeast-2",
                        "bias": "0",
                        "evaluate_target_health": True,
                        "endpoint_reference": "ap_endpoint",
                    },
                ],
            },
        ])
    example_traffic_policy = aws.route53.TrafficPolicy("example",
        name="example",
        comment="example comment",
        document=example.json)
    ```


    :param Sequence[Union['GetTrafficPolicyDocumentEndpointArgs', 'GetTrafficPolicyDocumentEndpointArgsDict']] endpoints: Configuration block for the definitions of the endpoints that you want to use in this traffic policy. See below
    :param str record_type: DNS type of all of the resource record sets that Amazon Route 53 will create based on this traffic policy.
    :param Sequence[Union['GetTrafficPolicyDocumentRuleArgs', 'GetTrafficPolicyDocumentRuleArgsDict']] rules: Configuration block for definitions of the rules that you want to use in this traffic policy. See below
    :param str start_endpoint: An endpoint to be as the starting point for the traffic policy.
    :param str start_rule: A rule to be as the starting point for the traffic policy.
    :param str version: Version of the traffic policy format.
    """
    __args__ = dict()
    __args__['endpoints'] = endpoints
    __args__['recordType'] = record_type
    __args__['rules'] = rules
    __args__['startEndpoint'] = start_endpoint
    __args__['startRule'] = start_rule
    __args__['version'] = version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:route53/getTrafficPolicyDocument:getTrafficPolicyDocument', __args__, opts=opts, typ=GetTrafficPolicyDocumentResult).value

    return AwaitableGetTrafficPolicyDocumentResult(
        endpoints=pulumi.get(__ret__, 'endpoints'),
        id=pulumi.get(__ret__, 'id'),
        json=pulumi.get(__ret__, 'json'),
        record_type=pulumi.get(__ret__, 'record_type'),
        rules=pulumi.get(__ret__, 'rules'),
        start_endpoint=pulumi.get(__ret__, 'start_endpoint'),
        start_rule=pulumi.get(__ret__, 'start_rule'),
        version=pulumi.get(__ret__, 'version'))
def get_traffic_policy_document_output(endpoints: Optional[pulumi.Input[Optional[Sequence[Union['GetTrafficPolicyDocumentEndpointArgs', 'GetTrafficPolicyDocumentEndpointArgsDict']]]]] = None,
                                       record_type: Optional[pulumi.Input[Optional[str]]] = None,
                                       rules: Optional[pulumi.Input[Optional[Sequence[Union['GetTrafficPolicyDocumentRuleArgs', 'GetTrafficPolicyDocumentRuleArgsDict']]]]] = None,
                                       start_endpoint: Optional[pulumi.Input[Optional[str]]] = None,
                                       start_rule: Optional[pulumi.Input[Optional[str]]] = None,
                                       version: Optional[pulumi.Input[Optional[str]]] = None,
                                       opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetTrafficPolicyDocumentResult]:
    """
    Generates an Route53 traffic policy document in JSON format for use with resources that expect policy documents such as `route53.TrafficPolicy`.

    ## Example Usage

    ### Basic Example

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.get_region()
    example = aws.route53.get_traffic_policy_document(record_type="A",
        start_rule="site_switch",
        endpoints=[
            {
                "id": "my_elb",
                "type": "elastic-load-balancer",
                "value": f"elb-111111.{current.name}.elb.amazonaws.com",
            },
            {
                "id": "site_down_banner",
                "type": "s3-website",
                "region": current.name,
                "value": "www.example.com",
            },
        ],
        rules=[{
            "id": "site_switch",
            "type": "failover",
            "primary": {
                "endpoint_reference": "my_elb",
            },
            "secondary": {
                "endpoint_reference": "site_down_banner",
            },
        }])
    example_traffic_policy = aws.route53.TrafficPolicy("example",
        name="example",
        comment="example comment",
        document=example.json)
    ```

    ### Complex Example

    The following example showcases the use of nested rules within the traffic policy document and introduces the `geoproximity` rule type.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.route53.get_traffic_policy_document(record_type="A",
        start_rule="geoproximity_rule",
        endpoints=[
            {
                "id": "na_endpoint_a",
                "type": "elastic-load-balancer",
                "value": "elb-111111.us-west-1.elb.amazonaws.com",
            },
            {
                "id": "na_endpoint_b",
                "type": "elastic-load-balancer",
                "value": "elb-222222.us-west-1.elb.amazonaws.com",
            },
            {
                "id": "eu_endpoint",
                "type": "elastic-load-balancer",
                "value": "elb-333333.eu-west-1.elb.amazonaws.com",
            },
            {
                "id": "ap_endpoint",
                "type": "elastic-load-balancer",
                "value": "elb-444444.ap-northeast-2.elb.amazonaws.com",
            },
        ],
        rules=[
            {
                "id": "na_rule",
                "type": "failover",
                "primary": {
                    "endpoint_reference": "na_endpoint_a",
                },
                "secondary": {
                    "endpoint_reference": "na_endpoint_b",
                },
            },
            {
                "id": "geoproximity_rule",
                "type": "geoproximity",
                "geo_proximity_locations": [
                    {
                        "region": "aws:route53:us-west-1",
                        "bias": "10",
                        "evaluate_target_health": True,
                        "rule_reference": "na_rule",
                    },
                    {
                        "region": "aws:route53:eu-west-1",
                        "bias": "10",
                        "evaluate_target_health": True,
                        "endpoint_reference": "eu_endpoint",
                    },
                    {
                        "region": "aws:route53:ap-northeast-2",
                        "bias": "0",
                        "evaluate_target_health": True,
                        "endpoint_reference": "ap_endpoint",
                    },
                ],
            },
        ])
    example_traffic_policy = aws.route53.TrafficPolicy("example",
        name="example",
        comment="example comment",
        document=example.json)
    ```


    :param Sequence[Union['GetTrafficPolicyDocumentEndpointArgs', 'GetTrafficPolicyDocumentEndpointArgsDict']] endpoints: Configuration block for the definitions of the endpoints that you want to use in this traffic policy. See below
    :param str record_type: DNS type of all of the resource record sets that Amazon Route 53 will create based on this traffic policy.
    :param Sequence[Union['GetTrafficPolicyDocumentRuleArgs', 'GetTrafficPolicyDocumentRuleArgsDict']] rules: Configuration block for definitions of the rules that you want to use in this traffic policy. See below
    :param str start_endpoint: An endpoint to be as the starting point for the traffic policy.
    :param str start_rule: A rule to be as the starting point for the traffic policy.
    :param str version: Version of the traffic policy format.
    """
    __args__ = dict()
    __args__['endpoints'] = endpoints
    __args__['recordType'] = record_type
    __args__['rules'] = rules
    __args__['startEndpoint'] = start_endpoint
    __args__['startRule'] = start_rule
    __args__['version'] = version
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:route53/getTrafficPolicyDocument:getTrafficPolicyDocument', __args__, opts=opts, typ=GetTrafficPolicyDocumentResult)
    return __ret__.apply(lambda __response__: GetTrafficPolicyDocumentResult(
        endpoints=pulumi.get(__response__, 'endpoints'),
        id=pulumi.get(__response__, 'id'),
        json=pulumi.get(__response__, 'json'),
        record_type=pulumi.get(__response__, 'record_type'),
        rules=pulumi.get(__response__, 'rules'),
        start_endpoint=pulumi.get(__response__, 'start_endpoint'),
        start_rule=pulumi.get(__response__, 'start_rule'),
        version=pulumi.get(__response__, 'version')))
