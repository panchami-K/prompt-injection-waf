import sys
import os

# Make sure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openenv.core.env_server.http_server import create_app
from models import WAFAction, WAFObservation
from server.prompt_injection_waf_environment import PromptInjectionWafEnvironment

# This MUST be a module-level variable named 'app'
app = create_app(
    PromptInjectionWafEnvironment,
    WAFAction,
    WAFObservation,
    env_name="prompt_injection_waf",
    max_concurrent_envs=10,
)

if __name__ == "__main__":
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host="0.0.0.0", port=args.port)