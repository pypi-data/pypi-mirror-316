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
    'GetEngineVersionResult',
    'AwaitableGetEngineVersionResult',
    'get_engine_version',
    'get_engine_version_output',
]

@pulumi.output_type
class GetEngineVersionResult:
    """
    A collection of values returned by getEngineVersion.
    """
    def __init__(__self__, default_character_set=None, default_only=None, engine=None, engine_description=None, exportable_log_types=None, filters=None, has_major_target=None, has_minor_target=None, id=None, include_all=None, latest=None, parameter_group_family=None, preferred_major_targets=None, preferred_upgrade_targets=None, preferred_versions=None, status=None, supported_character_sets=None, supported_feature_names=None, supported_modes=None, supported_timezones=None, supports_global_databases=None, supports_limitless_database=None, supports_log_exports_to_cloudwatch=None, supports_parallel_query=None, supports_read_replica=None, valid_major_targets=None, valid_minor_targets=None, valid_upgrade_targets=None, version=None, version_actual=None, version_description=None):
        if default_character_set and not isinstance(default_character_set, str):
            raise TypeError("Expected argument 'default_character_set' to be a str")
        pulumi.set(__self__, "default_character_set", default_character_set)
        if default_only and not isinstance(default_only, bool):
            raise TypeError("Expected argument 'default_only' to be a bool")
        pulumi.set(__self__, "default_only", default_only)
        if engine and not isinstance(engine, str):
            raise TypeError("Expected argument 'engine' to be a str")
        pulumi.set(__self__, "engine", engine)
        if engine_description and not isinstance(engine_description, str):
            raise TypeError("Expected argument 'engine_description' to be a str")
        pulumi.set(__self__, "engine_description", engine_description)
        if exportable_log_types and not isinstance(exportable_log_types, list):
            raise TypeError("Expected argument 'exportable_log_types' to be a list")
        pulumi.set(__self__, "exportable_log_types", exportable_log_types)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if has_major_target and not isinstance(has_major_target, bool):
            raise TypeError("Expected argument 'has_major_target' to be a bool")
        pulumi.set(__self__, "has_major_target", has_major_target)
        if has_minor_target and not isinstance(has_minor_target, bool):
            raise TypeError("Expected argument 'has_minor_target' to be a bool")
        pulumi.set(__self__, "has_minor_target", has_minor_target)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if include_all and not isinstance(include_all, bool):
            raise TypeError("Expected argument 'include_all' to be a bool")
        pulumi.set(__self__, "include_all", include_all)
        if latest and not isinstance(latest, bool):
            raise TypeError("Expected argument 'latest' to be a bool")
        pulumi.set(__self__, "latest", latest)
        if parameter_group_family and not isinstance(parameter_group_family, str):
            raise TypeError("Expected argument 'parameter_group_family' to be a str")
        pulumi.set(__self__, "parameter_group_family", parameter_group_family)
        if preferred_major_targets and not isinstance(preferred_major_targets, list):
            raise TypeError("Expected argument 'preferred_major_targets' to be a list")
        pulumi.set(__self__, "preferred_major_targets", preferred_major_targets)
        if preferred_upgrade_targets and not isinstance(preferred_upgrade_targets, list):
            raise TypeError("Expected argument 'preferred_upgrade_targets' to be a list")
        pulumi.set(__self__, "preferred_upgrade_targets", preferred_upgrade_targets)
        if preferred_versions and not isinstance(preferred_versions, list):
            raise TypeError("Expected argument 'preferred_versions' to be a list")
        pulumi.set(__self__, "preferred_versions", preferred_versions)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if supported_character_sets and not isinstance(supported_character_sets, list):
            raise TypeError("Expected argument 'supported_character_sets' to be a list")
        pulumi.set(__self__, "supported_character_sets", supported_character_sets)
        if supported_feature_names and not isinstance(supported_feature_names, list):
            raise TypeError("Expected argument 'supported_feature_names' to be a list")
        pulumi.set(__self__, "supported_feature_names", supported_feature_names)
        if supported_modes and not isinstance(supported_modes, list):
            raise TypeError("Expected argument 'supported_modes' to be a list")
        pulumi.set(__self__, "supported_modes", supported_modes)
        if supported_timezones and not isinstance(supported_timezones, list):
            raise TypeError("Expected argument 'supported_timezones' to be a list")
        pulumi.set(__self__, "supported_timezones", supported_timezones)
        if supports_global_databases and not isinstance(supports_global_databases, bool):
            raise TypeError("Expected argument 'supports_global_databases' to be a bool")
        pulumi.set(__self__, "supports_global_databases", supports_global_databases)
        if supports_limitless_database and not isinstance(supports_limitless_database, bool):
            raise TypeError("Expected argument 'supports_limitless_database' to be a bool")
        pulumi.set(__self__, "supports_limitless_database", supports_limitless_database)
        if supports_log_exports_to_cloudwatch and not isinstance(supports_log_exports_to_cloudwatch, bool):
            raise TypeError("Expected argument 'supports_log_exports_to_cloudwatch' to be a bool")
        pulumi.set(__self__, "supports_log_exports_to_cloudwatch", supports_log_exports_to_cloudwatch)
        if supports_parallel_query and not isinstance(supports_parallel_query, bool):
            raise TypeError("Expected argument 'supports_parallel_query' to be a bool")
        pulumi.set(__self__, "supports_parallel_query", supports_parallel_query)
        if supports_read_replica and not isinstance(supports_read_replica, bool):
            raise TypeError("Expected argument 'supports_read_replica' to be a bool")
        pulumi.set(__self__, "supports_read_replica", supports_read_replica)
        if valid_major_targets and not isinstance(valid_major_targets, list):
            raise TypeError("Expected argument 'valid_major_targets' to be a list")
        pulumi.set(__self__, "valid_major_targets", valid_major_targets)
        if valid_minor_targets and not isinstance(valid_minor_targets, list):
            raise TypeError("Expected argument 'valid_minor_targets' to be a list")
        pulumi.set(__self__, "valid_minor_targets", valid_minor_targets)
        if valid_upgrade_targets and not isinstance(valid_upgrade_targets, list):
            raise TypeError("Expected argument 'valid_upgrade_targets' to be a list")
        pulumi.set(__self__, "valid_upgrade_targets", valid_upgrade_targets)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)
        if version_actual and not isinstance(version_actual, str):
            raise TypeError("Expected argument 'version_actual' to be a str")
        pulumi.set(__self__, "version_actual", version_actual)
        if version_description and not isinstance(version_description, str):
            raise TypeError("Expected argument 'version_description' to be a str")
        pulumi.set(__self__, "version_description", version_description)

    @property
    @pulumi.getter(name="defaultCharacterSet")
    def default_character_set(self) -> str:
        """
        Default character set for new instances of the engine version.
        """
        return pulumi.get(self, "default_character_set")

    @property
    @pulumi.getter(name="defaultOnly")
    def default_only(self) -> Optional[bool]:
        return pulumi.get(self, "default_only")

    @property
    @pulumi.getter
    def engine(self) -> str:
        return pulumi.get(self, "engine")

    @property
    @pulumi.getter(name="engineDescription")
    def engine_description(self) -> str:
        """
        Description of the engine.
        """
        return pulumi.get(self, "engine_description")

    @property
    @pulumi.getter(name="exportableLogTypes")
    def exportable_log_types(self) -> Sequence[str]:
        """
        Set of log types that the engine version has available for export to CloudWatch Logs.
        """
        return pulumi.get(self, "exportable_log_types")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetEngineVersionFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="hasMajorTarget")
    def has_major_target(self) -> Optional[bool]:
        return pulumi.get(self, "has_major_target")

    @property
    @pulumi.getter(name="hasMinorTarget")
    def has_minor_target(self) -> Optional[bool]:
        return pulumi.get(self, "has_minor_target")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="includeAll")
    def include_all(self) -> Optional[bool]:
        return pulumi.get(self, "include_all")

    @property
    @pulumi.getter
    def latest(self) -> Optional[bool]:
        return pulumi.get(self, "latest")

    @property
    @pulumi.getter(name="parameterGroupFamily")
    def parameter_group_family(self) -> str:
        return pulumi.get(self, "parameter_group_family")

    @property
    @pulumi.getter(name="preferredMajorTargets")
    def preferred_major_targets(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "preferred_major_targets")

    @property
    @pulumi.getter(name="preferredUpgradeTargets")
    def preferred_upgrade_targets(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "preferred_upgrade_targets")

    @property
    @pulumi.getter(name="preferredVersions")
    def preferred_versions(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "preferred_versions")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the engine version, either `available` or `deprecated`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="supportedCharacterSets")
    def supported_character_sets(self) -> Sequence[str]:
        """
        Set of character sets supported by th engine version.
        """
        return pulumi.get(self, "supported_character_sets")

    @property
    @pulumi.getter(name="supportedFeatureNames")
    def supported_feature_names(self) -> Sequence[str]:
        """
        Set of features supported by the engine version.
        """
        return pulumi.get(self, "supported_feature_names")

    @property
    @pulumi.getter(name="supportedModes")
    def supported_modes(self) -> Sequence[str]:
        """
        Set of supported engine version modes.
        """
        return pulumi.get(self, "supported_modes")

    @property
    @pulumi.getter(name="supportedTimezones")
    def supported_timezones(self) -> Sequence[str]:
        """
        Set of the time zones supported by the engine version.
        """
        return pulumi.get(self, "supported_timezones")

    @property
    @pulumi.getter(name="supportsGlobalDatabases")
    def supports_global_databases(self) -> bool:
        """
        Whether you can use Aurora global databases with the engine version.
        """
        return pulumi.get(self, "supports_global_databases")

    @property
    @pulumi.getter(name="supportsLimitlessDatabase")
    def supports_limitless_database(self) -> bool:
        """
        Whether the engine version supports Aurora Limitless Database.
        """
        return pulumi.get(self, "supports_limitless_database")

    @property
    @pulumi.getter(name="supportsLogExportsToCloudwatch")
    def supports_log_exports_to_cloudwatch(self) -> bool:
        """
        Whether the engine version supports exporting the log types specified by `exportable_log_types` to CloudWatch Logs.
        """
        return pulumi.get(self, "supports_log_exports_to_cloudwatch")

    @property
    @pulumi.getter(name="supportsParallelQuery")
    def supports_parallel_query(self) -> bool:
        """
        Whether you can use Aurora parallel query with the engine version.
        """
        return pulumi.get(self, "supports_parallel_query")

    @property
    @pulumi.getter(name="supportsReadReplica")
    def supports_read_replica(self) -> bool:
        """
        Whether the engine version supports read replicas.
        """
        return pulumi.get(self, "supports_read_replica")

    @property
    @pulumi.getter(name="validMajorTargets")
    def valid_major_targets(self) -> Sequence[str]:
        """
        Set of versions that are valid major version upgrades for the engine version.
        """
        return pulumi.get(self, "valid_major_targets")

    @property
    @pulumi.getter(name="validMinorTargets")
    def valid_minor_targets(self) -> Sequence[str]:
        """
        Set of versions that are valid minor version upgrades for the engine version.
        """
        return pulumi.get(self, "valid_minor_targets")

    @property
    @pulumi.getter(name="validUpgradeTargets")
    def valid_upgrade_targets(self) -> Sequence[str]:
        """
        Set of versions that are valid major or minor upgrades for the engine version.
        """
        return pulumi.get(self, "valid_upgrade_targets")

    @property
    @pulumi.getter
    def version(self) -> str:
        return pulumi.get(self, "version")

    @property
    @pulumi.getter(name="versionActual")
    def version_actual(self) -> str:
        """
        Complete engine version.
        """
        return pulumi.get(self, "version_actual")

    @property
    @pulumi.getter(name="versionDescription")
    def version_description(self) -> str:
        """
        Description of the engine version.
        """
        return pulumi.get(self, "version_description")


