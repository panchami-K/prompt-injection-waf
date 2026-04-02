from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult
from models import WAFAction, WAFObservation, WAFState


class WAFEnv(EnvClient[WAFAction, WAFObservation, WAFState]):

    def _step_payload(self, action: WAFAction) -> dict:
        return {
            "prompt": action.prompt,
            "task_name": action.task_name,
        }

    def _parse_result(self, payload: dict) -> StepResult:
        obs_data = payload.get("observation", {})
        return StepResult(
            observation=WAFObservation(
                done=payload.get("done", False),
                reward=payload.get("reward"),
                waf_response=obs_data.get("waf_response", ""),
                bypassed=obs_data.get("bypassed", False),
                reason=obs_data.get("reason", ""),
                attempts_used=obs_data.get("attempts_used", 0),
                attempts_remaining=obs_data.get("attempts_remaining", 0),
                task_name=obs_data.get("task_name", "direct_injection"),
            ),
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: dict) -> WAFState:
        return WAFState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            task_name=payload.get("task_name", "direct_injection"),
            secret=payload.get("secret", ""),
            max_attempts=payload.get("max_attempts", 5),
        )