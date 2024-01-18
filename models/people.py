from datetime import datetime
from pydantic import BaseModel
from typing import Dict, List, Literal, Union
from datetime import datetime
from pydantic import HttpUrl

class PlenumSessionVotersStats(BaseModel):
    knesset: int = 16
    plenum: int = 1
    assembly: int = 1
    pagra: int = 0
    faction_id: int = 53
    mk_id: int = 1
    voted_sessions: int = 0
    total_sessions: int = 10
    voted_sessions_percent: int = 0

class CommitteesJoinedMeetings(BaseModel):
    CommitteeSessionID: int = 64516
    Number: int = 2
    KnessetNum: int = 16
    TypeID: int = 161
    TypeDesc: str = "פתוחה"
    CommitteeID: int = 21
    Location: str | None = "חדר הוועדה, באגף הוועדות (קדמה), קומה 3, חדר 3750"
    SessionUrl: HttpUrl = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesAgenda.aspx?Tab=3&ItemID=64516"
    BroadcastUrl: HttpUrl | None = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesBroadcast.aspx?TopicID=12416"
    StartDate: datetime = "2003-02-24T10:00:00"
    FinishDate: datetime | None = "2005-02-24T10:00:00"
    Note: str | None = "דיון בסעיף 49, בדבר פתיחת התחרות בתחום התקשורת הנייחת"
    LastUpdatedDate: datetime = "2012-09-19T15:27:32"
    text_file_name: str | None = "data/committees/meeting_protocols_text/files/6/4/64529.txt"
    text_file_size: int | None = 482
    topics: List[str] = [
      "שינויים בתקציב לשנת 2003",
      "בחירת יו\"ר לועדה הזמנית",
      "תקנות התקשורת (בזק ושידורים)(חישוב תשלומים בעד שירותי בזק והצמדתם)(תיקון), התשס\"ג - 2003",
      "תקנות התקשורת (בזק ושידורים)(תשלומים בעד שירותי בזק המפורטים בתוספת לחוק)(תיקון מס' 2), התשס\"ג - 2003",
      "צו תעריף המכס והפטורים ומס קניה על טובין (תיקון מס' 115), התשס\"ג - 2003",
      "צו תעריף המכס והפטורים ומס קניה על טובין (הוראת שעה)(מס' 3), התשס\"ג - 2003 (פסיפס מקרמיקה וזכוכית)",
      "צו תעריף המכס והפטורים ומס קניה על טובין (תיקון מס' 110), התשס\"ג - 2002 (דגים שנדוגו ע\"י ספינות דייג ישראליות)"
    ]

