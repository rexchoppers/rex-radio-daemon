from typing import Union, List

from beanie import Document

class Configuration(Document):
    field: str
    value: Union[str, List[str]]