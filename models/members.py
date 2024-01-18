from datetime import datetime
from pydantic import BaseModel
from typing import List, Literal
from datetime import date as dt
from datetime import datetime
from pydantic import HttpUrl

class FactionChairpersons(BaseModel):
    mk_individual_id: int = 915
    faction_id: int = 1102
    faction_name: str = "סיעת יש עתיד"
    start_date: dt = "16/10/23"
    finish_date: dt | None = '24/10/23'
    knesset: int = 25

class Govministries(BaseModel):
    mk_individual_id: int = 915
    govministry_id: int = 1
    govministry_name: str = "בלי תיק"
    position_id: int = 39
    position_name: str = "שר"
    start_date: dt = "16/10/23"
    finish_date: dt | None = '24/10/23'
    knesset: int = 25

class MembersPresence(BaseModel):
    mk_id: int = 790
    mk_name: str = "יצחק אהרונוביץ'"
    date: dt= "05/07/10"
    year: int = 2010
    month: int = 7
    day: int = 5
    year_week_number: int = 27
    total_attended_hours: int = 8
    
class Committees(BaseModel):
    mk_individual_id: int = 1097
    committee_id: int = 4228
    committee_name: str = "ועדת המשנה לביטחון, יחסי חוץ וקשרי מסחר בינלאומיים "
    position_id: int = 42
    position_name: str = "חבר ועדה"
    start_date: dt = "21/11/20"
    finish_date: dt | None = "23/10/21"
    knesset: int = 25

class PersonAirflow(BaseModel):
    PersonID: int = 405
    LastName: str = "ליברמן"
    FirstName: str = "אביגדור"
    GenderID: int = 251
    GenderDesc: str = "זכר"
    Email: str | None = 'aliberman@knesset.gov.il'
    IsCurrent: bool = 'true'
    LastUpdatedDate: datetime = "2015-03-20T12:03:08"


class Mksitecode(BaseModel):
    MKSiteCode: int = 1
    KnsID: int = 405
    SiteId: int = 12

class Person(BaseModel):
    PersonID: int = 405
    LastName: str = "ליברמן"
    FirstName: str = "אביגדור"
    GenderID: int = 251
    GenderDesc: str = "זכר"
    Email: str | None = 'aliberman@knesset.gov.il'
    IsCurrent: bool = 'true'
    LastUpdatedDate: datetime = "2015-03-20T12:03:08"

class Individual(BaseModel):
    mk_individual_id: int = 214
    mk_status_id: int = 0
    mk_individual_name: str = "ליברמן"
    mk_individual_name_eng: str | None = 'Liberman'
    mk_individual_first_name: str = "אביגדור"
    mk_individual_first_name_eng: str | None = 'Avigdor'
    mk_individual_email: str | None = "aliberman@knesset.gov.il"
    mk_individual_photo: HttpUrl = "https://oknesset.org/static/img/Male_portrait_placeholder_cropped.jpg"
    PersonID: int = 427
    LastName: str = "ליברמן"
    FirstName: str = "אביגדור"
    GenderID: int = 251
    GenderDesc: str = "זכר"
    Email: str | None = "aliberman@knesset.gov.il"
    IsCurrent: bool = 'true'
    LastUpdatedDate: datetime = "2022-11-10T11:19:09"
    altnames: List[str] = [
      "אביגדור ליברמן"
    ]

class Factions(BaseModel):
    id: int = 1082
    name: str = "דגל התורה"
    start_date: dt = "15/08/22"
    finish_date: dt | None = "15/11/22"
    knessets: List[int] = [
      24
    ]

class IndividualNames(BaseModel):
    mk_individual_id: int = 209
    names: List[str] = [
      "אליעזר כהן"
    ]

class FactionMemberships(BaseModel):
    faction_id: int = 1096
    faction_name: str = "סיעת הליכוד "
    start_date: dt = "16/10/23"
    finish_date: dt | None = "10/12/23"
    member_mk_ids: List[int] = [
      1,
      771,
      914,
      921,
      30772,
      953,
      826,
      828,
      69,
      1095,
      1098,
      1100,
      1101,
      974,
      976,
      1105,
      723,
      1109,
      1111,
      30809,
      90,
      987,
      1116,
      992,
      1122,
      1123,
      1124,
      1125,
      1002,
      1011,
      30711,
      1018
    ]
    knesset: int = 25

class PersonToPosition(BaseModel):
    PersonToPositionID: int = 379
    PersonID: int = 2605
    PositionID: int = 43
    KnessetNum: int | None = 2
    GovMinistryID: int | None = 28
    GovMinistryName: str = "משרד ראש הממשלה"
    DutyDesc: str | None = "שר המשפטים"
    FactionID: int | None = 638
    FactionName: str | None = 'אגודת ישראל'
    GovernmentNum: int | None = 29
    CommitteeID: int | None = 327
    CommitteeName: str | None = 'ועדת הכספים'
    StartDate: datetime = "1951-08-20T00:00:00"
    FinishDate: datetime | None = "1955-08-15T00:00:00"
    IsCurrent: bool = 'false'
    LastUpdatedDate: datetime = "2015-03-20T12:03:08"

class IndividualFactions(BaseModel):
    mk_individual_id: int = 30809
    faction_id: int = 1096
    faction_name: str = "סיעת הליכוד "
    start_date: dt = "15/10/20"
    finish_date: dt | None = "15/10/21"
    knesset: int = 23

class Position(BaseModel):
    PositionID: int = 29
    Description: str = "יושבת–ראש הקואליציה"
    GenderID: int = 250
    GenderDesc: Literal['זכר', 'נקבה'] = "נקבה"
    LastUpdatedDate: datetime = "2015-03-20T12:03:00"


