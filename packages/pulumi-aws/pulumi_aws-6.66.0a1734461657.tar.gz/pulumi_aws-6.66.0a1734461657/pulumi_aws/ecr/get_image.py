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

__all__ = [
    'GetImageResult',
    'AwaitableGetImageResult',
    'get_image',
    'get_image_output',
]

@pulumi.output_type
class GetImageResult:
    """
    A collection of values returned by getImage.
    """
    def __init__(__self__, id=None, image_digest=None, image_pushed_at=None, image_size_in_bytes=None, image_tag=None, image_tags=None, image_uri=None, most_recent=None, registry_id=None, repository_name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if image_digest and not isinstance(image_digest, str):
            raise TypeError("Expected argument 'image_digest' to be a str")
        pulumi.set(__self__, "image_digest", image_digest)
        if image_pushed_at and not isinstance(image_pushed_at, int):
            raise TypeError("Expected argument 'image_pushed_at' to be a int")
        pulumi.set(__self__, "image_pushed_at", image_pushed_at)
        if image_size_in_bytes and not isinstance(image_size_in_bytes, int):
            raise TypeError("Expected argument 'image_size_in_bytes' to be a int")
        pulumi.set(__self__, "image_size_in_bytes", image_size_in_bytes)
        if image_tag and not isinstance(image_tag, str):
            raise TypeError("Expected argument 'image_tag' to be a str")
        pulumi.set(__self__, "image_tag", image_tag)
        if image_tags and not isinstance(image_tags, list):
            raise TypeError("Expected argument 'image_tags' to be a list")
        pulumi.set(__self__, "image_tags", image_tags)
        if image_uri and not isinstance(image_uri, str):
            raise TypeError("Expected argument 'image_uri' to be a str")
        pulumi.set(__self__, "image_uri", image_uri)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if registry_id and not isinstance(registry_id, str):
            raise TypeError("Expected argument 'registry_id' to be a str")
        pulumi.set(__self__, "registry_id", registry_id)
        if repository_name and not isinstance(repository_name, str):
            raise TypeError("Expected argument 'repository_name' to be a str")
        pulumi.set(__self__, "repository_name", repository_name)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="imageDigest")
    def image_digest(self) -> str:
        return pulumi.get(self, "image_digest")

    @property
    @pulumi.getter(name="imagePushedAt")
    def image_pushed_at(self) -> int:
        """
        Date and time, expressed as a unix timestamp, at which the current image was pushed to the repository.
        """
        return pulumi.get(self, "image_pushed_at")

    @property
    @pulumi.getter(name="imageSizeInBytes")
    def image_size_in_bytes(self) -> int:
        """
        Size, in bytes, of the image in the repository.
        """
        return pulumi.get(self, "image_size_in_bytes")

    @property
    @pulumi.getter(name="imageTag")
    def image_tag(self) -> Optional[str]:
        return pulumi.get(self, "image_tag")

    @property
    @pulumi.getter(name="imageTags")
    def image_tags(self) -> Sequence[str]:
        """
        List of tags associated with this image.
        """
        return pulumi.get(self, "image_tags")

    @property
    @pulumi.getter(name="imageUri")
    def image_uri(self) -> str:
        """
        The URI for the specific image version specified by `image_tag` or `image_digest`.
        """
        return pulumi.get(self, "image_uri")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter(name="registryId")
    def registry_id(self) -> str:
        return pulumi.get(self, "registry_id")

    @property
    @pulumi.getter(name="repositoryName")
    def repository_name(self) -> str:
        return pulumi.get(self, "repository_name")


