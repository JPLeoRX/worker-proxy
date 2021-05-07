from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class ProxyChannel(BaseModel):
    id: str
    request_channel: str
    response_channel: str

    def __init__(self, id: str, request_channel: str, response_channel: str) -> None:
        super().__init__(id=id, request_channel=request_channel, response_channel=response_channel)
