from pydantic import BaseModel
from datetime import datetime
from models.enums.enums import FileType
from pydantic import HttpUrl


class DocumentLaw(BaseModel):
    DocumentLawID: int = 311000
    LawID: int = 2001482
    GroupTypeID: int = 9
    GroupTypeDesc: str = "חוק - פרסום ברשומות"
    ApplicationID: int = 3
    ApplicationDesc: FileType = "PPT"
    FilePath: HttpUrl = "https://fs.knesset.gov.il//2/law/2_lsr_311000.PDF"
    LastUpdatedDate: datetime = "2015-06-29T15:31:18"


class IsraelLaw(BaseModel):
    IsraelLawID: int = 2000001
    KnessetNum: int = 1
    Name: str = "חוק רשות הפיתוח (העברת נכסים), התש\"י-1950"
    IsBasicLaw: bool = 'false'
    IsFavoriteLaw: bool = 'false'
    IsBudgetLaw: bool | None = 'false'
    PublicationDate: datetime | None = "1950-08-09T00:00:00"
    LatestPublicationDate: datetime | None = "1960-07-29T00:00:00"
    LawValidityID: int | None = 6079
    LawValidityDesc: str | None = "תקף"
    ValidityStartDate: datetime | None = "1959-04-19T00:00:00"
    ValidityStartDateNotes: str | None = "תחילתו של חוק זה ביום שתיכון הממשלה לאחר הבחירות לכנסת השש עשרה"
    ValidityFinishDate: datetime | None = "1969-04-14T00:00:00"
    ValidityFinishDateNotes: str | None = "כל הפקודה הוחלפה על-ידי חוק העונשין למעט סעיף 38 לפקודה שנותר בתוקף"
    LastUpdatedDate: datetime | None = "2015-06-29T15:31:18"


class IsraelLawBinding(BaseModel):
    IsraelLawBinding: int = 1
    IsraelLawID: int = 2002363
    IsraelLawReplacedID: int = 2001409
    LawID: int = 569596
    LawTypeID: int = 2
    LastUpdatedDate: datetime = "2016-05-25T14:10:03"


class IsraelLawMinistry(BaseModel):
    LawMinistryID: int = 2135419
    IsraelLawID: int = 2000001
    GovMinistryID: int = 16
    LastUpdatedDate: datetime = "2014-09-10T14:27:17"


class KnsLaw(BaseModel):
    LawID: int = 2001427
    TypeID: int = 6002
    TypeDesc: str = "חוק בן חיצוני"
    SubTypeID: int = 6043
    SubTypeDesc: str = "מנדטורי"
    KnessetNum: int | None = 4
    Name: str | None = "דבר המלך על הטיס במושבות (הטלת חוקים), 1937"
    PublicationDate: datetime | None = "1937-07-29T00:00:00"
    PublicationSeriesID: int | None = 6078
    PublicationSeriesDesc: str | None = "עיתון רשמי מנדטורי"
    MagazineNumber: str | None = "תוס' 2 - 707"
    PageNumber: str | None = "תוס' 2 - 707"
    LastUpdatedDate: datetime | None = "2019-07-02T09:42:20"


class IsraelLawName(BaseModel):
    IsraelLawNameID: int = 1
    IsraelLawID: int = 2000001
    LawID: int = 148560
    LawTypeID: int = 2
    Name: str = "חוק רשות הפיתוח (העברת נכסים), התש\"י-1950"
    LastUpdatedDate: datetime = "2016-05-09T15:40:21"


class LawBinding(BaseModel):
    LawBindingID: int = 41555
    LawID: int = 148560
    LawTypeID: int = 2
    IsraelLawID: int = 2000001
    ParentLawID: int = 2000001
    LawParentTypeID: int = 6003
    BindingType: int = 6012
    BindingTypeDesc: str = "החוק המקורי"
    PageNumber: str = "278"
    AmendmentType: int = 6010
    AmendmentTypeDesc: str = "ישיר"
    LastUpdatedDate: datetime = "2014-09-10T14:27:13"


class IsraelLawClassification(BaseModel):
    LawClassificiationID: int = 1
    IsraelLawID: int = 2000001
    ClassificiationID: int = 23
    ClassificiationDesc: str = "מקרקעין"
    LastUpdatedDate: datetime = "2015-01-15T15:59:55"
