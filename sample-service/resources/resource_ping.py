from fastapi import APIRouter
from message_protocol.ping_get_output import PingGetOutput
from message_protocol.ping_post_input import PingPostInput
from message_protocol.ping_post_output import PingPostOutput
from utils.utils_id import UtilsId

router_ping = APIRouter()

utils_id = UtilsId()


@router_ping.get("/ping", response_model=PingGetOutput)
def ping_get() -> PingGetOutput:
    return PingGetOutput(utils_id.generate_uuid(), True)


@router_ping.post("/ping", response_model=PingPostOutput)
def ping_post(input: PingPostInput) -> PingPostOutput:
    return PingPostOutput(utils_id.generate_uuid(), True, input.text)
