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

class ${to_class_name(name)}ResponseSchema(BaseModel):
    """Response schema for ${to_title_case(name)}"""
    id: int = Field(..., description="Unique identifier")
    # Add response fields here
    # Example:
    # name: str = Field(..., description="Name of the ${to_snake_case(name)}")
    # created_at: Optional[str] = Field(None, description="Creation timestamp")
    
    model_config = ConfigDict(from_attributes=True) 