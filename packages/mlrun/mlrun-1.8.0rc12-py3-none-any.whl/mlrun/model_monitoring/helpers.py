# Copyright 2023 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
import typing

import numpy as np
import pandas as pd

if typing.TYPE_CHECKING:
    from mlrun.datastore import DataItem
    from mlrun.db.base import RunDBInterface
    from mlrun.projects import MlrunProject

from fnmatch import fnmatchcase
from typing import Optional

import mlrun
import mlrun.artifacts
import mlrun.common.model_monitoring.helpers
import mlrun.common.schemas.model_monitoring.constants as mm_constants
import mlrun.data_types.infer
import mlrun.model_monitoring
import mlrun.utils.helpers
from mlrun.common.schemas import ModelEndpoint
from mlrun.common.schemas.model_monitoring.model_endpoints import (
    ModelEndpointMonitoringMetric,
    _compose_full_name,
)
from mlrun.utils import logger


class _BatchDict(typing.TypedDict):
    minutes: int
    hours: int
    days: int


def _is_results_regex_match(
    existing_result_name: Optional[str],
    result_name_filters: Optional[list[str]],
) -> bool:
    if existing_result_name.count(".") != 3 or any(
        part == "" for part in existing_result_name.split(".")
    ):
        logger.warning(
            f"_is_results_regex_match: existing_result_name illegal, will be ignored."
            f" existing_result_name: {existing_result_name}"
        )
        return False
    existing_result_name = ".".join(existing_result_name.split(".")[i] for i in [1, 3])
    for result_name_filter in result_name_filters:
        if fnmatchcase(existing_result_name, result_name_filter):
            return True
    return False


def filter_results_by_regex(
    existing_result_names: Optional[list[str]] = None,
    result_name_filters: Optional[list[str]] = None,
) -> list[str]:
    """
    Filter a list of existing result names by a list of filters.

    This function returns only the results that match the filters provided. If no filters are given,
    it returns all results. Invalid inputs are ignored.

    :param existing_result_names: List of existing results' fully qualified names (FQNs)
                                  in the format: endpoint_id.app_name.type.name.
                                  Example: mep1.app1.result.metric1
    :param result_name_filters:   List of filters in the format: app.result_name.
                                  Wildcards can be used, such as app.result* or *.result

    :return: List of FQNs of the matching results
    """

    if not result_name_filters:
        return existing_result_names

    if not existing_result_names:
        return []

    #  filters validations
    validated_filters = []
    for result_name_filter in result_name_filters:
        if result_name_filter.count(".") != 1:
            logger.warning(
                f"filter_results_by_regex: result_name_filter illegal, will be ignored."
                f"Filter: {result_name_filter}"
            )
        else:
            validated_filters.append(result_name_filter)
    filtered_metrics_names = []
    for existing_result_name in existing_result_names:
        if _is_results_regex_match(
            existing_result_name=existing_result_name,
            result_name_filters=validated_filters,
        ):
            filtered_metrics_names.append(existing_result_name)
    return filtered_metrics_names


def get_stream_path(
    project: str,
    function_name: str = mm_constants.MonitoringFunctionNames.STREAM,
    stream_uri: typing.Optional[str] = None,
) -> str:
    """
    Get stream path from the project secret. If wasn't set, take it from the system configurations

    :param project:             Project name.
    :param function_name:       Application name. Default is model_monitoring_stream.
    :param stream_uri:          Stream URI. If provided, it will be used instead of the one from the project secret.

    :return:                    Monitoring stream path to the relevant application.
    """

    stream_uri = stream_uri or mlrun.get_secret_or_env(
        mm_constants.ProjectSecretKeys.STREAM_PATH
    )

    if not stream_uri or stream_uri == "v3io":
        stream_uri = mlrun.mlconf.get_model_monitoring_file_target_path(
            project=project,
            kind=mm_constants.FileTargetKind.STREAM,
            target="online",
            function_name=function_name,
        )

    return mlrun.common.model_monitoring.helpers.parse_monitoring_stream_path(
        stream_uri=stream_uri, project=project, function_name=function_name
    )


def get_monitoring_parquet_path(
    project: "MlrunProject",
    kind: str = mm_constants.FileTargetKind.PARQUET,
) -> str:
    """Get model monitoring parquet target for the current project and kind. The parquet target path is based on the
    project artifact path. If project artifact path is not defined, the parquet target path will be based on MLRun
    artifact path.

    :param project:     Project object.
    :param kind:        indicate the kind of the parquet path, can be either stream_parquet or stream_controller_parquet

    :return:           Monitoring parquet target path.
    """
    artifact_path = project.spec.artifact_path
    # Generate monitoring parquet path value
    parquet_path = mlrun.mlconf.get_model_monitoring_file_target_path(
        project=project.name,
        kind=kind,
        target="offline",
        artifact_path=artifact_path,
    )
    return parquet_path


