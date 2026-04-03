import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from openenv.core.env_server.http_server import create_app
from models import WAFAction, WAFObservation
from server.prompt_injection_waf_environment import PromptInjectionWafEnvironment

# Create the openenv sub-app
openenv_app = create_app(
    PromptInjectionWafEnvironment,
    WAFAction,
    WAFObservation,
    env_name="prompt_injection_waf",
    max_concurrent_envs=10,
)

# Main app with health routes
app = FastAPI()

@app.get("/")
@app.head("/")
async def root():
    return JSONResponse({"status": "healthy", "env": "prompt_injection_waf"})

@app.get("/health")
@app.head("/health")
async def health():
    return JSONResponse({"status": "healthy"})

@app.post("/reset")
async def reset(request: dict = None):
    from starlette.requests import Request
    import json
    return openenv_app

# Mount openenv AFTER defining our routes
app.mount("/env", openenv_app)

# Also wire reset/step/state directly
from starlette.requests import Request
import httpx

@app.post("/reset")
async def reset(request: Request):
    body = await request.body()
    async with httpx.AsyncClient(app=openenv_app, base_url="http://test") as client:
        r = await client.post("/reset", content=body, headers={"content-type": "application/json"})
        return JSONResponse(r.json())

@app.post("/step")
async def step(request: Request):
    body = await request.body()
    async with httpx.AsyncClient(app=openenv_app, base_url="http://test") as client:
        r = await client.post("/step", content=body, headers={"content-type": "application/json"})
        return JSONResponse(r.json())

@app.get("/state")
async def state():
    async with httpx.AsyncClient(app=openenv_app, base_url="http://test") as client:
        r = await client.get("/state")
        return JSONResponse(r.json())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)