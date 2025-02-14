#db/base_class.py
import inflect
from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative
# Create an inflect engine
p = inflect.engine()
@as_declarative()
class Base:
            id: Any
            __name__: str