def get_monitoring_stats_directory_path(
    project: str,
    kind: str = mm_constants.FileTargetKind.STATS,
) -> str:
    """
    Get model monitoring stats target for the current project and kind. The stats target path is based on the
    project artifact path. If project artifact path is not defined, the stats target path will be based on MLRun
    artifact path.
    :param project:     Project object.
    :param kind:        indicate the kind of the stats path
    :return:            Monitoring stats target path.
    """
    stats_path = mlrun.mlconf.get_model_monitoring_file_target_path(
        project=project,
        kind=kind,
    )
    return stats_path


def _get_monitoring_current_stats_file_path(project: str, endpoint_id: str) -> str:
    return os.path.join(
        get_monitoring_stats_directory_path(project),
        f"{endpoint_id}_current_stats.json",
    )


def _get_monitoring_drift_measures_file_path(project: str, endpoint_id: str) -> str:
    return os.path.join(
        get_monitoring_stats_directory_path(project),
        f"{endpoint_id}_drift_measures.json",
    )


def get_monitoring_current_stats_data(project: str, endpoint_id: str) -> "DataItem":
    """
    getter for data item of current stats for project and endpoint
    :param project: project name str
    :param endpoint_id: endpoint id str
    :return: DataItem
    """
    return mlrun.datastore.store_manager.object(
        _get_monitoring_current_stats_file_path(
            project=project, endpoint_id=endpoint_id
        )
    )


def get_monitoring_drift_measures_data(project: str, endpoint_id: str) -> "DataItem":
    """
    getter for data item of drift measures for project and endpoint
    :param project: project name str
    :param endpoint_id: endpoint id str
    :return: DataItem
    """
    return mlrun.datastore.store_manager.object(
        _get_monitoring_drift_measures_file_path(
            project=project, endpoint_id=endpoint_id
        )
    )


def get_tsdb_connection_string(
    secret_provider: typing.Optional[typing.Callable[[str], str]] = None,
) -> str:
    """Get TSDB connection string from the project secret. If wasn't set, take it from the system
    configurations.
    :param secret_provider: An optional secret provider to get the connection string secret.
    :return:                Valid TSDB connection string.
    """

    return mlrun.get_secret_or_env(
        key=mm_constants.ProjectSecretKeys.TSDB_CONNECTION,
        secret_provider=secret_provider,
    )


def batch_dict2timedelta(batch_dict: _BatchDict) -> datetime.timedelta:
    """
    Convert a batch dictionary to timedelta.

    :param batch_dict:  Batch dict.

    :return:            Timedelta.
    """
    return datetime.timedelta(**batch_dict)


def _get_monitoring_time_window_from_controller_run(
    project: str, db: "RunDBInterface"
) -> datetime.timedelta:
    """
    Get the base period form the controller.

    :param project: Project name.
    :param db:      DB interface.

    :return:    Timedelta for the controller to run.
    :raise:     MLRunNotFoundError if the controller isn't deployed yet
    """

    controller = db.get_function(
        name=mm_constants.MonitoringFunctionNames.APPLICATION_CONTROLLER,
        project=project,
    )
    if isinstance(controller, dict):
        controller = mlrun.runtimes.RemoteRuntime.from_dict(controller)
    elif not hasattr(controller, "to_dict"):
        raise mlrun.errors.MLRunNotFoundError()
    base_period = controller.spec.config["spec.triggers.cron_interval"]["attributes"][
        "interval"
    ]
    batch_dict = {
        mm_constants.EventFieldType.MINUTES: int(base_period[:-1]),
        mm_constants.EventFieldType.HOURS: 0,
        mm_constants.EventFieldType.DAYS: 0,
    }
    return batch_dict2timedelta(batch_dict)


