from datetime import datetime
from pydantic import BaseModel,Field
from typing import Dict, List, Literal, Optional, Union
from datetime import date
from datetime import time
from datetime import datetime
from pydantic import HttpUrl
from models.enums.enums import FileType

class KnsDocumentCommitteeSessionDataservice(BaseModel):
    DocumentCommitteeSessionID: int = 71335
    CommitteeSessionID: int = 66045
    GroupTypeID: int = 23
    GroupTypeDesc: str = "פרוטוקול ועדה"
    ApplicationID: int = 1
    ApplicationDesc: str = "DOC"
    FilePath: HttpUrl = "https://fs.knesset.gov.il//16/Committees/16_ptv_71308.doc"
    LastUpdatedDate: datetime = "2010-06-02T20:32:33"

class KnsJointCommittee(BaseModel):
    JointCommitteeID: int = 1
    CommitteeID: int = 37
    ParticipantCommitteeID: int = 21
    LastUpdatedDate: datetime = "2015-03-20T12:02:57"

class KnsCommitteeAirflow(BaseModel):
    CommitteeID:  int = 1
    Name: str = "ועדת הכנסת"
    CategoryID: int | None = 1
    CategoryDesc: str | None = "ועדת הכנסת"
    KnessetNum: int | None = 15
    CommitteeTypeID: int | None = 70
    CommitteeTypeDesc: str | None = "ועדת הכנסת"
    Email: str | None = "vadatk@knesset.gov.il"
    StartDate: datetime = "1999-06-07T00:00:00"
    FinishDate: datetime | None = "2001-06-07T00:00:00"
    AdditionalTypeID: int | None = 991
    AdditionalTypeDesc: str | None = "קבועה"
    ParentCommitteeID: int | None = 39
    CommitteeParentName: str | None = "ועדת החקירה בנושא איתור והשבת נכסים של נספי השואה"
    IsCurrent: bool = "true"
    LastUpdatedDate: datetime = "2017-04-24T16:47:06"

class BuildMeetings(BaseModel):
    CommitteeSessionID: int = 64529
    Number: int | None = 460
    KnessetNum: int = 16
    TypeID: int = 161
    TypeDesc: str = "פתוחה"
    CommitteeID: int = 29
    Location: str | None = "חדר הוועדה, באגף הוועדות (קדמה), קומה 2, חדר 2740"
    SessionUrl: HttpUrl = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesAgenda.aspx?Tab=3&ItemID=64529"
    BroadcastUrl: HttpUrl | None = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesBroadcast.aspx?TopicID=1576"
    StartDate: datetime = "2003-03-12T10:30:00"
    FinishDate: datetime | None = "2003-03-12T23:59:00"
    Note: str | None = "חדר הוועדה, קומה 2-, באגף החדש"
    LastUpdatedDate: datetime = "2017-06-13T15:44:21"
    protocol_extension: str | None = ".doc"
    text_filename: str | None = "files/6/4/64529.txt"
    parts_filename: str | None = "files/6/4/64529.csv"
    topics: List[str] | None =[
      "בחירת יושב ראש הוועדה לביקורת המדינה"
    ],
    mks: List[str] = [
        " יולי אדלשטיין",
        "אברהם בורג",
        "רשף חן",
        "אליעזר כהן",
        "אתי לבני",
        "גדעון סער"
    ]
    invitees: List[Dict[str,str]] = [
        {"name":"פרופ' שלמה סלונים"},
        {"name":"פרופ' אריאל בנדור, דיקאן הפקולטה למשפטים, אוניברסיטת חיפה"},
        {"name":"פרופ' זאב סגל, בית הספר לממשל, מדעי החברה, אוניברסיטת תל-אביב"},
    ]
    legal_advisors: List[str] = [
        " אתי בנדלר",
        " הלית ברק"
    ]
    manager: List[str] = [
        "וילמה מאור"
    ]
    attended_mk_individual_ids: List[int] = [
        212,
        61
    ]

class DocumentBackgroundMaterialTitles(BaseModel):
    DocumentCommitteeSessionID: int = 0
    CommitteeSessionID: int = 64776
    CommitteeID: int = 25
    FilePath: HttpUrl = "https://fs.knesset.gov.il/\\16\\Committees\\16_cs_bg_339777.pdf"
    title: str = "חומר רקע - חוקי יסוד-1.6.03-רקע"

