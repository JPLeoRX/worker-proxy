import os
import worker_proxy_utils
from injectable import load_injection_container
load_injection_container()
load_injection_container(str(os.path.dirname(worker_proxy_utils.__file__)))
from fastapi import FastAPI, Request
from interceptor import Interceptor

app = FastAPI()
interceptor = Interceptor()
rabbit_host = 'localhost'
rabbit_port = 5672

@app.middleware("http")
async def intercept(request: Request, call_next):
    return await interceptor.intercept('localhost', 5672, request)
