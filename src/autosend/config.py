from pydantic import BaseModel

class Settings(BaseModel):
    name: str
    api_id: str
    api_hash: str
    phone_number: str

