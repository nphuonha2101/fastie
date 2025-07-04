<%!
def to_class_name(name):
    parts = name.lower().replace('-', '_').split('_')
    return ''.join(word.capitalize() for word in parts)

def to_snake_case(name):
    return name.lower().replace('-', '_')

def get_table_name(name):
    """Generate table name from model name"""
    return f"{to_snake_case(name)}s"

def generate_field_definition(field_name, field_type):
    """Generate SQLAlchemy field definition"""
    field_type_lower = field_type.lower()
    
    if field_type_lower in ['str', 'string']:
        return f"    {field_name} = Column(String(255), nullable=False)"
    elif field_type_lower in ['int', 'integer']:
        return f"    {field_name} = Column(Integer, nullable=False)"
    elif field_type_lower in ['bool', 'boolean']:
        return f"    {field_name} = Column(Boolean, default=True)"
    elif field_type_lower == 'text':
        return f"    {field_name} = Column(Text, nullable=True)"
    elif field_type_lower == 'datetime':
        return f"    {field_name} = Column(DateTime, nullable=True)"
    else:
        return f"    {field_name} = Column(String(255), nullable=False)  # {field_type}"
%>
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from app.models.abstract_model import AbstractModel
from typing import Optional
from pydantic import BaseModel

class ${to_class_name(name)}(AbstractModel):
    __tablename__ = '${get_table_name(name)}'
    
    def get_response_model(self) -> Optional[BaseModel]:
        return None

% if fields:
% for field in fields.split(','):
% if ':' in field:
<%
    field_name, field_type = field.split(':')
    field_definition = generate_field_definition(field_name.strip(), field_type.strip())
%>
${field_definition}
% endif
% endfor
% else:
    # Add your model fields here
    # name = Column(String(100), nullable=False)
    # email = Column(String(255), nullable=False)
    # is_active = Column(Boolean, default=True)
% endif 