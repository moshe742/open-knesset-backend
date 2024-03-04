from pydantic import BaseModel, validator, ValidationError
from typing import List, Union


class MinisterByIndividual(BaseModel):
    mk_individual_id: int = 69
    FirstName: str = "ישראל"
    LastName: str = "כץ"
    GenderDesc: str = "זכר"
    Email: str = "yiskatz@knesset.gov.il"
    altnames: List[str] = ["ישראל כץ"]
    mk_individual_photo: str = "https://oknesset.org/static/img/Male_portrait_placeholder_cropped.jpg"
    faction_name: str = "הליכוד"
    ministers: str = "[משרד האנרגיה והתשתיות: שר]"
    IsChairPerson: bool = True
    knessets: str = "14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25"
    committees: List[Union[None, str]] = [None]
    year_total_hours_attended: str = "[2010-72, 2011-193, 2012-148, 2013-308, 2014-276, 2015-384, 2016-388, 2017-297, 2018-182, 2019-71, 2020-205, 2021-518, 2022-335, 2023-399]"


class MinisterByPersonal(BaseModel):
    PersonID: int = 468
    PersonID: int = 468
    FirstName: str = "ישראל"
    LastName: str = "כץ"
    GenderDesc: str = "זכר"
    Email: str = "yiskatz@knesset.gov.il"
    altnames: List[str] = ["ישראל כץ"]
    mk_individual_photo: str = "https://oknesset.org/static/img/Male_portrait_placeholder_cropped.jpg"
    faction_name: str = "הליכוד"
    ministers: str = "[משרד האנרגיה והתשתיות: שר]"
    IsChairPerson: bool = True
    knessets: str = "14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25"
    committees: List[Union[None, str]] = [None]
    year_total_hours_attended: str = "[2010-72, 2011-193, 2012-148, 2013-308, 2014-276, 2015-384, 2016-388, 2017-297, 2018-182, 2019-71, 2020-205, 2021-518, 2022-335, 2023-399]"
