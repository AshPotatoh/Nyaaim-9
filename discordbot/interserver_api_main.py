import fastapi

from dcs_server_trigger import *
from fastapi.middleware import Middleware
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = fastapi.FastAPI()



valid_api_keys = []

with open("api_keys.txt", "r") as f:
    for line in f:
        valid_api_keys.append(line.strip())

class Shutdown(BaseModel):
    action: str
    api_key: str

class Test(BaseModel):
    action: str
    api_key: str



@app.post("/api/v1/dcs_shutdown")
async def dcs_status(item: Shutdown):
    if item.api_key == valid_api_keys[0]:
        
        if item.action == "shutdown":
            dcs_server_stop()
            return {"message": "Shutting down..."}
        else:
            return {"message": "Error"}
    else:
        return {"message": "Error"}

@app.post("/test")
async def test(item: Test):
    if item.api_key == valid_api_keys[0]:
        if item.action == "test":
            return {"message": "Its working"}
        else:
            return {"message": "Error"}
    else:
        return {"message": "Error"}