from functools import lru_cache
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from lightning_sdk.api.user_api import UserApi
from lightning_sdk.job.base import _BaseJob
from lightning_sdk.job.v1 import _JobV1
from lightning_sdk.job.v2 import _JobV2

if TYPE_CHECKING:
    from lightning_sdk.machine import Machine
    from lightning_sdk.organization import Organization
    from lightning_sdk.status import Status
    from lightning_sdk.studio import Studio
    from lightning_sdk.teamspace import Teamspace
    from lightning_sdk.user import User


@lru_cache(maxsize=None)
def _has_jobs_v2() -> bool:
    api = UserApi()
    try:
        return api._get_feature_flags().jobs_v2
    except Exception:
        return False


class Job(_BaseJob):
    def __init__(
        self,
        name: str,
        teamspace: Union[str, "Teamspace", None] = None,
        org: Union[str, "Organization", None] = None,
        user: Union[str, "User", None] = None,
        *,
        _fetch_job: bool = True,
    ) -> None:
        internal_job_cls = _JobV2 if _has_jobs_v2() else _JobV1

        self._internal_job = internal_job_cls(
            name=name,
            teamspace=teamspace,
            org=org,
            user=user,
            _fetch_job=_fetch_job,
        )

    @classmethod
    def run(
        cls,
        name: str,
        machine: "Machine",
        command: Optional[str] = None,
        studio: Union["Studio", str, None] = None,
        image: Union[str, None] = None,
        teamspace: Union[str, "Teamspace", None] = None,
        org: Union[str, "Organization", None] = None,
        user: Union[str, "User", None] = None,
        cluster: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        interruptible: bool = False,
        image_credentials: Optional[str] = None,
        cluster_auth: bool = False,
        artifacts_local: Optional[str] = None,
        artifacts_remote: Optional[str] = None,
    ) -> "Job":
        ret_val = super().run(
            name=name,
            machine=machine,
            command=command,
            studio=studio,
            image=image,
            teamspace=teamspace,
            org=org,
            user=user,
            cluster=cluster,
            env=env,
            interruptible=interruptible,
            image_credentials=image_credentials,
            cluster_auth=cluster_auth,
            artifacts_local=artifacts_local,
            artifacts_remote=artifacts_remote,
        )
        # required for typing with "Job"
        assert isinstance(ret_val, cls)
        return ret_val

    def _submit(
        self,
        machine: "Machine",
        command: Optional[str] = None,
        studio: Optional["Studio"] = None,
        image: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        interruptible: bool = False,
        cluster: Optional[str] = None,
        image_credentials: Optional[str] = None,
        cluster_auth: bool = False,
        artifacts_local: Optional[str] = None,
        artifacts_remote: Optional[str] = None,
    ) -> None:
        self._job = self._internal_job._submit(
            machine=machine,
            cluster=cluster,
            command=command,
            studio=studio,
            image=image,
            env=env,
            interruptible=interruptible,
            image_credentials=image_credentials,
            cluster_auth=cluster_auth,
            artifacts_local=artifacts_local,
            artifacts_remote=artifacts_remote,
        )
        return self

    def stop(self) -> None:
        return self._internal_job.stop()

    def delete(self) -> None:
        return self._internal_job.delete()

    @property
    def status(self) -> "Status":
        return self._internal_job.status

    @property
    def machine(self) -> "Machine":
        return self._internal_job.machine

    @property
    def artifact_path(self) -> Optional[str]:
        return self._internal_job.artifact_path

    @property
    def snapshot_path(self) -> Optional[str]:
        return self._internal_job.snapshot_path

    @property
    def share_path(self) -> Optional[str]:
        return self._internal_job.share_path

    def _update_internal_job(self) -> None:
        return self._internal_job._update_internal_job()

    @property
    def name(self) -> str:
        return self._internal_job.name

    @property
    def teamspace(self) -> "Teamspace":
        return self._internal_job._teamspace

    @property
    def cluster(self) -> Optional[str]:
        return self._internal_job.cluster

    def __getattr__(self, key: str) -> Any:
        """Forward the attribute lookup to the internal job implementation."""
        try:
            return getattr(super(), key)
        except AttributeError:
            return getattr(self._internal_job, key)
