from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class PingGetOutput(BaseModel):
    id: str
    success: bool

    def __init__(self, id: str, success: bool) -> None:
        super().__init__(id=id, success=success)
