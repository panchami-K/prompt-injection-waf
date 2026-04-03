import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import WAFAction, WAFObservation, WAFState
from server.prompt_injection_waf_environment import PromptInjectionWafEnvironment
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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
    body = await request.json()
    task_name = body.get("task_name", "direct_injection")
    obs = env.reset(task_name=task_name)
    return JSONResponse({
        "observation": obs.model_dump(),
        "reward": None,
        "done": False,
    })

@app.post("/step")
async def step(request: Request):
    body = await request.json()
    action_data = body.get("action", body)
    action = WAFAction(
        prompt=action_data.get("prompt", ""),
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)