class CommitteesMeetingAttendees(BaseModel):
    CommitteeSessionID: int = 64516
    Number: int = 2
    KnessetNum: int = 16
    TypeID: int = 161
    TypeDesc: str = "פתוחה"
    CommitteeID: int = 21
    Location: str | None = "חדר הוועדה, באגף הוועדות (קדמה), קומה 3, חדר 3750"
    SessionUrl: HttpUrl = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesAgenda.aspx?Tab=3&ItemID=64516"
    BroadcastUrl: HttpUrl | None = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesBroadcast.aspx?TopicID=12416"
    StartDate: datetime = "2003-02-24T10:00:00"
    FinishDate: datetime | None = "2005-02-24T10:00:00"
    Note: str | None = "דיון בסעיף 49, בדבר פתיחת התחרות בתחום התקשורת הנייחת"
    LastUpdatedDate: datetime = "2019-05-16T11:33:28"
    download_crc32c: str | None = "owAZHg=="
    download_filename: str | None = "files/23/4/7/475281.DOC"
    download_filesize: int | None = 83913
    parts_crc32c: str | None = "54N8hg=="
    parts_filesize: int | None = 157418
    parts_parsed_filename: str | None = "files/6/4/64516.csv"
    text_crc32c: str | None = "l58eRw=="
    text_filesize: int | None = 157991
    text_parsed_filename: str | None = "files/6/4/64516.txt"
    item_ids: List[int] | None = [
      74814,
      74813,
      73285,
      73284,
      74812,
      74811,
      74810
    ],
    item_type_ids: List[int] | None = [
      11,
      11,
      11,
      11,
      11,
      11,
      11
    ],
    topics: List[str] | None = [
      "שינויים בתקציב לשנת 2003",
      "בחירת יו\"ר לועדה הזמנית",
      "תקנות התקשורת (בזק ושידורים)(חישוב תשלומים בעד שירותי בזק והצמדתם)(תיקון), התשס\"ג - 2003",
      "תקנות התקשורת (בזק ושידורים)(תשלומים בעד שירותי בזק המפורטים בתוספת לחוק)(תיקון מס' 2), התשס\"ג - 2003",
      "צו תעריף המכס והפטורים ומס קניה על טובין (תיקון מס' 115), התשס\"ג - 2003",
      "צו תעריף המכס והפטורים ומס קניה על טובין (הוראת שעה)(מס' 3), התשס\"ג - 2003 (פסיפס מקרמיקה וזכוכית)",
      "צו תעריף המכס והפטורים ומס קניה על טובין (תיקון מס' 110), התשס\"ג - 2002 (דגים שנדוגו ע\"י ספינות דייג ישראליות)"
    ],
    committee_name: str | None =  "ועדת הכספים"
    bill_names: List[str] = [
        "חוק שירות המילואים, התשס\"ח-2008",
        "הצעת חוק המילואים, התשס\"ו-2006"
    ]
    bill_types: List[str] = [
        "ממשלתית",
        "פרטית"
    ]
    related_to_legislation: bool | None = 'true'
    mks: List[str] | None = [
      "ישראל כץ - היו\"ר",
      "רוחמה אברהם",
      "זבולון אורלב",
      "אברהם בייגה שוחט",
      "שלום שמחון"
    ],
    invitees: List[Dict[str, str]] | None = [
      {
        "name": "אורטל מינקוביץ-ראש ענף פיקוח תקציבי, החשב הכללי, משרד האוצר"
      },
      {
        "name": "גיא אבן-רפרנט שיכון, אגף התקציבים, משרד האוצר"
      },
    ]
    legal_advisors: List[str] | None = [
      "שגית אפיק",
      "אנה שניידר",
      "מירב אלבז (מתמחה)"
    ]
    manager: List[str] | None = [
      "טמיר כהן"
    ]
    financial_advisors: List[str] | None = [
      "סמדר אלחנני"
    ]
    attended_mk_individual_ids: List[int] = [
      64,
      123,
      92
    ]

class PartyDisciplineStats(BaseModel):
    knesset: int = 16
    plenum: int = 2
    assembly: int = 1
    pagra: int = 0
    faction_id: int = 24
    mk_id: int = 1
    undisciplined_votes: int = 0
    disciplined_votes: int = 112
    total_votes: int = 961
    undisciplined_votes_percent: int = 0
    disciplined_votes_percent: int = 11

class CommitteesMeetingAttendeesMksFullStats(BaseModel):
    knesset: int = 16
    plenum: int = 1
    assembly: int = 1
    pagra: int = 0
    committee_id: int = 21
    faction_id: int = 53
    mk_id: int = 1
    attended_meetings: int = 0
    protocol_meetings: int = 1
    open_meetings: int = 1
    attended_meetings_percent: int = 0
    attended_meetings_relative_percent: int = 0

class CommitteesMeetingSpeakerStats(BaseModel):
    CommitteeSessionID: int = 100017
    parts_crc32c: str = "EIzyDg=="
    part_index: int = 0
    header: str = "סדר היום"
    body_length: int = 214
    body_num_words: int = 25
    part_categories: str = "משפטן"
    name_role: str = 'עו"ד יאיר שילה - יועמ"ש, המועצה להסדר ההימורים בספורט '
    mk_individual_id: int = 1
    mk_individual_faction: str = 'התאחדות הספרדים שומרי תורה - תנועת ש"ס'

