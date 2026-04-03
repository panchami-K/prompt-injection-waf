from typing import Optional, List
from openenv.core.env_server import Action, Observation, State


# ── What the AI attacker SENDS ──────────────────────────────────────────────
class WAFAction(Action):
    """The attacker sends a prompt injection attempt."""
    prompt: str
    task_name: str = "direct_injection"
    # For custom task only
    custom_secret: Optional[str] = None
    custom_triggers: Optional[List[str]] = None
    custom_max_attempts: Optional[int] = None

# ── What the environment SENDS BACK ─────────────────────────────────────────
class WAFObservation(Observation):
    """
    'done' and 'reward' are inherited from Observation base class.
    We add WAF-specific fields.
    """
    waf_response: str            # What the WAF/defender replied
    bypassed: bool               # Did the attacker get past the WAF?
    reason: str                  # Why bypassed=True or False (for debugging)
    attempts_used: int           # How many attempts used so far
    attempts_remaining: int      # How many attempts left
    task_name: str               # Which task is being run


# ── Episode metadata ─────────────────────────────────────────────────────────
class WAFState(State):
    """
    'episode_id' and 'step_count' are inherited from State base class.
    """
    task_name: str = "direct_injection"
    secret: str = ""             # The secret the WAF is protecting
    max_attempts: int = 5