class JoinedMeetings(BaseModel):
    CommitteeSessionID: int = 64515
    Number: int | None = 2
    KnessetNum: int = 16
    TypeID: int = 161
    TypeDesc: str = "פתוחה"
    CommitteeID: int = 22
    Location: str | None = "חדר הוועדה, באגף הוועדות (קדמה), קומה 2, חדר 2750"
    SessionUrl: HttpUrl = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesAgenda.aspx?Tab=3&ItemID=64515"
    BroadcastUrl: HttpUrl | None = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesBroadcast.aspx?TopicID=12416"
    StartDate: datetime = "2003-02-25T10:30:00"
    FinishDate: datetime | None = "2005-02-25T10:30:00"
    Note: str | None = "הישיבה בהשתתפות שר החינוך"
    LastUpdatedDate: datetime = "2012-09-19T15:27:32"
    protocol_extension: str | None = ".doc"
    text_filename: str | None = "files/3/6/365775.txt"
    parts_filename: str | None = "files/3/6/365775.csv"
    topics: List[str] | None = [
        "העסקת קטינות על מסלול הדוגמנות"
    ]

class KnsCmtSitecode(BaseModel):
    CmtSiteCode: int = 1
    KnsID: int = 1
    SiteId: int = 1

class MeetingProtocolsParts(BaseModel):
    DocumentCommitteeSessionID: int = 71333
    CommitteeSessionID: int = 65782
    GroupTypeID: int = 23
    GroupTypeDesc: str = "פרוטוקול ועדה"
    ApplicationID: int = 1
    ApplicationDesc: FileType = "DOC"
    FilePath: HttpUrl = "http://fs.knesset.gov.il//16/Committees/16_ptv_71307.doc"
    LastUpdatedDate: datetime = "2010-06-02T20:32:33"
    KnessetNum: int = 16
    protocol_extension: str | None = ".doc"
    parsed_filename: str | None = "files/6/5/65782.csv"
    filesize: int | None = 82050
    crc32c: str | None = "LLmkqg=="
    error: str | None = None

class BuildRenderedMeetingsStats(BaseModel):
    CommitteeSessionID: int = 64529
    num_speech_parts: int = 7

class KnsDocumentCommitteeSession(BaseModel):
    DocumentCommitteeSessionID: int = 138775
    CommitteeSessionID: int = 311813
    GroupTypeID: int = 23
    GroupTypeDesc: str = "פרוטוקול ועדה"
    ApplicationID: int = 1
    ApplicationDesc: str = "DOC"
    FilePath: HttpUrl = "https://fs.knesset.gov.il//17/Committees/17_ptv_137257.doc"
    LastUpdatedDate: datetime = "2010-06-03T10:09:32"
    download_filename: str = "files/23/1/3/138775.DOC"
    download_filesize: int = 43008
    download_crc32c: str = "rPCcdg=="
    download_error: str = None
    text_protocol_extension: str = ".doc"
    text_parsed_filename: str = "files/3/1/311813.txt"
    text_filesize: int = 6128
    text_crc32c: str = "F0QTJw=="
    text_error:  str = None
    parts_protocol_extension: str = ".doc"
    parts_parsed_filename: str = "files/3/1/311813.csv"
    parts_filesize: int = 6123
    parts_crc32c: str = "b/YY6w=="
    parts_error:  str = None

class KnsCmtSessionItem(BaseModel):
    CmtSessionItemID: int = 28006
    ItemID: int = 74814
    CommitteeSessionID: int = 64516
    Ordinal: int | None = 20
    StatusID: int | None = 108
    Name: str | None = "שינויים בתקציב לשנת 2003"
    ItemTypeID: int | None = 11
    LastUpdatedDate: datetime = "2012-09-20T22:23:49"