class PlenumSessionVoters(BaseModel):
    PlenumSessionID: int = 9626
    Number: int = 1
    KnessetNum: int = 16
    Name: str = "ישיבת מליאה בתאריך 17/02/2003 בשעה: 16:00"
    StartDate: datetime = "2003-02-17T16:00:00"
    FinishDate: datetime | None = "2004-02-17T16:00:00"
    IsSpecialMeeting: bool = "false"
    LastUpdatedDate: datetime = "2013-10-03T16:21:47"
    voter_mk_ids: List[int] | None = [
        65,3,100,197,36,5,13,206,208,752,756,757,727,732
    ]

class MkVotedAgainstMajority(BaseModel):
    vote_id: int = 10
    mk_id: int = 114
    faction_id: int = 24
    vote_knesset: int = 16
    vote_plenum: int = 2
    vote_assembly: int = 1
    vote_pagra: bool = 'false'
    vote_datetime: datetime = '2003-10-20T20:09:00'
    vote_majority: str = 'against'
    voted_against_majority: bool = 'false'

class MkPartyDisciplineKnesset20(BaseModel):
    vote_id: int = 31582
    vote_url: HttpUrl = 'http://www.knesset.gov.il/vote/heb/Vote_Res_Map.asp?vote_id_t=31582'
    vote_datetime: datetime = '2018-12-31T15:27:00'
    vote_knesset: int = 20
    vote_plenum: int = 5
    vote_assembly: int = 1
    vote_pagra: bool = 'false'
    mk_id: int = 868
    mk_name: str = 'יעל גרמן'
    faction_id: int = 904
    faction_name: str = 'יש עתיד'
    vote_majority: str = 'pro'

class CommitteesMeetingAttendeesMksStats(BaseModel):
    knesset_num: int = 16
    committee_id: int = 21
    committee_name: str = 'ועדת הכספים'
    meeting_start_date: datetime = '2003-02-24T10:00:00'
    meeting_topics: str = "'שינויים בתקציב לשנת 2003, בחירת יו\ר לועדה הזמנית, תקנות התקשורת (בזק ושידורים)(חישוב תשלומים בעד שירותי בזק והצמדתם)(תיקון), התשס\ג - 2003, תקנות התקשורת (בזק ושידורים)(תשלומים בעד שירותי בזק המפורטים בתוספת לחוק)(תיקון מס' 2), התשס\ג - 2003, צו תעריף המכס והפטורים ומס קניה על טובין (תיקון מס' 115), התשס\ג - 2003, צו תעריף המכס והפטורים ומס קניה על טובין (הוראת שעה)(מס' 3), התשס\ג - 2003 (פסיפס מקרמיקה וזכוכית), צו תעריף המכס והפטורים ומס קניה על טובין (תיקון מס' 110), התשס\ג - 2002 (דגים שנדוגו ע\י ספינות דייג ישראליות)"
    mk_id: int = 64
    mk_name: str = 'איתן כבל'
    mk_membership_committee_names: str = 'ועדת הכספים, ועדת הפנים ואיכות הסביבה'
    mk_faction_id: int = 24
    mk_faction_name: str = 'הליכוד'

