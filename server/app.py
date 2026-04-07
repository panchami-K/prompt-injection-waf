import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import WAFAction, WAFObservation, WAFState
from server.prompt_injection_waf_environment import PromptInjectionWafEnvironment
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import WAFAction, WAFObservation, WAFState

app = FastAPI()
env = PromptInjectionWafEnvironment()

@app.get("/")
@app.head("/")
async def root():
    return JSONResponse({"status": "healthy", "env": "prompt_injection_waf"})

@app.get("/health")
@app.head("/health")
async def health():
    return JSONResponse({"status": "healthy"})

@app.post("/reset")
async def reset(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    task_name = body.get("task_name", "direct_injection")
    obs = env.reset(task_name=task_name)
    return JSONResponse({
        "observation": obs.model_dump(),
        "reward": None,
        "done": False,
    })

@app.post("/step")
async def step(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    action_data = body.get("action", body)
    action = WAFAction(
        prompt=action_data.get("prompt", "test"),
        task_name=action_data.get("task_name", "direct_injection"),
    )
    obs = env.step(action)
    return JSONResponse({
        "observation": obs.model_dump(),
        "reward": obs.reward,
        "done": obs.done,
    })

@app.get("/state")
async def state():
    return JSONResponse(env.state.model_dump())

@app.get("/demo")
async def demo():
    return FileResponse(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "index.html"))

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")), name="static")

@app.post("/custom-reset")
async def custom_reset(request: Request):
    body = await request.json()
    secret = body.get("secret", "MYSECRET").upper()
    triggers = [t.strip().lower() for t in body.get("triggers", ["secret"])]
    max_attempts = int(body.get("max_attempts", 5))

    # Store custom config in env
    env._task_name = "custom"
    env._secret = secret
    env._custom_triggers = triggers
    env._max_attempts = max_attempts
    env._attempts_used = 0
    env._bypassed = False

    import uuid
    env._state = WAFState(
        episode_id=str(uuid.uuid4()),
        step_count=0,
        task_name="custom",
        secret=secret,
        max_attempts=max_attempts,
    )

    return JSONResponse({
        "observation": {
            "waf_response": f"Custom WAF active. Secret set. {len(triggers)} trigger word(s) configured. Good luck.",
            "bypassed": False,
            "reason": "Episode started.",
            "attempts_used": 0,
            "attempts_remaining": max_attempts,
            "task_name": "custom",
        },
        "reward": None,
        "done": False,
        "config": {
            "secret": secret,
            "triggers": triggers,
            "max_attempts": max_attempts,
        }
    })

def main():
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()