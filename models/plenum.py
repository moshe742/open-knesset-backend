from pydantic import BaseModel
from datetime import datetime
from models.enums.enums import FileType


class DocumentPlenumSession(BaseModel):
    DocumentPlenumSessionID: int = 128869
    PlenumSessionID: int = 129232
    GroupTypeID: int = 30
    GroupTypeDesc: str = "תוכן עניינים"
    ApplicationID: int = 1
    ApplicationDesc: FileType = "DOC"
    FilePath: str = "https://fs.knesset.gov.il//16/Plenum/16_toc_128869.DOC"
    LastUpdatedDate: datetime = "2010-06-03T06:55:10"


class PlenumSession(BaseModel):
    PlenumSessionID: int = 9626
    Number: int = 1
    KnessetNum: int = 16
    Name: str = "ישיבת מליאה בתאריך 17/02/2003 בשעה 16:00"
    StartDate: datetime = "2003-02-17T16:00:00"
    FinishDate: datetime | None = "2003-02-17T17:03:00"
    IsSpecialMeeting: bool = 'false'
    LastUpdatedDate: datetime = "2023-07-06T12:45:23"


class PlmSessionItem(BaseModel):
    plmPlenumSessionID: int = 3365
    ItemID: int = 9632
    PlenumSessionID: int = 9630
    ItemTypeID: int = 9
    ItemTypeDesc: str = "פריטי מליאה"
    Ordinal: int = 1
    Name: str = "דברים לזכרם של חברי הכנסת לשעבר שמעון גרידי ודוד שטרן, זכרונם לברכה"
    StatusID: int | None = 305
    IsDiscussion: int = 1
    LastUpdatedDate: datetime = "2023-07-06T12:45:23"