class MembersJoinedMks(BaseModel):
    mk_individual_id: int = 1
    mk_status_id: int = 1
    mk_individual_name: str = 'אדלשטיין'
    mk_individual_name_eng: str | None = 'Edelstein'
    mk_individual_first_name: str = 'יולי יואל'
    mk_individual_first_name_eng: str | None = 'Yuli-Yoel'
    mk_individual_email: str | None = 'yedelstein@KNESSET.GOV.IL'
    mk_individual_photo: HttpUrl | None = 'http://fs.knesset.gov.il/globaldocs/MK/1/1_1_3_4.jpeg'
    PersonID: int = 532,
    LastName: str = 'אדלשטיין'
    FirstName: str = 'יולי יואל'
    GenderID: int = 251
    GenderDesc: Literal['זכר','נקבה'] = 'זכר'
    Email: str | None = 'yedelstein@knesset.gov.il'
    IsCurrent: bool = 'true'
    LastUpdatedDate: datetime = '2015-11-15T19:51:25'
    positions: List[Dict[str, Union[str, int, datetime]]] = [
      {
        'gender':'m',
        'position': 'סגן יו\ר הכנסת',
        'KnessetNum': 15,
        'start_date': '1999-09-14 00:00:00',
        'finish_date': '2001-03-12 00:00:00',
        'position_id': 70
      },
      {
        'gender':'m',
        'DutyDesc': 'שר ההסברה והתפוצות',
        'position':'שר',
        'KnessetNum': 18,
        'start_date':'2009-03-31 00:00:00',
        'finish_date': '2013-02-05 00:00:00',
        'position_id': 39,
        'GovMinistryID': 137,
        'GovernmentNum': 32,
        'GovMinistryName': 'ההסברה'
      },
      {
        'gender': 'm',
        'position': 'חבר ועדה',
        'KnessetNum': 16,
        'start_date': '2003-02-17 00:00:00',
        'CommitteeID': 72,
        'finish_date': '2006-04-17 00:00:00',
        'position_id': 42,
        'CommitteeName': 'לתיקונים בחוקי הבחירות'
      }
    ]
    altnames: List[str] = [
      'יואל אדלשטין',
      'יואל יולי אדלשטיין',
      'יולי אדלשטין',
      'יולי יואל אדלשטיין',
      'יואל אדלשטיין',
      'יולי - יואל אדלשטיין'
    ]

class CommitteesMeetingAttendeesMks(BaseModel):
    CommitteeSessionID: int = 64529
    Number: int | None = 67
    KnessetNum: int = 16
    TypeID: int = 161
    TypeDesc: str = 'פתוחה'
    CommitteeID: int | None = 29
    Location: str | None = 'חדר הוועדה, באגף הוועדות (קדמה), קומה 2, חדר 2740'
    SessionUrl: HttpUrl | None = 'http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesAgenda.aspx?Tab=3&ItemID=64529'
    BroadcastUrl: str | None = "http://main.knesset.gov.il/Activity/committees/Pages/AllCommitteesBroadcast.aspx?TopicID=12416"
    StartDate: datetime = '2003-03-12T10:30:00'
    FinishDate: datetime | None = '2003-03-12T23:59:00'
    Note: str | None = "דיון בסעיף 49, בדבר פתיחת התחרות בתחום התקשורת הנייחת"
    LastUpdatedDate: datetime = '2017-06-13T15:44:21'
    protocol_extension: str | None = '.doc'
    text_filename: str | None = 'files/6/4/64529.txt'
    parts_filename: str | None = 'files/6/4/64529.csv'
    topics: List[str] | None = [
      'בחירת יושב ראש הוועדה לביקורת המדינה'
    ],
    mks: List[str] = [
        " יולי אדלשטיין",
        "אברהם בורג",
        "רשף חן",
        "אליעזר כהן",
        "אתי לבני",
        "גדעון סער"
    ]
    invitees: List[Dict[str, str]] = [
        {"name":"פרופ' שלמה סלונים"},
        {"name":"פרופ' אריאל בנדור, דיקאן הפקולטה למשפטים, אוניברסיטת חיפה"},
        {"name":"פרופ' זאב סגל, בית הספר לממשל, מדעי החברה, אוניברסיטת תל-אביב"}
    ]
    legal_advisors: List[str] = [
        " אתי בנדלר",
        " הלית ברק"
    ]
    manager: List[str] = [
        "דורית ואג"
    ]