from pydantic import BaseModel


class InputObjectDTO(BaseModel):
    name: str


class InputScheduleDTO(BaseModel):
    delay: int
    message: str


class OutputObjectDTO(BaseModel):
    id: int
    name: str