class AwaitableGetEngineVersionResult(GetEngineVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEngineVersionResult(
            default_character_set=self.default_character_set,
            default_only=self.default_only,
            engine=self.engine,
            engine_description=self.engine_description,
            exportable_log_types=self.exportable_log_types,
            filters=self.filters,
            has_major_target=self.has_major_target,
            has_minor_target=self.has_minor_target,
            id=self.id,
            include_all=self.include_all,
            latest=self.latest,
            parameter_group_family=self.parameter_group_family,
            preferred_major_targets=self.preferred_major_targets,
            preferred_upgrade_targets=self.preferred_upgrade_targets,
            preferred_versions=self.preferred_versions,
            status=self.status,
            supported_character_sets=self.supported_character_sets,
            supported_feature_names=self.supported_feature_names,
            supported_modes=self.supported_modes,
            supported_timezones=self.supported_timezones,
            supports_global_databases=self.supports_global_databases,
            supports_limitless_database=self.supports_limitless_database,
            supports_log_exports_to_cloudwatch=self.supports_log_exports_to_cloudwatch,
            supports_parallel_query=self.supports_parallel_query,
            supports_read_replica=self.supports_read_replica,
            valid_major_targets=self.valid_major_targets,
            valid_minor_targets=self.valid_minor_targets,
            valid_upgrade_targets=self.valid_upgrade_targets,
            version=self.version,
            version_actual=self.version_actual,
            version_description=self.version_description)


def get_engine_version(default_only: Optional[bool] = None,
                       engine: Optional[str] = None,
                       filters: Optional[Sequence[Union['GetEngineVersionFilterArgs', 'GetEngineVersionFilterArgsDict']]] = None,
                       has_major_target: Optional[bool] = None,
                       has_minor_target: Optional[bool] = None,
                       include_all: Optional[bool] = None,
                       latest: Optional[bool] = None,
                       parameter_group_family: Optional[str] = None,
                       preferred_major_targets: Optional[Sequence[str]] = None,
                       preferred_upgrade_targets: Optional[Sequence[str]] = None,
                       preferred_versions: Optional[Sequence[str]] = None,
                       version: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEngineVersionResult:
    """
    Information about an RDS engine version.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.rds.get_engine_version(engine="mysql",
        preferred_versions=[
            "8.0.27",
            "8.0.26",
        ])
    ```

    ### With `filter`

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.rds.get_engine_version(engine="aurora-postgresql",
        version="10.14",
        include_all=True,
        filters=[{
            "name": "engine-mode",
            "values": ["serverless"],
        }])
    ```


    :param bool default_only: Whether the engine version must be an AWS-defined default version. Some engines have multiple default versions, such as for each major version. Using `default_only` may help avoid `multiple RDS engine versions` errors. See also `latest`.
    :param str engine: Database engine. Engine values include `aurora`, `aurora-mysql`, `aurora-postgresql`, `docdb`, `mariadb`, `mysql`, `neptune`, `oracle-ee`, `oracle-se`, `oracle-se1`, `oracle-se2`, `postgres`, `sqlserver-ee`, `sqlserver-ex`, `sqlserver-se`, and `sqlserver-web`.
           
           The following arguments are optional:
    :param Sequence[Union['GetEngineVersionFilterArgs', 'GetEngineVersionFilterArgsDict']] filters: One or more name/value pairs to use in filtering versions. There are several valid keys; for a full reference, check out [describe-db-engine-versions in the AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/rds/describe-db-engine-versions.html).
    :param bool has_major_target: Whether the engine version must have one or more major upgrade targets. Not including `has_major_target` or setting it to `false` doesn't imply that there's no corresponding major upgrade target for the engine version.
    :param bool has_minor_target: Whether the engine version must have one or more minor upgrade targets. Not including `has_minor_target` or setting it to `false` doesn't imply that there's no corresponding minor upgrade target for the engine version.
    :param bool include_all: Whether the engine version `status` can either be `deprecated` or `available`. When not set or set to `false`, the engine version `status` will always be `available`.
    :param bool latest: Whether the engine version is the most recent version matching the other criteria. This is different from `default_only` in important ways: "default" relies on AWS-defined defaults, the latest version isn't always the default, and AWS might have multiple default versions for an engine. As a result, `default_only` might not prevent errors from `multiple RDS engine versions`, while `latest` will. (`latest` can be used with `default_only`.) **Note:** The data source uses a best-effort approach at selecting the latest version. Due to the complexity of version identifiers across engines and incomplete version date information provided by AWS, using `latest` may not always result in the engine version being the actual latest version.
    :param str parameter_group_family: Name of a specific database parameter group family. Examples of parameter group families are `mysql8.0`, `mariadb10.4`, and `postgres12`.
    :param Sequence[str] preferred_major_targets: Ordered list of preferred major version upgrade targets. The engine version will be the first match in the list unless the `latest` parameter is set to `true`. The engine version will be the default version if you don't include any criteria, such as `preferred_major_targets`.
    :param Sequence[str] preferred_upgrade_targets: Ordered list of preferred version upgrade targets. The engine version will be the first match in this list unless the `latest` parameter is set to `true`. The engine version will be the default version if you don't include any criteria, such as `preferred_upgrade_targets`.
    :param Sequence[str] preferred_versions: Ordered list of preferred versions. The engine version will be the first match in this list unless the `latest` parameter is set to `true`. The engine version will be the default version if you don't include any criteria, such as `preferred_versions`.
    """
    __args__ = dict()
    __args__['defaultOnly'] = default_only
    __args__['engine'] = engine
    __args__['filters'] = filters
    __args__['hasMajorTarget'] = has_major_target
    __args__['hasMinorTarget'] = has_minor_target
    __args__['includeAll'] = include_all
    __args__['latest'] = latest
    __args__['parameterGroupFamily'] = parameter_group_family
    __args__['preferredMajorTargets'] = preferred_major_targets
    __args__['preferredUpgradeTargets'] = preferred_upgrade_targets
    __args__['preferredVersions'] = preferred_versions
    __args__['version'] = version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:rds/getEngineVersion:getEngineVersion', __args__, opts=opts, typ=GetEngineVersionResult).value

    return AwaitableGetEngineVersionResult(
        default_character_set=pulumi.get(__ret__, 'default_character_set'),
        default_only=pulumi.get(__ret__, 'default_only'),
        engine=pulumi.get(__ret__, 'engine'),
        engine_description=pulumi.get(__ret__, 'engine_description'),
        exportable_log_types=pulumi.get(__ret__, 'exportable_log_types'),
        filters=pulumi.get(__ret__, 'filters'),
        has_major_target=pulumi.get(__ret__, 'has_major_target'),
        has_minor_target=pulumi.get(__ret__, 'has_minor_target'),
        id=pulumi.get(__ret__, 'id'),
        include_all=pulumi.get(__ret__, 'include_all'),
        latest=pulumi.get(__ret__, 'latest'),
        parameter_group_family=pulumi.get(__ret__, 'parameter_group_family'),
        preferred_major_targets=pulumi.get(__ret__, 'preferred_major_targets'),
        preferred_upgrade_targets=pulumi.get(__ret__, 'preferred_upgrade_targets'),
        preferred_versions=pulumi.get(__ret__, 'preferred_versions'),
        status=pulumi.get(__ret__, 'status'),
        supported_character_sets=pulumi.get(__ret__, 'supported_character_sets'),
        supported_feature_names=pulumi.get(__ret__, 'supported_feature_names'),
        supported_modes=pulumi.get(__ret__, 'supported_modes'),
        supported_timezones=pulumi.get(__ret__, 'supported_timezones'),
        supports_global_databases=pulumi.get(__ret__, 'supports_global_databases'),
        supports_limitless_database=pulumi.get(__ret__, 'supports_limitless_database'),
        supports_log_exports_to_cloudwatch=pulumi.get(__ret__, 'supports_log_exports_to_cloudwatch'),
        supports_parallel_query=pulumi.get(__ret__, 'supports_parallel_query'),
        supports_read_replica=pulumi.get(__ret__, 'supports_read_replica'),
        valid_major_targets=pulumi.get(__ret__, 'valid_major_targets'),
        valid_minor_targets=pulumi.get(__ret__, 'valid_minor_targets'),
        valid_upgrade_targets=pulumi.get(__ret__, 'valid_upgrade_targets'),
        version=pulumi.get(__ret__, 'version'),
        version_actual=pulumi.get(__ret__, 'version_actual'),
        version_description=pulumi.get(__ret__, 'version_description'))
def get_engine_version_output(default_only: Optional[pulumi.Input[Optional[bool]]] = None,
                              engine: Optional[pulumi.Input[str]] = None,
                              filters: Optional[pulumi.Input[Optional[Sequence[Union['GetEngineVersionFilterArgs', 'GetEngineVersionFilterArgsDict']]]]] = None,
                              has_major_target: Optional[pulumi.Input[Optional[bool]]] = None,
                              has_minor_target: Optional[pulumi.Input[Optional[bool]]] = None,
                              include_all: Optional[pulumi.Input[Optional[bool]]] = None,
                              latest: Optional[pulumi.Input[Optional[bool]]] = None,
                              parameter_group_family: Optional[pulumi.Input[Optional[str]]] = None,
                              preferred_major_targets: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              preferred_upgrade_targets: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              preferred_versions: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              version: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetEngineVersionResult]:
    """
    Information about an RDS engine version.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.rds.get_engine_version(engine="mysql",
        preferred_versions=[
            "8.0.27",
            "8.0.26",
        ])
    ```

    ### With `filter`

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.rds.get_engine_version(engine="aurora-postgresql",
        version="10.14",
        include_all=True,
        filters=[{
            "name": "engine-mode",
            "values": ["serverless"],
        }])
    ```


    :param bool default_only: Whether the engine version must be an AWS-defined default version. Some engines have multiple default versions, such as for each major version. Using `default_only` may help avoid `multiple RDS engine versions` errors. See also `latest`.
    :param str engine: Database engine. Engine values include `aurora`, `aurora-mysql`, `aurora-postgresql`, `docdb`, `mariadb`, `mysql`, `neptune`, `oracle-ee`, `oracle-se`, `oracle-se1`, `oracle-se2`, `postgres`, `sqlserver-ee`, `sqlserver-ex`, `sqlserver-se`, and `sqlserver-web`.
           
           The following arguments are optional:
    :param Sequence[Union['GetEngineVersionFilterArgs', 'GetEngineVersionFilterArgsDict']] filters: One or more name/value pairs to use in filtering versions. There are several valid keys; for a full reference, check out [describe-db-engine-versions in the AWS CLI reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/rds/describe-db-engine-versions.html).
    :param bool has_major_target: Whether the engine version must have one or more major upgrade targets. Not including `has_major_target` or setting it to `false` doesn't imply that there's no corresponding major upgrade target for the engine version.
    :param bool has_minor_target: Whether the engine version must have one or more minor upgrade targets. Not including `has_minor_target` or setting it to `false` doesn't imply that there's no corresponding minor upgrade target for the engine version.
    :param bool include_all: Whether the engine version `status` can either be `deprecated` or `available`. When not set or set to `false`, the engine version `status` will always be `available`.
    :param bool latest: Whether the engine version is the most recent version matching the other criteria. This is different from `default_only` in important ways: "default" relies on AWS-defined defaults, the latest version isn't always the default, and AWS might have multiple default versions for an engine. As a result, `default_only` might not prevent errors from `multiple RDS engine versions`, while `latest` will. (`latest` can be used with `default_only`.) **Note:** The data source uses a best-effort approach at selecting the latest version. Due to the complexity of version identifiers across engines and incomplete version date information provided by AWS, using `latest` may not always result in the engine version being the actual latest version.
    :param str parameter_group_family: Name of a specific database parameter group family. Examples of parameter group families are `mysql8.0`, `mariadb10.4`, and `postgres12`.
    :param Sequence[str] preferred_major_targets: Ordered list of preferred major version upgrade targets. The engine version will be the first match in the list unless the `latest` parameter is set to `true`. The engine version will be the default version if you don't include any criteria, such as `preferred_major_targets`.
    :param Sequence[str] preferred_upgrade_targets: Ordered list of preferred version upgrade targets. The engine version will be the first match in this list unless the `latest` parameter is set to `true`. The engine version will be the default version if you don't include any criteria, such as `preferred_upgrade_targets`.
    :param Sequence[str] preferred_versions: Ordered list of preferred versions. The engine version will be the first match in this list unless the `latest` parameter is set to `true`. The engine version will be the default version if you don't include any criteria, such as `preferred_versions`.
    """
    __args__ = dict()
    __args__['defaultOnly'] = default_only
    __args__['engine'] = engine
    __args__['filters'] = filters
    __args__['hasMajorTarget'] = has_major_target
    __args__['hasMinorTarget'] = has_minor_target
    __args__['includeAll'] = include_all
    __args__['latest'] = latest
    __args__['parameterGroupFamily'] = parameter_group_family
    __args__['preferredMajorTargets'] = preferred_major_targets
    __args__['preferredUpgradeTargets'] = preferred_upgrade_targets
    __args__['preferredVersions'] = preferred_versions
    __args__['version'] = version
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws:rds/getEngineVersion:getEngineVersion', __args__, opts=opts, typ=GetEngineVersionResult)
    return __ret__.apply(lambda __response__: GetEngineVersionResult(
        default_character_set=pulumi.get(__response__, 'default_character_set'),
        default_only=pulumi.get(__response__, 'default_only'),
        engine=pulumi.get(__response__, 'engine'),
        engine_description=pulumi.get(__response__, 'engine_description'),
        exportable_log_types=pulumi.get(__response__, 'exportable_log_types'),
        filters=pulumi.get(__response__, 'filters'),
        has_major_target=pulumi.get(__response__, 'has_major_target'),
        has_minor_target=pulumi.get(__response__, 'has_minor_target'),
        id=pulumi.get(__response__, 'id'),
        include_all=pulumi.get(__response__, 'include_all'),
        latest=pulumi.get(__response__, 'latest'),
        parameter_group_family=pulumi.get(__response__, 'parameter_group_family'),
        preferred_major_targets=pulumi.get(__response__, 'preferred_major_targets'),
        preferred_upgrade_targets=pulumi.get(__response__, 'preferred_upgrade_targets'),
        preferred_versions=pulumi.get(__response__, 'preferred_versions'),
        status=pulumi.get(__response__, 'status'),
        supported_character_sets=pulumi.get(__response__, 'supported_character_sets'),
        supported_feature_names=pulumi.get(__response__, 'supported_feature_names'),
        supported_modes=pulumi.get(__response__, 'supported_modes'),
        supported_timezones=pulumi.get(__response__, 'supported_timezones'),
        supports_global_databases=pulumi.get(__response__, 'supports_global_databases'),
        supports_limitless_database=pulumi.get(__response__, 'supports_limitless_database'),
        supports_log_exports_to_cloudwatch=pulumi.get(__response__, 'supports_log_exports_to_cloudwatch'),
        supports_parallel_query=pulumi.get(__response__, 'supports_parallel_query'),
        supports_read_replica=pulumi.get(__response__, 'supports_read_replica'),
        valid_major_targets=pulumi.get(__response__, 'valid_major_targets'),
        valid_minor_targets=pulumi.get(__response__, 'valid_minor_targets'),
        valid_upgrade_targets=pulumi.get(__response__, 'valid_upgrade_targets'),
        version=pulumi.get(__response__, 'version'),
        version_actual=pulumi.get(__response__, 'version_actual'),
        version_description=pulumi.get(__response__, 'version_description')))
