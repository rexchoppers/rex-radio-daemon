from pydantic import BaseModel

class Configuration(BaseModel):
    # Radio Station Name
    name: str