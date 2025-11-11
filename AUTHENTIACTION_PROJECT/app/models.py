from pydantic import BaseModel
from typing import Optional

class item(BaseModel):
    id:Optional[int]= None
    descriptiom:Optional[str]= None