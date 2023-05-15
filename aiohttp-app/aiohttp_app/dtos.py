from pydantic import BaseModel


class InputObjectDTO(BaseModel):
    name: str
