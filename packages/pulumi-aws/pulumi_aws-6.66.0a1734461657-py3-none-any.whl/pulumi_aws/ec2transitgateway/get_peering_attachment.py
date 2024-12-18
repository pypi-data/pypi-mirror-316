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
    'GetPeeringAttachmentResult',
    'AwaitableGetPeeringAttachmentResult',
    'get_peering_attachment',
    'get_peering_attachment_output',
]

@pulumi.output_type
class GetPeeringAttachmentResult:
    """
    A collection of values returned by getPeeringAttachment.
    """
    def __init__(__self__, filters=None, id=None, peer_account_id=None, peer_region=None, peer_transit_gateway_id=None, state=None, tags=None, transit_gateway_id=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if peer_account_id and not isinstance(peer_account_id, str):
            raise TypeError("Expected argument 'peer_account_id' to be a str")
        pulumi.set(__self__, "peer_account_id", peer_account_id)
        if peer_region and not isinstance(peer_region, str):
            raise TypeError("Expected argument 'peer_region' to be a str")
        pulumi.set(__self__, "peer_region", peer_region)
        if peer_transit_gateway_id and not isinstance(peer_transit_gateway_id, str):
            raise TypeError("Expected argument 'peer_transit_gateway_id' to be a str")
        pulumi.set(__self__, "peer_transit_gateway_id", peer_transit_gateway_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if transit_gateway_id and not isinstance(transit_gateway_id, str):
            raise TypeError("Expected argument 'transit_gateway_id' to be a str")
        pulumi.set(__self__, "transit_gateway_id", transit_gateway_id)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetPeeringAttachmentFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="peerAccountId")
    def peer_account_id(self) -> str:
        """
        Identifier of the peer AWS account
        """
        return pulumi.get(self, "peer_account_id")

    @property
    @pulumi.getter(name="peerRegion")
    def peer_region(self) -> str:
        """
        Identifier of the peer AWS region
        """
        return pulumi.get(self, "peer_region")

    @property
    @pulumi.getter(name="peerTransitGatewayId")
    def peer_transit_gateway_id(self) -> str:
        """
        Identifier of the peer EC2 Transit Gateway
        """
        return pulumi.get(self, "peer_transit_gateway_id")

    @property
    @pulumi.getter
    def state(self) -> str:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> str:
        """
        Identifier of the local EC2 Transit Gateway
        """
        return pulumi.get(self, "transit_gateway_id")


class AwaitableGetPeeringAttachmentResult(GetPeeringAttachmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPeeringAttachmentResult(
            filters=self.filters,
            id=self.id,
            peer_account_id=self.peer_account_id,
            peer_region=self.peer_region,
            peer_transit_gateway_id=self.peer_transit_gateway_id,
            state=self.state,
            tags=self.tags,
            transit_gateway_id=self.transit_gateway_id)


def get_peering_attachment(filters: Optional[Sequence[Union['GetPeeringAttachmentFilterArgs', 'GetPeeringAttachmentFilterArgsDict']]] = None,
                           id: Optional[str] = None,
                           tags: Optional[Mapping[str, str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPeeringAttachmentResult:
    """
    Get information on an EC2 Transit Gateway Peering Attachment.

    ## Example Usage

    ### By Filter

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2transitgateway.get_peering_attachment(filters=[{
        "name": "transit-gateway-attachment-id",
        "values": ["tgw-attach-12345678"],
    }])
    ```

    ### By Identifier

    ```python
    import pulumi
    import pulumi_aws as aws

    attachment = aws.ec2transitgateway.get_peering_attachment(id="tgw-attach-12345678")
    ```


    :param Sequence[Union['GetPeeringAttachmentFilterArgs', 'GetPeeringAttachmentFilterArgsDict']] filters: One or more configuration blocks containing name-values filters. Detailed below.
    :param str id: Identifier of the EC2 Transit Gateway Peering Attachment.
    :param Mapping[str, str] tags: Mapping of tags, each pair of which must exactly match
           a pair on the specific EC2 Transit Gateway Peering Attachment to retrieve.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2transitgateway/getPeeringAttachment:getPeeringAttachment', __args__, opts=opts, typ=GetPeeringAttachmentResult).value

    return AwaitableGetPeeringAttachmentResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        peer_account_id=pulumi.get(__ret__, 'peer_account_id'),
        peer_region=pulumi.get(__ret__, 'peer_region'),
        peer_transit_gateway_id=pulumi.get(__ret__, 'peer_transit_gateway_id'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'),
        transit_gateway_id=pulumi.get(__ret__, 'transit_gateway_id'))
def get_peering_attachment_output(filters: Optional[pulumi.Input[Optional[Sequence[Union['GetPeeringAttachmentFilterArgs', 'GetPeeringAttachmentFilterArgsDict']]]]] = None,
                                  id: Optional[pulumi.Input[Optional[str]]] = None,
                                  tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                  opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPeeringAttachmentResult]:
    """
    Get information on an EC2 Transit Gateway Peering Attachment.

    ## Example Usage

    ### By Filter

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2transitgateway.get_peering_attachment(filters=[{
        "name": "transit-gateway-attachment-id",
        "values": ["tgw-attach-12345678"],
    }])
    ```

    ### By Identifier

    ```python
    import pulumi
    import pulumi_aws as aws

    attachment = aws.ec2transitgateway.get_peering_attachment(id="tgw-attach-12345678")
    ```


    :param Sequence[Union['GetPeeringAttachmentFilterArgs', 'GetPeeringAttachmentFilterArgsDict']] filters: One or more configuration blocks containing name-values filters. Detailed below.
    :param str id: Identifier of the EC2 Transit Gateway Peering Attachment.
    :param Mapping[str, str] tags: Mapping of tags, each pair of which must exactly match
           a pair on the specific EC2 Transit Gateway Peering Attachment to retrieve.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['tags'] = tags
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:ec2transitgateway/getPeeringAttachment:getPeeringAttachment', __args__, opts=opts, typ=GetPeeringAttachmentResult)
    return __ret__.apply(lambda __response__: GetPeeringAttachmentResult(
        filters=pulumi.get(__response__, 'filters'),
        id=pulumi.get(__response__, 'id'),
        peer_account_id=pulumi.get(__response__, 'peer_account_id'),
        peer_region=pulumi.get(__response__, 'peer_region'),
        peer_transit_gateway_id=pulumi.get(__response__, 'peer_transit_gateway_id'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags'),
        transit_gateway_id=pulumi.get(__response__, 'transit_gateway_id')))
