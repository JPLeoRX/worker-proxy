from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class ProxyChannel(BaseModel):
    id: str
    request_id: str
    response_id: str

    def __init__(self, id: str, request_id: str, response_id: str) -> None:
        super().__init__(id=id, request_id=request_id, response_id=response_id)
