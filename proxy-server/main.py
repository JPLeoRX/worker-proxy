import os
import worker_proxy_utils
from injectable import load_injection_container
from worker_proxy_utils import UtilsEnv

load_injection_container()
load_injection_container(str(os.path.dirname(worker_proxy_utils.__file__)))
from fastapi import FastAPI, Request
from interceptor import Interceptor

app = FastAPI()
utils_env = UtilsEnv()
interceptor = Interceptor()


@app.middleware("http")
async def intercept(request: Request, call_next):
    return await interceptor.intercept(utils_env.get_rabbitmq_config(), request)
