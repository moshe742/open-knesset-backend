from pydantic import BaseModel
from datetime import datetime
from pydantic import HttpUrl


class KnsBillUnion(BaseModel):
    BillUnionID: int = 1
    MainBillID: int = 31252
    UnionBillID: int = 37664
    LastUpdatedDate: datetime = "2015-03-20T12:03:33"


class KnsBillSplit(BaseModel):
    BillSplitID: int = 1
    MainBillID: int = 258446
    SplitBillID: int = 262881
    Name: str = "הצעת חוק אזור סחר חופשי באילת (פטורים והנחות ממסים) (תיקון), התשס\"ח-2007"
    LastUpdatedDate: datetime = "2015-03-20T12:03:32"


class KnsBillInitiator(BaseModel):
    BillInitiatorID: int = 1
    BillID: int = 29803
    PersonID: int = 1047
    IsInitiator: bool = 'true'
    Ordinal: int = 7
    LastUpdatedDate: datetime = "2015-03-20T12:03:24"


class KnsBillName(BaseModel):
    BillNameID: int = 1
    BillID: int = 135664
    Name: str = "הצעת חוק בתי דין רבניים (קיום פסקי דין של גירושין) (תיקון - הרחבת אמצעי האכיפה כנגד סרבן גט), התשס\"ו-2006"
    NameHistoryTypeID: int = 5201
    NameHistoryTypeDesc: str = "בקריאה הראשונה"
    LastUpdatedDate: datetime = "2007-06-24T11:51:36"


class KnsDocumentBill(BaseModel):
    DocumentBillID: int = 75133
    BillID: int = 17689
    GroupTypeID: int = 15
    GroupTypeDesc: str = "קטע מדברי הכנסת"
    ApplicationID: int = 1
    ApplicationDesc: str = "DOC"
    FilePath: HttpUrl = "https://fs.knesset.gov.il//16/law/16_ls_ptk_73614.doc"
    LastUpdatedDate: datetime = "2010-06-02T21:14:42"


class KnsBillAirflow(BaseModel):
    BillID: int = 5
    KnessetNum: int = 1
    Name: str = "חוק שכר חברי הכנסת, התש\\ט-1949"
    SubTypeID: int = 55
    SubTypeDesc: str = "ועדה"
    PrivateNumber: int | None = 1449
    CommitteeID: int | None = 377
    StatusID: int | None = 118
    Number: int | None = 61
    PostponementReasonID: int | None = 2505
    PostponementReasonDesc: str | None = 'הסרה מסד"י בד. מוקדם'
    PublicationDate: datetime | None = "1949-06-07T00:00:00"
    MagazineNumber: int | None = 10
    PageNumber: int | None = 41
    IsContinuationBill: bool | None = 'true'
    SummaryLaw: str | None = (
        'החוק קובע כי המוסד לביטוח לאומי יפרסם באתר האינטרנט שלו, '
        'בתחילת כל שנה קלנדרית, את החגים שלפניהם יוקדם תשלום הגמלה לזכאים, '
        'את הגמלאות שתשלומן יוקדם, ואת המועד שבו תשולם הגמלה לפני החג.'
    )
    PublicationSeriesID: int | None = 6071
    PublicationSeriesDesc: str | None = "ספר החוקים"
    PublicationSeriesFirstCall: str | None = 'הצ"ח הכנסת (מתשס"ג 10/2002) - 74 ,מיום 16:00:00'
    LastUpdatedDate: datetime | None = "2022-11-17T11:08:23"


class KnsBillHistoryInitiator(BaseModel):
    BillHistoryInitiatorID: int = 1
    BillID: int = 403285
    PersonID: int = 557
    IsInitiator: bool = "true"
    StartDate: datetime | None = "2010-12-09T00:00:00"
    EndDate: datetime = "2012-12-09T00:00:00"
    ReasonID: int = 1204
    ReasonDesc: str = "חדל להיות חבר כנסת"
    LastUpdatedDate: datetime = "2015-03-20T12:03:30"


class KnsBill(BaseModel):
    BillID: int = 5
    KnessetNum: int = 1
    Name: str = "חוק שכר חברי הכנסת, התש\\ט-1949"
    SubTypeID: int = 55
    SubTypeDesc: str = "ועדה"
    PrivateNumber: int | None = 1449
    CommitteeID: int | None = 377
    StatusID: int | None = 118
    Number: int | None = 61
    PostponementReasonID: int | None = 2505
    PostponementReasonDesc: str | None = 'הסרה מסד"י בד. מוקדם'
    PublicationDate: datetime | None = "1949-06-07T00:00:00"
    MagazineNumber: int | None = 10
    PageNumber: int | None = 41
    IsContinuationBill: bool | None = 'true'
    SummaryLaw: str | None = (
        'החוק קובע כי המוסד לביטוח לאומי יפרסם באתר האינטרנט שלו, '
        'בתחילת כל שנה קלנדרית, את החגים שלפניהם יוקדם תשלום הגמלה לזכאים, '
        'את הגמלאות שתשלומן יוקדם, ואת המועד שבו תשולם הגמלה לפני החג.'
    )
    PublicationSeriesID: int | None = 6071
    PublicationSeriesDesc: str | None = "ספר החוקים"
    PublicationSeriesFirstCall: str | None = 'הצ"ח הכנסת (מתשס"ג 10/2002) - 74 ,מיום 16:00:00'
    LastUpdatedDate: datetime | None = "2022-11-17T11:08:23"
