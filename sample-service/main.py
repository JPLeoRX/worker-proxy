from injectable import load_injection_container
load_injection_container()

from fastapi import FastAPI
from resources.resource_ping import router_ping

app = FastAPI()
app.include_router(router_ping)
