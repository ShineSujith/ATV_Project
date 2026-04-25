from pydantic import BaseModel

class TextInput(BaseModel):
    payload: str