class AwaitableGetImageResult(GetImageResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetImageResult(
            id=self.id,
            image_digest=self.image_digest,
            image_pushed_at=self.image_pushed_at,
            image_size_in_bytes=self.image_size_in_bytes,
            image_tag=self.image_tag,
            image_tags=self.image_tags,
            image_uri=self.image_uri,
            most_recent=self.most_recent,
            registry_id=self.registry_id,
            repository_name=self.repository_name)


def get_image(image_digest: Optional[str] = None,
              image_tag: Optional[str] = None,
              most_recent: Optional[bool] = None,
              registry_id: Optional[str] = None,
              repository_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetImageResult:
    """
    The ECR Image data source allows the details of an image with a particular tag or digest to be retrieved.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    service_image = aws.ecr.get_image(repository_name="my/service",
        image_tag="latest")
    ```


    :param str image_digest: Sha256 digest of the image manifest. At least one of `image_digest`, `image_tag`, or `most_recent` must be specified.
    :param str image_tag: Tag associated with this image. At least one of `image_digest`, `image_tag`, or `most_recent` must be specified.
    :param bool most_recent: Return the most recently pushed image. At least one of `image_digest`, `image_tag`, or `most_recent` must be specified.
    :param str registry_id: ID of the Registry where the repository resides.
    :param str repository_name: Name of the ECR Repository.
    """
    __args__ = dict()
    __args__['imageDigest'] = image_digest
    __args__['imageTag'] = image_tag
    __args__['mostRecent'] = most_recent
    __args__['registryId'] = registry_id
    __args__['repositoryName'] = repository_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ecr/getImage:getImage', __args__, opts=opts, typ=GetImageResult).value

    return AwaitableGetImageResult(
        id=pulumi.get(__ret__, 'id'),
        image_digest=pulumi.get(__ret__, 'image_digest'),
        image_pushed_at=pulumi.get(__ret__, 'image_pushed_at'),
        image_size_in_bytes=pulumi.get(__ret__, 'image_size_in_bytes'),
        image_tag=pulumi.get(__ret__, 'image_tag'),
        image_tags=pulumi.get(__ret__, 'image_tags'),
        image_uri=pulumi.get(__ret__, 'image_uri'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        registry_id=pulumi.get(__ret__, 'registry_id'),
        repository_name=pulumi.get(__ret__, 'repository_name'))
def get_image_output(image_digest: Optional[pulumi.Input[Optional[str]]] = None,
                     image_tag: Optional[pulumi.Input[Optional[str]]] = None,
                     most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                     registry_id: Optional[pulumi.Input[Optional[str]]] = None,
                     repository_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetImageResult]:
    """
    The ECR Image data source allows the details of an image with a particular tag or digest to be retrieved.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    service_image = aws.ecr.get_image(repository_name="my/service",
        image_tag="latest")
    ```


    :param str image_digest: Sha256 digest of the image manifest. At least one of `image_digest`, `image_tag`, or `most_recent` must be specified.
    :param str image_tag: Tag associated with this image. At least one of `image_digest`, `image_tag`, or `most_recent` must be specified.
    :param bool most_recent: Return the most recently pushed image. At least one of `image_digest`, `image_tag`, or `most_recent` must be specified.
    :param str registry_id: ID of the Registry where the repository resides.
    :param str repository_name: Name of the ECR Repository.
    """
    __args__ = dict()
    __args__['imageDigest'] = image_digest
    __args__['imageTag'] = image_tag
    __args__['mostRecent'] = most_recent
    __args__['registryId'] = registry_id
    __args__['repositoryName'] = repository_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:ecr/getImage:getImage', __args__, opts=opts, typ=GetImageResult)
    return __ret__.apply(lambda __response__: GetImageResult(
        id=pulumi.get(__response__, 'id'),
        image_digest=pulumi.get(__response__, 'image_digest'),
        image_pushed_at=pulumi.get(__response__, 'image_pushed_at'),
        image_size_in_bytes=pulumi.get(__response__, 'image_size_in_bytes'),
        image_tag=pulumi.get(__response__, 'image_tag'),
        image_tags=pulumi.get(__response__, 'image_tags'),
        image_uri=pulumi.get(__response__, 'image_uri'),
        most_recent=pulumi.get(__response__, 'most_recent'),
        registry_id=pulumi.get(__response__, 'registry_id'),
        repository_name=pulumi.get(__response__, 'repository_name')))
