from pydantic import BaseModel
from typing import List, Union


class KnessetMemberByIndividual(BaseModel):
    mk_individual_id: int = 214
    FirstName: str = "אביגדור"
    LastName: str = "ליברמן"
    GenderDesc: str = "זכר"
    Email: str | None = "aliberman@knesset.gov.il"
    altnames: List[str] = ["אביגדור ליברמן"]
    mk_individual_photo: str | None = "https://oknesset.org/static/img/Male_portrait_placeholder_cropped.jpg"
    mk_individual_photo: str | None = "https://oknesset.org/static/img/Male_portrait_placeholder_cropped.jpg"
    faction_name: str = "ישראל ביתנו בראשות אביגדור ליברמן"
    IsChairPerson: bool = True
    knessets: str = "15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25"
    committees: List[Union[None,
                           str]] = ["הוועדה לפיקוח על הקרן לאזרחי ישראל (חבר ועדה)",
                                    "ועדת הכלכלה (חבר ועדה)",
                                    "ועדת המשנה לקידום תעשיית ההייטק (חבר ועדה)",
                                    "ועדת המשנה לקידום תעשיית ההייטק (יו\"ר ועדה)"]
    year_total_hours_attended: str = "[2010-86,2011-219,2012-185,2013-1252,2014-270,2015-699,2016-586,2019-437,2020-688,2021-434,2022-222,2023-818]"


class KnessetMemberByPersonal(BaseModel):
    PersonID: int = 427
    PersonID: int = 427
    FirstName: str = "אביגדור"
    LastName: str = "ליברמן"
    GenderDesc: str = "זכר"
    Email: str | None = "aliberman@knesset.gov.il"
    Email: str | None = "aliberman@knesset.gov.il"
    altnames: List[str] = ["אביגדור ליברמן"]
    mk_individual_photo: str | None = "https://oknesset.org/static/img/Male_portrait_placeholder_cropped.jpg"
    mk_individual_photo: str | None = "https://oknesset.org/static/img/Male_portrait_placeholder_cropped.jpg"
    faction_name: str = "ישראל ביתנו בראשות אביגדור ליברמן"
    IsChairPerson: bool = True
    knessets: str = "15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25"
    committees: List[Union[None,
                           str]] = ["הוועדה לפיקוח על הקרן לאזרחי ישראל (חבר ועדה)",
                                    "ועדת הכלכלה (חבר ועדה)",
                                    "ועדת המשנה לקידום תעשיית ההייטק (חבר ועדה)",
                                    "ועדת המשנה לקידום תעשיית ההייטק (יו\"ר ועדה)"]
    year_total_hours_attended: str = "[2010-86,2011-219,2012-185,2013-1252,2014-270,2015-699,2016-586,2019-437,2020-688,2021-434,2022-222,2023-818]"
