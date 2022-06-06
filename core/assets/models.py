from pydantic import BaseModel

class Keywords(BaseModel):
    keywords: str

class URL(BaseModel):
    url: str
    source: str