class KnsCommitteeSession(BaseModel):
    CommitteeSessionID: int = 64515
    Number: int = 460
    KnessetNum: int = 16
    TypeID: int = 161
    TypeDesc: str = "פתוחה"
    CommitteeID: int = 22
    Location: str = "חדר הוועדה, באגף הוועדות (קדמה), קומה 2, חדר 2750"
    SessionUrl: HttpUrl = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesAgenda.aspx?Tab=3&ItemID=64515"
    BroadcastUrl: HttpUrl = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesBroadcast.aspx?TopicID=1576"
    StartDate: datetime = "2003-02-25T10:30:00"
    FinishDate: datetime = "2005-02-25T10:30:00"
    Note: str = "חדר הוועדה, קומה 2-, באגף החדש"
    LastUpdatedDate: datetime = "2012-09-19T15:27:32"
    download_crc32c: str = "owAZHg=="
    download_filename: str = "files/23/4/7/475281.DOC"
    download_filesize: int = 83913
    parts_crc32c: str = "54N8hg=="
    parts_filesize: int = 157418
    parts_parsed_filename: str = "files/6/4/64516.csv"
    text_crc32c: str = "l58eRw=="
    text_filesize: int= 157991
    text_parsed_filename: str = "files/6/4/64516.txt"
    item_ids: List[int] = [
        74814,
        74813,
        73285,
        73284,
        74812,
        74811,
        74810
    ]
    item_type_ids: List[int] = [ 
        11,
        11,
        11,
        11,
        11,
        11,
        11
    ]
    topics: List[str] = [
      "שינויים בתקציב לשנת 2003",
      "בחירת יו\"ר לועדה הזמנית",
      "תקנות התקשורת (בזק ושידורים)(חישוב תשלומים בעד שירותי בזק והצמדתם)(תיקון), התשס\"ג - 2003",
      "תקנות התקשורת (בזק ושידורים)(תשלומים בעד שירותי בזק המפורטים בתוספת לחוק)(תיקון מס' 2), התשס\"ג - 2003",
      "צו תעריף המכס והפטורים ומס קניה על טובין (תיקון מס' 115), התשס\"ג - 2003",
      "צו תעריף המכס והפטורים ומס קניה על טובין (הוראת שעה)(מס' 3), התשס\"ג - 2003 (פסיפס מקרמיקה וזכוכית)",
      "צו תעריף המכס והפטורים ומס קניה על טובין (תיקון מס' 110), התשס\"ג - 2002 (דגים שנדוגו ע\"י ספינות דייג ישראליות)"
    ]
    committee_name: str = "ועדת החוץ והביטחון"
    bill_names: List[str] = [
        "חוק הגנה על עובדים בשעת חירום (הוראת שעה), התשס\"ג-2003"
    ]
    bill_types: List[str] = [
        "ממשלתית"
    ]
    related_to_legislation: bool = "false"


class DocumentCommitteeSessionsParsing(BaseModel):
    DocumentCommitteeSessionID: int = 71333
    CommitteeSessionID: int = 65782
    GroupTypeID: int = 23
    GroupTypeDesc: str = "פרוטוקול ועדה"
    ApplicationID: int = 1
    ApplicationDesc: FileType = "DOC"
    FilePath: HttpUrl = "http://fs.knesset.gov.il//16/Committees/16_ptv_71307.doc"
    LastUpdatedDate: datetime = "2010-06-02T20:32:33"
    KnessetNum: int = 16

class DownloadDocumentCommitteeSession(BaseModel):
    DocumentCommitteeSessionID: int = 71333
    CommitteeSessionID: int = 65782
    GroupTypeID: int = 23
    GroupTypeDesc: str = "פרוטוקול ועדה"
    ApplicationID: int | None = 1
    ApplicationDesc: FileType = "DOC"
    FilePath: HttpUrl | None = "http://fs.knesset.gov.il//16/Committees/16_ptv_71307.doc"
    LastUpdatedDate: datetime = "2010-06-02T20:32:33"
    KnessetNum: int | None = 16
    filename: str | None = "files/23/7/1/71333.DOC"
    filesize: int | None = 190976
    crc32c: str | None = "UqP16Q=="
    error: str | None = None

class MeetingProtocolsText(BaseModel):
    DocumentCommitteeSessionID: int = 71333
    CommitteeSessionID: int = 65782
    GroupTypeID: int = 23
    GroupTypeDesc: str = "פרוטוקול ועדה"
    ApplicationID: int = 1
    ApplicationDesc: FileType = "DOC"
    FilePath: HttpUrl | None = "http://fs.knesset.gov.il//16/Committees/16_ptv_71307.doc"
    LastUpdatedDate: datetime = "2010-06-02T20:32:33"
    KnessetNum: int | None = 16
    protocol_extension: str  | None=  ".doc"
    parsed_filename: str  | None= "files/6/5/65782.txt"
    filesize: int | None = 82413
    crc32c: str | None = "56WyDA=="
    error: str | None = None

class KnsCommittee(BaseModel):
    CommitteeID: int = 1
    Name: str = "ועדת הכנסת"
    CategoryID: int | None = 1
    CategoryDesc: str | None = "ועדת הכנסת"
    KnessetNum: int | None = 15
    CommitteeTypeID: int | None = 70
    CommitteeTypeDesc: str | None = "ועדת הכנסת"
    Email: str | None = "vadatk@knesset.gov.il"
    StartDate: datetime | None = "1999-06-07T00:00:00"
    FinishDate: datetime = "2001-06-07T00:00:00"
    AdditionalTypeID: int | None = 991
    AdditionalTypeDesc: str | None = "קבועה"
    ParentCommitteeID: int | None = 39
    CommitteeParentName: str | None = "ועדת החקירה בנושא איתור והשבת נכסים של נספי השואה"
    IsCurrent: bool = "true"
    LastUpdatedDate: datetime = "2017-04-24T16:47:06"





    
