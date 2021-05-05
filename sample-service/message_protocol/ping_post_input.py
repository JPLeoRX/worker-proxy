from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class PingPostInput(BaseModel):
    text: str

    def __init__(self, text: str) -> None:
        super().__init__(text=text)
