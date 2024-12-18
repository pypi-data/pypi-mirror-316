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
    'GetSnapshotResult',
    'AwaitableGetSnapshotResult',
    'get_snapshot',
    'get_snapshot_output',
]

@pulumi.output_type
class GetSnapshotResult:
    """
    A collection of values returned by getSnapshot.
    """
    def __init__(__self__, arn=None, data_encryption_key_id=None, description=None, encrypted=None, filters=None, id=None, kms_key_id=None, most_recent=None, outpost_arn=None, owner_alias=None, owner_id=None, owners=None, restorable_by_user_ids=None, snapshot_id=None, snapshot_ids=None, start_time=None, state=None, storage_tier=None, tags=None, volume_id=None, volume_size=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if data_encryption_key_id and not isinstance(data_encryption_key_id, str):
            raise TypeError("Expected argument 'data_encryption_key_id' to be a str")
        pulumi.set(__self__, "data_encryption_key_id", data_encryption_key_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if encrypted and not isinstance(encrypted, bool):
            raise TypeError("Expected argument 'encrypted' to be a bool")
        pulumi.set(__self__, "encrypted", encrypted)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if outpost_arn and not isinstance(outpost_arn, str):
            raise TypeError("Expected argument 'outpost_arn' to be a str")
        pulumi.set(__self__, "outpost_arn", outpost_arn)
        if owner_alias and not isinstance(owner_alias, str):
            raise TypeError("Expected argument 'owner_alias' to be a str")
        pulumi.set(__self__, "owner_alias", owner_alias)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if owners and not isinstance(owners, list):
            raise TypeError("Expected argument 'owners' to be a list")
        pulumi.set(__self__, "owners", owners)
        if restorable_by_user_ids and not isinstance(restorable_by_user_ids, list):
            raise TypeError("Expected argument 'restorable_by_user_ids' to be a list")
        pulumi.set(__self__, "restorable_by_user_ids", restorable_by_user_ids)
        if snapshot_id and not isinstance(snapshot_id, str):
            raise TypeError("Expected argument 'snapshot_id' to be a str")
        pulumi.set(__self__, "snapshot_id", snapshot_id)
        if snapshot_ids and not isinstance(snapshot_ids, list):
            raise TypeError("Expected argument 'snapshot_ids' to be a list")
        pulumi.set(__self__, "snapshot_ids", snapshot_ids)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if storage_tier and not isinstance(storage_tier, str):
            raise TypeError("Expected argument 'storage_tier' to be a str")
        pulumi.set(__self__, "storage_tier", storage_tier)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if volume_id and not isinstance(volume_id, str):
            raise TypeError("Expected argument 'volume_id' to be a str")
        pulumi.set(__self__, "volume_id", volume_id)
        if volume_size and not isinstance(volume_size, int):
            raise TypeError("Expected argument 'volume_size' to be a int")
        pulumi.set(__self__, "volume_size", volume_size)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the EBS Snapshot.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="dataEncryptionKeyId")
    def data_encryption_key_id(self) -> str:
        """
        The data encryption key identifier for the snapshot.
        """
        return pulumi.get(self, "data_encryption_key_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description for the snapshot
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def encrypted(self) -> bool:
        """
        Whether the snapshot is encrypted.
        """
        return pulumi.get(self, "encrypted")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetSnapshotFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> str:
        """
        ARN for the KMS encryption key.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> str:
        """
        ARN of the Outpost on which the snapshot is stored.
        """
        return pulumi.get(self, "outpost_arn")

    @property
    @pulumi.getter(name="ownerAlias")
    def owner_alias(self) -> str:
        """
        Value from an Amazon-maintained list (`amazon`, `aws-marketplace`, `microsoft`) of snapshot owners.
        """
        return pulumi.get(self, "owner_alias")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> str:
        """
        AWS account ID of the EBS snapshot owner.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def owners(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "owners")

    @property
    @pulumi.getter(name="restorableByUserIds")
    def restorable_by_user_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "restorable_by_user_ids")

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> str:
        """
        Snapshot ID (e.g., snap-59fcb34e).
        """
        return pulumi.get(self, "snapshot_id")

    @property
    @pulumi.getter(name="snapshotIds")
    def snapshot_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "snapshot_ids")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        Time stamp when the snapshot was initiated.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Snapshot state.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageTier")
    def storage_tier(self) -> str:
        """
        Storage tier in which the snapshot is stored.
        """
        return pulumi.get(self, "storage_tier")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags for the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> str:
        """
        Volume ID (e.g., vol-59fcb34e).
        """
        return pulumi.get(self, "volume_id")

    @property
    @pulumi.getter(name="volumeSize")
    def volume_size(self) -> int:
        """
        Size of the drive in GiBs.
        """
        return pulumi.get(self, "volume_size")


