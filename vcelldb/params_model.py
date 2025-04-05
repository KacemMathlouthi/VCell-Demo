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


class QueryParams(BaseModel, use_enum_values=True):
    bmName: Optional[str] = None
    bmId: Optional[str] = None
    category: Optional[CategoryEnum] = CategoryEnum.all
    owner: Optional[str] = None
    savedLow: Optional[str] = None
    savedHigh: Optional[str] = None
    startRow: Optional[int] = 1
    maxRows: Optional[int] = 10
    orderBy: Optional[OrderByEnum] = OrderByEnum.date_desc