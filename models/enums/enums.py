from enum import Enum


class ResultTypeNameEnum(str, Enum):
    CANCELED = "בוטל"
    APPROVED = "בעד"
    AGAINST = "נגד"
    ABSTAINED = "נמנע"
    DID_NOT_VOTE = "לא הצביע"


class ResultTypeIDEnum(int, Enum):
    CANCELED = 0
    APPROVED = 1
    AGAINST = 2
    ABSTAINED = 3
    DID_NOT_VOTE = 4


class FileType(Enum):
    URL = "URL"
    PIC = "PIC"
    PDF = "PDF"
    VDO = "VDO"
    PPT = "PPT"
    DOC = "DOC"
