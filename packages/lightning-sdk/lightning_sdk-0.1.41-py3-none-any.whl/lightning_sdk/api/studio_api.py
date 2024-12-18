import json
import os
import tempfile
import time
import warnings
import zipfile
from threading import Event, Thread
from typing import Any, Dict, Mapping, Optional, Tuple, Union

import backoff
import requests
from tqdm import tqdm

from lightning_sdk.api.utils import (
    _COMPUTE_NAME_TO_MACHINE,
    _MACHINE_TO_COMPUTE_NAME,
    _create_app,
    _DummyBody,
    _DummyResponse,
    _FileUploader,
    _machine_to_compute_name,
    _sanitize_studio_remote_path,
)
from lightning_sdk.api.utils import (
    _get_cloud_url as _cloud_url,
)
from lightning_sdk.constants import _LIGHTNING_DEBUG
from lightning_sdk.lightning_cloud.login import Auth
from lightning_sdk.lightning_cloud.openapi import (
    CloudspaceIdRunsBody,
    Externalv1LightningappInstance,
    IdCodeconfigBody,
    IdExecuteBody1,
    IdForkBody1,
    IdStartBody,
    ProjectIdCloudspacesBody,
    V1CloudSpace,
    V1CloudSpaceInstanceConfig,
    V1CloudSpaceSeedFile,
    V1CloudSpaceState,
    V1GetCloudSpaceInstanceStatusResponse,
    V1GetLongRunningCommandInCloudSpaceResponse,
    V1LoginRequest,
    V1Plugin,
    V1PluginsListResponse,
    V1UserRequestedComputeConfig,
)
from lightning_sdk.lightning_cloud.rest_client import LightningClient
from lightning_sdk.machine import Machine


