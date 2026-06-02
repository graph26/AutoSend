from pydantic import BaseModel, Field

class Settings(BaseModel):
    name: str = Field()
    api_id: str = Field()
    api_hash: str = Field()
    phone_number: str = Field()

