from typing import Optional
from pydantic import BaseModel,model_validator,ConfigDict
from datetime import datetime


class CreateBlog(BaseModel):
    title: str
    slug: str = ""
    content: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def generate_slug(cls, values):
        if isinstance(values, dict) and 'title' in values:
            values["slug"] = values["title"].replace(" ", "-").lower()
        return values
    
class UpdateBlog(CreateBlog):
    pass
    
class ReadBlog(BaseModel):
    title: str
    content: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)