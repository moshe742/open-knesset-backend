from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union, Dict
from datetime import datetime
from datetime import date as dt
from datetime import time

class Member(BaseModel):
    mk_individual_id: int = 14
    mk_individual_first_name: str = "זאב בנימין"
    mk_individual_name: str = "בגין"
    PersonID: int = 2178
    GenderID: int = 251
    GenderDesc: str = "זכר"
    IsCurrent: bool = "false"
    mk_individual_email: str| None = None
    altnames: List[str] = [
      "זאב בנימין בגין",
      "בינימין בגין",
      "בנימין בגין"
    ]
    committee_positions: List[Dict[str, Union[int, str, dt, None]]] |  List[None] = [
      {
        "mk_individual_id": 14,
        "committee_id": 932,
        "committee_name": "ועדת החוקה, חוק ומשפט",
        "position_id": 42,
        "position_name": "חבר ועדה",
        "start_date": "2015-06-01",
        "finish_date": "2019-04-30",
        "knesset": 20
      }
    ]
    factions: List[Dict[str, Union[int, str, dt, None]]] |  List[None]= [
      {
        "mk_individual_id": 14,
        "faction_id": 882,
        "faction_name": "הליכוד",
        "start_date": "2015-03-31",
        "finish_date": "2019-04-30",
        "knesset": 20
      }
    ]
    faction_chairpersons: List[Dict[str, Union[int, str, dt, None]]] | List[None]= [
      {
        "faction_name":"סיעת יהדות התורה",
        "finish_date":"2023-01-23",
        "knesset":25,
        "mk_individual_id":35,
        "faction_id":1101,
        "start_date":"2022-11-15"
      }
    ]
    govministries: List[Dict[str, Union[int, str, dt, None]]] |  List[None]= [
      {
        "mk_individual_id": 14,
        "govministry_id": 28,
        "govministry_name": "משרד ראש הממשלה",
        "position_id": 39,
        "position_name": "שר",
        "start_date": "2015-05-14",
        "finish_date": "2015-06-01",
        "knesset": 20
      }
    ]
class MemberAttendedCommitteeMeetings(BaseModel):
    CommitteeSessionID: int = 64541
    KnessetNum: int = 16
    TypeID: int = 161
    TypeDesc: str = "פתוחה"
    CommitteeID: int = 26
    Location: str | None= "חדר הוועדה, באגף הוועדות (קדמה), קומה 1, חדר 1750",
    SessionUrl: HttpUrl = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesAgenda.aspx?Tab=3&ItemID=64541",
    BroadcastUrl: HttpUrl| None = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesBroadcast.aspx?TopicID=1576"
    StartDate: datetime = "2003-03-24T12:00:00"
    FinishDate: datetime| None = "2003-03-24T23:59:00"
    Note: str | None = "חדר הוועדה, קומה 2-, באגף החדש"
    topics: List[str]| None =[
      "בחירת יושב ראש הוועדה לביקורת המדינה"
    ]
    committee_name: str = "ועדת העלייה, הקליטה והתפוצות"
    bill_names: List[str] = [
      "חוק המדיניות הכלכלית לשנת הכספים 2004 (תיקוני חקיקה), התשס\"ד-2004"
    ]
    bill_types: List[str] = [
      "ממשלתית"
    ]
    related_to_legislation: bool = 'false'

class MemberVote(BaseModel):
    knesset_num: int =  16
    session_id: int =  15797
    sess_item_id: int =  16060
    sess_item_dscr: str | None =  "הודעת ראש הממשלה על פעילות הממשלה בתקופה שחלפה ועל תוכניותיה למושב הקרוב"
    vote_item_id: int =  905
    vote_item_dscr: str | None =  "הצעת סיכום"
    vote_date: dt =  "2003-10-20"
    vote_time: time | None = "20:08"
    is_elctrnc_vote: int =  1
    is_accepted: int =  0
    total_for: int =  13
    total_against: int =  54
    total_abstain: int =  11
    mk_vote: str = "abstain"

class MemberBill(BaseModel):
    BillID: int = 86915
    KnessetNum: int = 16
    Name: str = "חוק שוויון זכויות לאנשים עם מוגבלות (תיקון מס' 2), התשס\"ה-2005"
    SubTypeID: Optional[int] = 54
    SubTypeDesc: Optional[str] = "פרטית"
    PrivateNumber: Optional[int] =  775
    CommitteeID: Optional[int] =  28
    StatusID: Optional[int] =  118
    Number: Optional[int] =  2951
    PostponementReasonID: Optional[int] =  None
    PostponementReasonDesc: Optional[str] = None
    PublicationDate: Optional[datetime] = "2005-04-07T00:00:00"
    MagazineNumber: Optional[int] =  1995
    PageNumber: Optional[int] =  288
    IsContinuationBill: Optional[bool] = True
    SummaryLaw: Optional[str] = None
    PublicationSeriesID: Optional[int] =  6071
    PublicationSeriesDesc: Optional[str] =  "ספר החוקים"
    PublicationSeriesFirstCall: Optional[str] = None
    IsInitiator: Optional[bool] = True

class MemberPresence(BaseModel):
    mk_id: int = 214
    mk_name: str = "אביגדור ליברמן"
    date: dt = "2024-01-01"
    year: int = 2024
    month: int = 1
    day: int = 1
    year_week_number: int = 1
    total_attended_hours : int = 7
