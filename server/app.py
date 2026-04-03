import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openenv.core.env_server.http_server import create_app
from models import WAFAction, WAFObservation
from server.prompt_injection_waf_environment import PromptInjectionWafEnvironment

app = create_app(
    PromptInjectionWafEnvironment,
    WAFAction,
    WAFObservation,
    env_name="prompt_injection_waf",
    max_concurrent_envs=10,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)