class AwaitableGetSnapshotResult(GetSnapshotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSnapshotResult(
            arn=self.arn,
            data_encryption_key_id=self.data_encryption_key_id,
            description=self.description,
            encrypted=self.encrypted,
            filters=self.filters,
            id=self.id,
            kms_key_id=self.kms_key_id,
            most_recent=self.most_recent,
            outpost_arn=self.outpost_arn,
            owner_alias=self.owner_alias,
            owner_id=self.owner_id,
            owners=self.owners,
            restorable_by_user_ids=self.restorable_by_user_ids,
            snapshot_id=self.snapshot_id,
            snapshot_ids=self.snapshot_ids,
            start_time=self.start_time,
            state=self.state,
            storage_tier=self.storage_tier,
            tags=self.tags,
            volume_id=self.volume_id,
            volume_size=self.volume_size)


def get_snapshot(filters: Optional[Sequence[Union['GetSnapshotFilterArgs', 'GetSnapshotFilterArgsDict']]] = None,
                 most_recent: Optional[bool] = None,
                 owners: Optional[Sequence[str]] = None,
                 restorable_by_user_ids: Optional[Sequence[str]] = None,
                 snapshot_ids: Optional[Sequence[str]] = None,
                 tags: Optional[Mapping[str, str]] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSnapshotResult:
    """
    Use this data source to get information about an EBS Snapshot for use when provisioning EBS Volumes

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    ebs_volume = aws.ebs.get_snapshot(most_recent=True,
        owners=["self"],
        filters=[
            {
                "name": "volume-size",
                "values": ["40"],
            },
            {
                "name": "tag:Name",
                "values": ["Example"],
            },
        ])
    ```


    :param Sequence[Union['GetSnapshotFilterArgs', 'GetSnapshotFilterArgsDict']] filters: One or more name/value pairs to filter off of. There are
           several valid keys, for a full reference, check out
           [describe-snapshots in the AWS CLI reference][1].
    :param bool most_recent: If more than one result is returned, use the most recent snapshot.
    :param Sequence[str] owners: Returns the snapshots owned by the specified owner id. Multiple owners can be specified.
    :param Sequence[str] restorable_by_user_ids: One or more AWS accounts IDs that can create volumes from the snapshot.
    :param Sequence[str] snapshot_ids: Returns information on a specific snapshot_id.
    :param Mapping[str, str] tags: Map of tags for the resource.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['mostRecent'] = most_recent
    __args__['owners'] = owners
    __args__['restorableByUserIds'] = restorable_by_user_ids
    __args__['snapshotIds'] = snapshot_ids
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ebs/getSnapshot:getSnapshot', __args__, opts=opts, typ=GetSnapshotResult).value

    return AwaitableGetSnapshotResult(
        arn=pulumi.get(__ret__, 'arn'),
        data_encryption_key_id=pulumi.get(__ret__, 'data_encryption_key_id'),
        description=pulumi.get(__ret__, 'description'),
        encrypted=pulumi.get(__ret__, 'encrypted'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        kms_key_id=pulumi.get(__ret__, 'kms_key_id'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        outpost_arn=pulumi.get(__ret__, 'outpost_arn'),
        owner_alias=pulumi.get(__ret__, 'owner_alias'),
        owner_id=pulumi.get(__ret__, 'owner_id'),
        owners=pulumi.get(__ret__, 'owners'),
        restorable_by_user_ids=pulumi.get(__ret__, 'restorable_by_user_ids'),
        snapshot_id=pulumi.get(__ret__, 'snapshot_id'),
        snapshot_ids=pulumi.get(__ret__, 'snapshot_ids'),
        start_time=pulumi.get(__ret__, 'start_time'),
        state=pulumi.get(__ret__, 'state'),
        storage_tier=pulumi.get(__ret__, 'storage_tier'),
        tags=pulumi.get(__ret__, 'tags'),
        volume_id=pulumi.get(__ret__, 'volume_id'),
        volume_size=pulumi.get(__ret__, 'volume_size'))
def get_snapshot_output(filters: Optional[pulumi.Input[Optional[Sequence[Union['GetSnapshotFilterArgs', 'GetSnapshotFilterArgsDict']]]]] = None,
                        most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                        owners: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        restorable_by_user_ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        snapshot_ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                        opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetSnapshotResult]:
    """
    Use this data source to get information about an EBS Snapshot for use when provisioning EBS Volumes

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    ebs_volume = aws.ebs.get_snapshot(most_recent=True,
        owners=["self"],
        filters=[
            {
                "name": "volume-size",
                "values": ["40"],
            },
            {
                "name": "tag:Name",
                "values": ["Example"],
            },
        ])
    ```


    :param Sequence[Union['GetSnapshotFilterArgs', 'GetSnapshotFilterArgsDict']] filters: One or more name/value pairs to filter off of. There are
           several valid keys, for a full reference, check out
           [describe-snapshots in the AWS CLI reference][1].
    :param bool most_recent: If more than one result is returned, use the most recent snapshot.
    :param Sequence[str] owners: Returns the snapshots owned by the specified owner id. Multiple owners can be specified.
    :param Sequence[str] restorable_by_user_ids: One or more AWS accounts IDs that can create volumes from the snapshot.
    :param Sequence[str] snapshot_ids: Returns information on a specific snapshot_id.
    :param Mapping[str, str] tags: Map of tags for the resource.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['mostRecent'] = most_recent
    __args__['owners'] = owners
    __args__['restorableByUserIds'] = restorable_by_user_ids
    __args__['snapshotIds'] = snapshot_ids
    __args__['tags'] = tags
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:ebs/getSnapshot:getSnapshot', __args__, opts=opts, typ=GetSnapshotResult)
    return __ret__.apply(lambda __response__: GetSnapshotResult(
        arn=pulumi.get(__response__, 'arn'),
        data_encryption_key_id=pulumi.get(__response__, 'data_encryption_key_id'),
        description=pulumi.get(__response__, 'description'),
        encrypted=pulumi.get(__response__, 'encrypted'),
        filters=pulumi.get(__response__, 'filters'),
        id=pulumi.get(__response__, 'id'),
        kms_key_id=pulumi.get(__response__, 'kms_key_id'),
        most_recent=pulumi.get(__response__, 'most_recent'),
        outpost_arn=pulumi.get(__response__, 'outpost_arn'),
        owner_alias=pulumi.get(__response__, 'owner_alias'),
        owner_id=pulumi.get(__response__, 'owner_id'),
        owners=pulumi.get(__response__, 'owners'),
        restorable_by_user_ids=pulumi.get(__response__, 'restorable_by_user_ids'),
        snapshot_id=pulumi.get(__response__, 'snapshot_id'),
        snapshot_ids=pulumi.get(__response__, 'snapshot_ids'),
        start_time=pulumi.get(__response__, 'start_time'),
        state=pulumi.get(__response__, 'state'),
        storage_tier=pulumi.get(__response__, 'storage_tier'),
        tags=pulumi.get(__response__, 'tags'),
        volume_id=pulumi.get(__response__, 'volume_id'),
        volume_size=pulumi.get(__response__, 'volume_size')))
