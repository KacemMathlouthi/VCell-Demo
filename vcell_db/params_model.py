from typing import Optional
from pydantic import BaseModel
from enum import Enum

class CategoryEnum(str, Enum):
    all = "all"
    public = "public"
    shared = "shared"
    tutorials = "tutorials"
    educational = "educational"


class OrderByEnum(str, Enum):
    date_desc = "date_desc"
    date_asc = "date_asc"
    name_desc = "name_desc"
    name_asc = "name_asc"


class QueryParams(BaseModel):
    bmName: Optional[str]
    bmId: Optional[str]
    category: Optional[CategoryEnum]
    owner: Optional[str]
    savedLow: Optional[str]
    savedHigh: Optional[str]
    startRow: Optional[int]
    maxRows: Optional[int]
    orderBy: Optional[OrderByEnum]