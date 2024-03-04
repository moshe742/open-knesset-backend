from pydantic import BaseModel
from decimal import Decimal


class LobbyistClients(BaseModel):
    LobbyistID: int = 242
    ClientID: int = 4
    Name: str = "Abbvie"
    ClientsNames: str = "Abbvie- ייצוג קבוע"


class Lobbyist(BaseModel):
    LobbyistID: int = 879
    IdentityNumber: str = "029723319"
    FullName: str = "אביב ברנט"
    PermitTypeValue: str = "שדלן זמני"
    Key: Decimal = "2.0"
    CorporationName: str = "שדלן עצמאי"
    IsIndependent: bool = 'true'
    CorpNumber: Decimal = "512065194.0"
    PracticeFramework: str | None = "תאגידים / גופים אחרים"
    IsMemberInFaction: str | None = 'הליכוד'
    MemberInFaction: bool = 'true'
