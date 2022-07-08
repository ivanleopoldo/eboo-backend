from pydantic import BaseModel

class Keywords(BaseModel):
    keywords: str


class URL(BaseModel):
    url: str
    path: str


class Plugin(BaseModel):
    plugin_name: str
    