def update_model_endpoint_last_request(
    project: str,
    model_endpoint: ModelEndpoint,
    current_request: datetime.datetime,
    db: "RunDBInterface",
) -> None:
    """
    Update the last request field of the model endpoint to be after the current request time.

    :param project:         Project name.
    :param model_endpoint:  Model endpoint object.
    :param current_request: current request time
    :param db:              DB interface.
    """
    is_batch_endpoint = (
        model_endpoint.metadata.endpoint_type == mm_constants.EndpointType.BATCH_EP
    )
    if not is_batch_endpoint:
        logger.info(
            "Update model endpoint last request time (EP with serving)",
            project=project,
            endpoint_id=model_endpoint.metadata.uid,
            name=model_endpoint.metadata.name,
            function_name=model_endpoint.spec.function_name,
            last_request=model_endpoint.status.last_request,
            current_request=current_request,
        )
        db.patch_model_endpoint(
            project=project,
            endpoint_id=model_endpoint.metadata.uid,
            name=model_endpoint.metadata.name,
            attributes={mm_constants.EventFieldType.LAST_REQUEST: current_request},
        )
    else:  # model endpoint without any serving function - close the window "manually"
        try:
            time_window = _get_monitoring_time_window_from_controller_run(project, db)
        except mlrun.errors.MLRunNotFoundError:
            logger.warn(
                "Not bumping model endpoint last request time - the monitoring controller isn't deployed yet.\n"
                "Call `project.enable_model_monitoring()` first."
            )
            return

        bumped_last_request = (
            current_request
            + time_window
            + datetime.timedelta(
                seconds=mlrun.mlconf.model_endpoint_monitoring.parquet_batching_timeout_secs
            )
        )
        logger.info(
            "Bumping model endpoint last request time (EP without serving)",
            project=project,
            endpoint_id=model_endpoint.metadata.uid,
            last_request=model_endpoint.status.last_request,
            current_request=current_request.isoformat(),
            bumped_last_request=bumped_last_request,
        )
        db.patch_model_endpoint(
            project=project,
            endpoint_id=model_endpoint.metadata.uid,
            name=model_endpoint.metadata.name,
            function_name=model_endpoint.spec.function_name,
            attributes={mm_constants.EventFieldType.LAST_REQUEST: bumped_last_request},
        )


def calculate_inputs_statistics(
    sample_set_statistics: dict, inputs: pd.DataFrame
) -> mlrun.common.model_monitoring.helpers.FeatureStats:
    """
    Calculate the inputs data statistics for drift monitoring purpose.

    :param sample_set_statistics: The sample set (stored end point's dataset to reference) statistics. The bins of the
                                  histograms of each feature will be used to recalculate the histograms of the inputs.
    :param inputs:                The inputs to calculate their statistics and later on - the drift with respect to the
                                  sample set.

    :returns: The calculated statistics of the inputs data.
    """

    # Use `DFDataInfer` to calculate the statistics over the inputs:
    inputs_statistics = mlrun.data_types.infer.DFDataInfer.get_stats(
        df=inputs, options=mlrun.data_types.infer.InferOptions.Histogram
    )

    # Recalculate the histograms over the bins that are set in the sample-set of the end point:
    for feature in list(inputs_statistics):
        if feature in sample_set_statistics:
            counts, bins = np.histogram(
                inputs[feature].to_numpy(),
                bins=sample_set_statistics[feature]["hist"][1],
            )
            inputs_statistics[feature]["hist"] = [
                counts.tolist(),
                bins.tolist(),
            ]
        else:
            # If the feature is not in the sample set and doesn't have a histogram, remove it from the statistics:
            inputs_statistics.pop(feature)

    return inputs_statistics


def get_result_instance_fqn(
    model_endpoint_id: str, app_name: str, result_name: str
) -> str:
    return f"{model_endpoint_id}.{app_name}.result.{result_name}"


def get_default_result_instance_fqn(model_endpoint_id: str) -> str:
    return get_result_instance_fqn(
        model_endpoint_id,
        mm_constants.HistogramDataDriftApplicationConstants.NAME,
        mm_constants.HistogramDataDriftApplicationConstants.GENERAL_RESULT_NAME,
    )


def get_invocations_fqn(project: str) -> str:
    return _compose_full_name(
        project=project,
        app=mm_constants.SpecialApps.MLRUN_INFRA,
        name=mm_constants.PredictionsQueryConstants.INVOCATIONS,
        type=mm_constants.ModelEndpointMonitoringMetricType.METRIC,
    )


def get_invocations_metric(project: str) -> ModelEndpointMonitoringMetric:
    """
    Return the invocations metric of any model endpoint in the given project.

    :param project: The project name.
    :returns:       The model monitoring metric object.
    """
    return ModelEndpointMonitoringMetric(
        project=project,
        app=mm_constants.SpecialApps.MLRUN_INFRA,
        type=mm_constants.ModelEndpointMonitoringMetricType.METRIC,
        name=mm_constants.PredictionsQueryConstants.INVOCATIONS,
        full_name=get_invocations_fqn(project),
    )


def _get_monitoring_schedules_folder_path(project: str) -> str:
    return typing.cast(
        str,
        mlrun.mlconf.get_model_monitoring_file_target_path(
            project=project, kind=mm_constants.FileTargetKind.MONITORING_SCHEDULES
        ),
    )


def _get_monitoring_schedules_file_path(*, project: str, endpoint_id: str) -> str:
    return os.path.join(
        _get_monitoring_schedules_folder_path(project), f"{endpoint_id}.json"
    )


def get_monitoring_schedules_data(*, project: str, endpoint_id: str) -> "DataItem":
    """
    Get the model monitoring schedules' data item of the project's model endpoint.
    """
    return mlrun.datastore.store_manager.object(
        _get_monitoring_schedules_file_path(project=project, endpoint_id=endpoint_id)
    )
