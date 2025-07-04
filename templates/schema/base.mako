<%!
def to_class_name(name):
    parts = name.lower().replace('-', '_').split('_')
    return ''.join(word.capitalize() for word in parts)

def to_snake_case(name):
    return name.lower().replace('-', '_')

def to_title_case(name):
    return name.replace('_', ' ').replace('-', ' ').title()
%>
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

class ${to_class_name(name)}BaseSchema(BaseModel):
    """Base schema for ${to_title_case(name)}"""
    # Add base fields here
    # Example:
    # name: str = Field(..., description="Name of the ${to_snake_case(name)}")
    # description: Optional[str] = Field(None, description="Description")
    
    model_config = ConfigDict(from_attributes=True) 