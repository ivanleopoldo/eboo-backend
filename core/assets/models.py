from pydantic import BaseModel

class Keywords(BaseModel):
    keywords: str
class URL(BaseModel):
    url: str
    source: str

class Plugin(BaseModel):
    plugin_name: str

class EmailAccount(BaseModel):
    email: str
    password: str
class Settings(BaseModel):
    emailacc: EmailAccount
    
