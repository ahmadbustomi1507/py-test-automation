## this is just an example
from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict,Field


class User(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        strict=True,
        validate_return=True,
    )

    id: str = Field(min_length=1)
    createdAt: str
    name: str
    avatar: str
    test:str = None

    #Optional equal to Union[...,None[
    # time: Optional[datetime]
    # friends: List[Union[int,str]] = []
