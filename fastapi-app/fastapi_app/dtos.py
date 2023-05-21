from pydantic import BaseModel


class InputObjectDTO(BaseModel):
    name: str


class OutputObjectDTO(BaseModel):
    id: int
    name: str