class StudioApi:
    """Internal API client for Studio requests (mainly http requests)."""

    def __init__(self) -> None:
        self._cloud_url = _cloud_url()
        self._client = LightningClient(max_tries=7)
        self._keep_alive_threads: Mapping[str, Thread] = {}
        self._keep_alive_events: Mapping[str, Event] = {}

    def start_keeping_alive(self, teamspace_id: str, studio_id: str) -> None:
        """Starts keeping the studio alive."""
        key = f"{teamspace_id}-{studio_id}"
        self._keep_alive_threads[key] = Thread(
            target=self._send_keepalives, kwargs={"teamspace_id": teamspace_id, "studio_id": studio_id}, daemon=True
        )
        self._keep_alive_events[key] = Event()
        self._keep_alive_threads[key].start()

    def stop_keeping_alive(self, teamspace_id: str, studio_id: str) -> None:
        """Stops keeping the studio alive."""
        key = f"{teamspace_id}-{studio_id}"

        if key in self._keep_alive_threads:
            self._keep_alive_events[key].set()
            self._keep_alive_threads[key].join()

    def _send_keepalives(self, teamspace_id: str, studio_id: str) -> None:
        """Sends keepalive requests as long as the event isn't set."""
        keep_alive_freq = os.environ.get("LIGHTNING_KEEPALIVE_FREQUENCY", 30)
        key = f"{teamspace_id}-{studio_id}"
        while not self._keep_alive_events[key].is_set():
            self._client.cloud_space_service_keep_alive_cloud_space_instance(
                body=_DummyBody(), project_id=teamspace_id, id=studio_id
            )
            time.sleep(keep_alive_freq)

    def get_studio(
        self,
        name: str,
        teamspace_id: str,
    ) -> V1CloudSpace:
        """Gets the current studio corresponding to the given name in the given teamspace."""
        res = self._client.cloud_space_service_list_cloud_spaces(project_id=teamspace_id, name=name)
        if not res.cloudspaces:
            raise ValueError(f"Studio {name} does not exist")
        return res.cloudspaces[0]

    def get_studio_by_id(
        self,
        studio_id: str,
        teamspace_id: str,
    ) -> V1CloudSpace:
        """Gets the current studio corresponding to the passed id."""
        return self._client.cloud_space_service_get_cloud_space(project_id=teamspace_id, id=studio_id)

    def create_studio(
        self,
        name: str,
        teamspace_id: str,
        cluster: Optional[str] = None,
    ) -> V1CloudSpace:
        """Create a Studio with a given name in a given Teamspace on a possibly given cluster."""
        body = ProjectIdCloudspacesBody(
            cluster_id=cluster,
            name=name,
            display_name=name,
            seed_files=[V1CloudSpaceSeedFile(path="main.py", contents="print('Hello, Lightning World!')\n")],
        )
        studio = self._client.cloud_space_service_create_cloud_space(body, teamspace_id)

        run_body = CloudspaceIdRunsBody(
            cluster_id=studio.cluster_id,
            local_source=True,
        )
        _ = self._client.cloud_space_service_create_lightning_run(
            project_id=teamspace_id, cloudspace_id=studio.id, body=run_body
        )

        return studio

    def get_studio_status(self, studio_id: str, teamspace_id: str) -> V1GetCloudSpaceInstanceStatusResponse:
        """Gets the current (internal) Studio status."""
        return self._client.cloud_space_service_get_cloud_space_instance_status(
            project_id=teamspace_id,
            id=studio_id,
        )

    @backoff.on_exception(backoff.expo, AttributeError, max_tries=10)
    def _check_code_status_top_up_restore_finished(self, studio_id: str, teamspace_id: str) -> bool:
        """Retries checking the top_up_restore_finished value of the code status when there's an AttributeError."""
        startup_status = self.get_studio_status(studio_id, teamspace_id).in_use.startup_status
        return startup_status and startup_status.top_up_restore_finished

    @backoff.on_exception(backoff.expo, AttributeError, max_tries=10)
    def _check_code_status_sync_in_progress(self, studio_id: str, teamspace_id: str) -> bool:
        """Retries checking the sync_in_progress value of the code status when there's an AttributeError."""
        return self.get_studio_status(studio_id, teamspace_id).in_use.sync_in_progress

    def start_studio(
        self, studio_id: str, teamspace_id: str, machine: Union[Machine, str], interruptible: False
    ) -> None:
        """Start an existing Studio."""
        if _machine_to_compute_name(machine) == _machine_to_compute_name(Machine.CPU_SMALL):
            warnings.warn(
                f"{Machine.CPU_SMALL} is not a valid machine for starting a Studio. "
                "It is reserved for running jobs only. "
                "The Studio will be started with a CPU machine instead."
            )
            machine = Machine.CPU

        self._client.cloud_space_service_start_cloud_space_instance(
            IdStartBody(
                compute_config=V1UserRequestedComputeConfig(name=_machine_to_compute_name(machine), spot=interruptible)
            ),
            teamspace_id,
            studio_id,
        )

        while self._check_code_status_sync_in_progress(studio_id, teamspace_id):
            time.sleep(1)

        while True:
            if self._check_code_status_top_up_restore_finished(studio_id, teamspace_id):
                break
            time.sleep(1)

        if _LIGHTNING_DEBUG:
            code_status = self.get_studio_status(studio_id, teamspace_id)
            instance_id = code_status.in_use.cloud_space_instance_id
            print(f"Studio started | {teamspace_id=} {studio_id=} {instance_id=}")

    def stop_studio(self, studio_id: str, teamspace_id: str) -> None:
        """Stop an existing Studio."""
        self.stop_keeping_alive(teamspace_id=teamspace_id, studio_id=studio_id)

        self._client.cloud_space_service_stop_cloud_space_instance(
            project_id=teamspace_id,
            id=studio_id,
        )

        # block until studio is really stopped
        while self._get_studio_instance_status(studio_id=studio_id, teamspace_id=teamspace_id) not in (
            None,
            "CLOUD_SPACE_INSTANCE_STATE_STOPPED",
        ):
            time.sleep(1)

    def _get_studio_instance_status(self, studio_id: str, teamspace_id: str) -> Optional[str]:
        """Returns status of the in-use instance of the Studio."""
        internal_status = self.get_studio_status(studio_id=studio_id, teamspace_id=teamspace_id).in_use
        if internal_status is None:
            return None

        return internal_status.phase

    def _get_studio_instance_status_from_object(self, studio: V1CloudSpace) -> Optional[str]:
        return getattr(getattr(studio.code_status, "in_use", None), "phase", None)

    def _request_switch(
        self, studio_id: str, teamspace_id: str, machine: Union[Machine, str], interruptible: bool
    ) -> None:
        """Switches given Studio to a new machine type."""
        if _machine_to_compute_name(machine) == _machine_to_compute_name(Machine.CPU_SMALL):
            warnings.warn(
                f"{Machine.CPU_SMALL} is not a valid machine for switching a Studio. "
                "It is reserved for running jobs only. "
                "The Studio will be switched to a CPU machine instead."
            )
            machine = Machine.CPU

        compute_name = _machine_to_compute_name(machine)
        # TODO: UI sends disk size here, maybe we need to also?
        body = IdCodeconfigBody(compute_config=V1UserRequestedComputeConfig(name=compute_name, spot=interruptible))
        self._client.cloud_space_service_update_cloud_space_instance_config(
            id=studio_id,
            project_id=teamspace_id,
            body=body,
        )

    def switch_studio_machine(
        self, studio_id: str, teamspace_id: str, machine: Union[Machine, str], interruptible: bool
    ) -> None:
        """Switches given Studio to a new machine type."""
        self._request_switch(
            studio_id=studio_id, teamspace_id=teamspace_id, machine=machine, interruptible=interruptible
        )

        # Wait until it's time to switch
        while True:
            startup_status = self.get_studio_status(studio_id, teamspace_id).requested.startup_status
            if startup_status and startup_status.initial_restore_finished:
                break
            time.sleep(1)

        self._client.cloud_space_service_switch_cloud_space_instance(teamspace_id, studio_id)

        # Wait until the new machine is ready to use
        while True:
            startup_status = self.get_studio_status(studio_id, teamspace_id).in_use.startup_status
            if startup_status and startup_status.top_up_restore_finished:
                break
            time.sleep(1)

    def get_machine(self, studio_id: str, teamspace_id: str) -> Machine:
        """Get the current machine type the given Studio is running on."""
        response: V1CloudSpaceInstanceConfig = self._client.cloud_space_service_get_cloud_space_instance_config(
            project_id=teamspace_id, id=studio_id
        )
        return _COMPUTE_NAME_TO_MACHINE[response.compute_config.name]

    def get_interruptible(self, studio_id: str, teamspace_id: str) -> bool:
        """Get whether the Studio is running on a interruptible instance."""
        response: V1CloudSpaceInstanceConfig = self._client.cloud_space_service_get_cloud_space_instance_config(
            project_id=teamspace_id, id=studio_id
        )

        return response.compute_config.spot

    def _get_detached_command_status(
        self, studio_id: str, teamspace_id: str, session_id: str
    ) -> V1GetLongRunningCommandInCloudSpaceResponse:
        """Get the status of a detached command."""
        # we need to decode this manually since this is ndjson and not usual json
        response_data = self._client.cloud_space_service_get_long_running_command_in_cloud_space_stream(
            project_id=teamspace_id, id=studio_id, session=session_id, _preload_content=False
        )

        if not response_data:
            raise RuntimeError("Unable to get status of running command")

        # convert from ndjson to json
        lines = ",".join(response_data.data.decode().splitlines())
        text = f"[{lines}]"
        # store in dummy class since api client deserializes the data attribute
        correct_response = _DummyResponse(text.encode())
        # decode as list of object as we have multiple of those
        responses = self._client.api_client.deserialize(
            correct_response, response_type="list[StreamResultOfV1GetLongRunningCommandInCloudSpaceResponse]"
        )

        for response in responses:
            yield response.result

    def run_studio_commands(self, studio_id: str, teamspace_id: str, *commands: str) -> Tuple[str, int]:
        """Run given commands in a given Studio."""
        response_submit = self._client.cloud_space_service_execute_command_in_cloud_space(
            IdExecuteBody1("; ".join(commands), detached=True),
            project_id=teamspace_id,
            id=studio_id,
        )

        if not response_submit:
            raise RuntimeError("Unable to submit command")

        if response_submit.session_name == "":
            raise RuntimeError("The session name should be defined.")

        while True:
            output = ""
            exit_code = None

            for resp in self._get_detached_command_status(
                studio_id=studio_id,
                teamspace_id=teamspace_id,
                session_id=response_submit.session_name,
            ):
                if resp.exit_code == -1:
                    break
                if exit_code is None:
                    exit_code = resp.exit_code
                elif exit_code != resp.exit_code:
                    raise RuntimeError("Cannot determine exit code")

                output += resp.output

            if exit_code is not None:
                return output, exit_code

            time.sleep(1)

    def update_autoshutdown(
        self,
        studio_id: str,
        teamspace_id: str,
        studio: V1CloudSpace,
        enabled: Optional[bool] = None,
        idle_shutdown_seconds: int = 0,
    ) -> None:
        """Update the autoshutdown time of the given Studio."""
        if enabled is None:
            enabled = not studio.code_config.disable_auto_shutdown
        body = IdCodeconfigBody(
            disable_auto_shutdown=not enabled,
            idle_shutdown_seconds=idle_shutdown_seconds,
            compute_config=studio.code_config.compute_config,
        )
        self._client.cloud_space_service_update_cloud_space_instance_config(
            id=studio_id,
            project_id=teamspace_id,
            body=body,
        )

    def duplicate_studio(self, studio_id: str, teamspace_id: str, target_teamspace_id: str) -> Dict[str, str]:
        """Duplicates the given Studio from a given Teamspace into a given target Teamspace."""
        target_teamspace = self._client.projects_service_get_project(target_teamspace_id)
        init_kwargs = {}
        if target_teamspace.owner_type == "user":
            from lightning_sdk.api.user_api import UserApi

            init_kwargs["user"] = UserApi()._get_user_by_id(target_teamspace.owner_id).username
        elif target_teamspace.owner_type == "organization":
            from lightning_sdk.api.org_api import OrgApi

            init_kwargs["org"] = OrgApi()._get_org_by_id(target_teamspace.owner_id).name

        new_cloudspace = self._client.cloud_space_service_fork_cloud_space(
            IdForkBody1(target_project_id=target_teamspace_id), project_id=teamspace_id, id=studio_id
        )

        while self.get_studio_by_id(new_cloudspace.id, target_teamspace_id).state != V1CloudSpaceState.READY:
            time.sleep(1)

        init_kwargs["name"] = new_cloudspace.name
        init_kwargs["teamspace"] = target_teamspace.name

        self.start_studio(new_cloudspace.id, target_teamspace_id, Machine.CPU, False)
        return init_kwargs

    def delete_studio(self, studio_id: str, teamspace_id: str) -> None:
        """Delete existing given Studio."""
        self.stop_keeping_alive(teamspace_id=teamspace_id, studio_id=studio_id)
        self._client.cloud_space_service_delete_cloud_space(project_id=teamspace_id, id=studio_id)

    def upload_file(
        self, studio_id: str, teamspace_id: str, cluster_id: str, file_path: str, remote_path: str, progress_bar: bool
    ) -> None:
        """Uploads file to given remote path on the studio."""
        _FileUploader(
            client=self._client,
            teamspace_id=teamspace_id,
            cluster_id=cluster_id,
            file_path=file_path,
            remote_path=_sanitize_studio_remote_path(remote_path, studio_id),
            progress_bar=progress_bar,
        )()

    def download_file(
        self, path: str, target_path: str, studio_id: str, teamspace_id: str, cluster_id: str, progress_bar: bool = True
    ) -> None:
        """Downloads a given file from a Studio to a target location."""
        # TODO: Update this endpoint to permit basic auth
        auth = Auth()
        auth.authenticate()
        token = self._client.auth_service_login(V1LoginRequest(auth.api_key)).token

        query_params = {
            "clusterId": cluster_id,
            "key": _sanitize_studio_remote_path(path, studio_id),
            "token": token,
        }

        r = requests.get(
            f"{self._client.api_client.configuration.host}/v1/projects/{teamspace_id}/artifacts/download",
            params=query_params,
            stream=True,
        )
        total_length = int(r.headers.get("content-length"))

        if progress_bar:
            pbar = tqdm(
                desc=f"Downloading {os.path.split(path)[1]}",
                total=total_length,
                unit="B",
                unit_scale=True,
                unit_divisor=1000,
            )

            pbar_update = pbar.update
        else:
            pbar_update = lambda x: None

        target_dir = os.path.split(target_path)[0]
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
        with open(target_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=4096 * 8):
                f.write(chunk)
                pbar_update(len(chunk))

    def download_folder(
        self, path: str, target_path: str, studio_id: str, teamspace_id: str, cluster_id: str, progress_bar: bool = True
    ) -> None:
        """Downloads a given folder from a Studio to a target location."""
        # TODO: Update this endpoint to permit basic auth
        auth = Auth()
        auth.authenticate()
        token = self._client.auth_service_login(V1LoginRequest(auth.api_key)).token

        query_params = {
            "clusterId": cluster_id,
            "prefix": _sanitize_studio_remote_path(path, studio_id),
            "token": token,
        }

        r = requests.get(
            f"{self._client.api_client.configuration.host}/v1/projects/{teamspace_id}/artifacts/download",
            params=query_params,
            stream=True,
        )

        if progress_bar:
            pbar = tqdm(
                desc=f"Downloading {os.path.split(path)[1]}",
                unit="B",
                unit_scale=True,
                unit_divisor=1000,
            )

            pbar_update = pbar.update
        else:
            pbar_update = lambda x: None

        if target_path:
            os.makedirs(target_path, exist_ok=True)

        with tempfile.TemporaryFile() as f:
            for chunk in r.iter_content(chunk_size=4096 * 8):
                f.write(chunk)
                pbar_update(len(chunk))

            with zipfile.ZipFile(f) as z:
                z.extractall(target_path)

    def install_plugin(self, studio_id: str, teamspace_id: str, plugin_name: str) -> str:
        """Installs the given plugin."""
        resp: V1Plugin = self._client.cloud_space_service_install_plugin(
            project_id=teamspace_id, id=studio_id, plugin_id=plugin_name
        )
        if not (resp.state == "installation_success" and resp.error == ""):
            raise RuntimeError(f"Failed to install plugin {plugin_name}: {resp.error}")

        additional_info = resp.additional_info or ""

        return additional_info.strip("\n").strip()

    def uninstall_plugin(self, studio_id: str, teamspace_id: str, plugin_name: str) -> None:
        """Uninstalls the given plugin."""
        resp: V1Plugin = self._client.cloud_space_service_uninstall_plugin(
            project_id=teamspace_id, id=studio_id, plugin_id=plugin_name
        )
        if not (resp.state == "uninstallation_success" and resp.error == ""):
            raise RuntimeError(f"Failed to uninstall plugin {plugin_name}: {resp.error}")

    def execute_plugin(self, studio_id: str, teamspace_id: str, plugin_name: str) -> Tuple[str, int]:
        """Executes the given plugin."""
        resp: V1Plugin = self._client.cloud_space_service_execute_plugin(
            project_id=teamspace_id, id=studio_id, plugin_id=plugin_name
        )
        if not (resp.state == "execution_success" and resp.error == ""):
            raise RuntimeError(f"Failed to execute plugin {plugin_name}: {resp.error}")

        additional_info_string = resp.additional_info
        additional_info = json.loads(additional_info_string)
        port = int(additional_info["port"])

        output_str = ""

        # if port is specified greater than 0 this means the plugin is interactive.
        # Prompt the user to head to the browser
        if port > 0:
            output_str = (
                f"Plugin {plugin_name} is interactive. Have a look at https://{port}-{studio_id}.cloudspaces.litng.ai"
            )

        elif port < 0:
            output_str = "This plugin can only be used on the browser interface of a Studio!"

        # TODO: retrieve actual command output?
        elif port == 0:
            output_str = f"Successfully executed plugin {plugin_name}"

        return output_str, port

    def list_available_plugins(self, studio_id: str, teamspace_id: str) -> Dict[str, str]:
        """Lists the available plugins."""
        resp: V1PluginsListResponse = self._client.cloud_space_service_list_available_plugins(
            project_id=teamspace_id, id=studio_id
        )
        return resp.plugins

    def list_installed_plugins(self, studio_id: str, teamspace_id: str) -> Dict[str, str]:
        """Lists all installed plugins."""
        resp: V1PluginsListResponse = self._client.cloud_space_service_list_installed_plugins(
            project_id=teamspace_id, id=studio_id
        )
        return resp.plugins

    def create_job(
        self,
        entrypoint: str,
        name: str,
        machine: Machine,
        studio_id: str,
        teamspace_id: str,
        cluster_id: str,
        interruptible: bool,
    ) -> Externalv1LightningappInstance:
        """Creates a job with given commands."""
        return self._create_app(
            studio_id=studio_id,
            teamspace_id=teamspace_id,
            cluster_id=cluster_id,
            plugin_type="job",
            entrypoint=entrypoint,
            name=name,
            compute=_MACHINE_TO_COMPUTE_NAME[machine],
            interruptible=interruptible,
        )

    def create_multi_machine_job(
        self,
        entrypoint: str,
        name: str,
        num_instances: int,
        machine: Machine,
        strategy: str,
        studio_id: str,
        teamspace_id: str,
        cluster_id: str,
        interruptible: bool,
    ) -> Externalv1LightningappInstance:
        """Creates a multi-machine job with given commands."""
        distributed_args = {
            "cloud_compute": _MACHINE_TO_COMPUTE_NAME[machine],
            "num_instances": num_instances,
            "strategy": strategy,
        }
        return self._create_app(
            studio_id=studio_id,
            teamspace_id=teamspace_id,
            cluster_id=cluster_id,
            plugin_type="distributed_plugin",
            entrypoint=entrypoint,
            name=name,
            distributedArguments=json.dumps(distributed_args),
            interruptible=interruptible,
        )

    def create_data_prep_machine_job(
        self,
        entrypoint: str,
        name: str,
        num_instances: int,
        machine: Machine,
        studio_id: str,
        teamspace_id: str,
        cluster_id: str,
        interruptible: bool,
    ) -> Externalv1LightningappInstance:
        """Creates a multi-machine job with given commands."""
        data_prep_args = {
            "cloud_compute": _MACHINE_TO_COMPUTE_NAME[machine],
            "num_instances": num_instances,
        }
        return self._create_app(
            studio_id=studio_id,
            teamspace_id=teamspace_id,
            cluster_id=cluster_id,
            plugin_type="litdata",
            entrypoint=entrypoint,
            name=name,
            dataPrepArguments=json.dumps(data_prep_args),
            interruptible=interruptible,
        )

    def create_inference_job(
        self,
        entrypoint: str,
        name: str,
        machine: Machine,
        min_replicas: str,
        max_replicas: str,
        max_batch_size: str,
        timeout_batching: str,
        scale_in_interval: str,
        scale_out_interval: str,
        endpoint: str,
        studio_id: str,
        teamspace_id: str,
        cluster_id: str,
        interruptible: bool,
    ) -> Externalv1LightningappInstance:
        """Creates an inference job for given endpoint."""
        return self._create_app(
            studio_id=studio_id,
            teamspace_id=teamspace_id,
            cluster_id=cluster_id,
            plugin_type="inference_plugin",
            compute=_MACHINE_TO_COMPUTE_NAME[machine],
            entrypoint=entrypoint,
            name=name,
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            max_batch_size=max_batch_size,
            timeout_batching=timeout_batching,
            scale_in_interval=scale_in_interval,
            scale_out_interval=scale_out_interval,
            endpoint=endpoint,
            interruptible=interruptible,
        )

    def _create_app(
        self, studio_id: str, teamspace_id: str, cluster_id: str, plugin_type: str, **other_arguments: Any
    ) -> Externalv1LightningappInstance:
        """Creates an arbitrary app."""
        return _create_app(
            self._client,
            studio_id=studio_id,
            teamspace_id=teamspace_id,
            cluster_id=cluster_id,
            plugin_type=plugin_type,
            **other_arguments,
        )
