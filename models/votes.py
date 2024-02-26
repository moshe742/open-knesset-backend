from pydantic import BaseModel
from typing import List
from datetime import date as dt
from datetime import time
from models.enums.enums import ResultTypeNameEnum, ResultTypeIDEnum


class ViewVoteRsltsHdrApproved(BaseModel):
    id: int = 8
    knesset_num: int = 16
    session_id: int = 15797
    sess_item_nbr: int = 2
    sess_item_id: int = 16060
    sess_item_dscr: str = "הודעת ראש הממשלה על פעילות הממשלה בתקופה שחלפה ועל תוכניותיה למושב הקרוב"
    vote_item_id: int = 905
    vote_item_dscr: str = "הצעת סיכום"
    vote_date: dt = "20/10/03"
    vote_time: time = "20:08"
    is_elctrnc_vote: int = 1
    vote_type: int = 1
    is_accepted: int = 0
    total_for: int = 13
    total_against: int = 54
    total_abstain: int = 11
    vote_stat: int = 1
    session_num: int = 58
    vote_nbr_in_sess: int = 8
    reason: int = 4
    modifier: str = "Unknown"
    remark: str | None = "הצעתו של חבר הכנסת אפי איתם"


class VoteRsltsKmmbrShadowExtra(BaseModel):
    vote_id: int = 94
    kmmbr_id: str = "000000405"
    kmmbr_name: str = "בנימין אלון"
    vote_result: int = 1
    knesset_num: int = 16
    faction_id: int = 45
    faction_name: str = "האיחוד הלאומי-ישראל ביתנו"
    reason: int | None = 5
    modifier: str | None = "Unknown"
    remark: str | None = "הצבעה ידנית"
    result_type_name: str = "בעד"
    mk_individual_id: int = 12


class ViewVoteMkIndividual(BaseModel):
    vip_id: str = "000000405"
    mk_individual_id: int = 12
    mk_individual_name: str = "אלון"
    mk_individual_name_eng: str = "Elon"
    mk_individual_first_name: str = "בנימין"
    mk_individual_first_name_eng: str = "Benyamin"


class VoteRsltsKmmbrShadow(BaseModel):
    vote_id: int = 94
    kmmbr_id: str = "000000405"
    kmmbr_name: str = "בנימין אלון"
    vote_result: int = 1
    knesset_num: int = 16
    faction_id: int = 45
    faction_name: str = "האיחוד הלאומי-ישראל ביתנו"
    reason: int | None = 5
    modifier: str | None = "Unknown"
    remark: str | None = "הצבעה ידנית"


class ViewVoteRsltsHdrApprovedExtra(BaseModel):
    id: int = 8
    knesset_num: int = 16
    session_id: int = 15797
    sess_item_nbr: int = 2
    sess_item_id: int = 16060
    sess_item_dscr: str = "הודעת ראש הממשלה על פעילות הממשלה בתקופה שחלפה ועל תוכניותיה למושב הקרוב"
    vote_item_id: int = 905
    vote_item_dscr: str = "הצעת סיכום"
    vote_date: dt = "20/10/03"
    vote_time: time = "20:08"
    is_elctrnc_vote: int = 1
    vote_type: int = 1
    is_accepted: int = 0
    total_for: int = 13
    total_against: int = 54
    total_abstain: int = 11
    vote_stat: int = 1
    session_num: int = 58
    vote_nbr_in_sess: int = 8
    reason: int = 4
    modifier: str = "Unknown"
    remark: str | None = "הצעתו של חבר הכנסת אפי איתם"
    mk_ids_pro: List[int] = [
        704,
        137,
        104,
        201,
        126,
        197,
        218,
        13,
        36,
        29,
        208,
        697,
        756
    ]
    mk_ids_against: List[int] = [
        209,
        751,
        3,
        92
    ]
    mk_ids_abstain: List[int] = [
        220,
        100,
        115,
        65,
        739,
        5
    ]
    knesset: int = 16
    plenum: int = 2
    assembly: int = 1
    pagra: bool = "false"


class VoteResultType(BaseModel):
    result_type_id: ResultTypeIDEnum = ResultTypeIDEnum.CANCELED
    result_type_name: ResultTypeNameEnum = ResultTypeNameEnum.CANCELED
