import time
import os
import worker_proxy_utils
from injectable import load_injection_container
load_injection_container()
load_injection_container(str(os.path.dirname(worker_proxy_utils.__file__)))
from fastapi import FastAPI, Request
from interceptors_schedule.interceptor_schedule_get import InterceptorScheduleGet
from interceptors_forward.interceptor_forward_get import InterceptorForwardGet

app = FastAPI()
interceptor_forward_get = InterceptorForwardGet()
interceptor_schedule_get = InterceptorScheduleGet()
rabbit_host = 'localhost'
rabbit_port = 5672

@app.middleware("http")
async def intercept(request: Request, call_next):
    new_base_url = 'http://0.0.0.0:7001/'
    if request.method == 'GET':
        return interceptor_schedule_get.intercept(rabbit_host, rabbit_port, request)
    else:
        raise RuntimeError("Unsupported operation!")
