from datetime import datetime
from pydantic import BaseModel
from datetime import datetime

class KnsGovministry(BaseModel):
    GovMinistryID: int = 490
    Name: str =  "אין נתונים"
    IsActive: bool = 'false'
    LastUpdatedDate: datetime = "2019-12-31T14:45:32"

class KnsKnessetDates(BaseModel):
    KnessetDateID: int = 1
    KnessetNum: int = 13
    Name: str = "השלוש-עשרה"
    Assembly: int = 1
    Plenum: int = 2
    PlenumStart: datetime = "1992-10-26T00:00:00"
    PlenumFinish: datetime | None = "1993-03-24T00:00:00"
    IsCurrent: bool = 'false'

class KnsStatus(BaseModel):
    StatusID: int = 6
    Desc: str = "בטיפול המשרד הנשאל"
    TypeID: int = 1
    TypeDesc: str = "שאילתה"
    OrderTransition: int | None = None
    IsActive: bool | None = 'true'
    LastUpdatedDate: datetime = "2013-10-06T14:08:19"

class KnsItemtype(BaseModel):
    ItemTypeID: int = 1
    Desc: str = "שאילתה"
    TableName: str | None = "KNS_Query"
      