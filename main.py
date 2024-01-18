from fastapi import FastAPI, HTTPException, status, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Union ,Optional, List
import models.current_minister as current_minister
import models.current_knesset_member as current_knesset_member
import models.user_friendly as user_friendly
import models.knesset as knesset
import models.plenum as plenum
import models.lobbyists as lobbyists
import models.laws as laws
import models.members as members
import models.people as people
import models.bills as bills
import models.committees as committees
import models.votes as votes

import errors

import api.db as DB

from api import queries as QUERY

from datetime import datetime
from datetime import date
from datetime import time


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['*']
)

    
# This endpoint, by default, returns details for current Knesset members only.
# If the 'is_current' parameter is set to false, 
# the endpoint returns details for all Knesset members across all time.
@app.get("/members", status_code=200,
         description = """By default returns only current knesset 
             members and all their details for the current knesset
             """,
         summary="""Get Knesset members and all their details 
             for some Knesset period""",
         response_model=List[user_friendly.Member],
         tags=['user friendly'])
async def get_members_list(
    knesset_num:Optional[int] = None,
    is_current:Optional[bool] = True,
):
    query = QUERY.get_members()
    data = DB.get_members(query,is_current,knesset_num)
    if isinstance(data, Exception):
        response_status = (status.HTTP_422_UNPROCESSABLE_ENTITY)
        raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data


# This endpoint, returns info about presence of some Knesset member.
@app.get("/members/{mk_individual_id}/presence", status_code=200,
         summary="""Get info about presence of some Knesset member""",
         response_model=List[user_friendly.MemberPresence],
         responses={
            404: errors.NO_DATA_FOUND_ERROR
         },
         tags=['user friendly'])
async def get_members_presence_list(
    mk_individual_id:int 
):
    query = QUERY.get_members_presence(mk_individual_id)
    data = DB.get_members_info(query,mk_individual_id)
    if isinstance(data, Exception):
        response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
        raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data


# This endpoint provides information about the attended committee 
# meetings of a Knesset member
@app.get("/members/{mk_individual_id}/attended_committee_meetings", 
         status_code=200,
         response_model=List[user_friendly.MemberAttendedCommitteeMeetings],
         summary="""Get info about the attended committee meetings of 
            a Knesset member""",
         responses={
            404: errors.NO_DATA_FOUND_ERROR
         },
         tags=['user friendly'])
async def get_members_attended_committee_meetings_list(
    mk_individual_id:int 
):
    query = QUERY.get_members_attended_committee_meetings(mk_individual_id)
    data = DB.get_members_info(query,mk_individual_id)
    if isinstance(data, Exception):
        response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
        raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data


# This endpoint provides information about 
# the votes of a Knesset member
@app.get("/members/{mk_individual_id}/votes", 
         status_code=200,
         summary="""Get info about the the votes of a Knesset member""",
         response_model=List[user_friendly.MemberVote],
         responses={
            404: errors.NO_DATA_FOUND_ERROR
         },
         tags=['user friendly'])
async def get_members_votes_list(
    mk_individual_id:int 
):
    query = QUERY.get_members_votes(mk_individual_id)
    data = DB.get_members_info(query,mk_individual_id)
    if isinstance(data, Exception):
        response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
        raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data
               

# This endpoint provides information about 
# the bills of a Knesset member
@app.get("/members/{mk_individual_id}/bills", 
         status_code=200,
         summary="""Get info about the the bills of a Knesset member""",
         response_model=List[user_friendly.MemberBill],
         responses={
            404: errors.NO_DATA_FOUND_ERROR
         },
         tags=['user friendly'])
async def get_members_votes_list(
    mk_individual_id:int 
):
    query = QUERY.get_members_bills(mk_individual_id)
    data = DB.get_members_info(query,mk_individual_id)
    if isinstance(data, Exception):
        response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
        raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data
           

# Route for list"bills_kns_billunion" table
@app.get("/bills_kns_billunion/list", 
         status_code=200,
         response_model=List[bills.KnsBillunion],
         responses={422: errors.LIMIT_ERROR},
         tags=['bills'])
async def get_billunion_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    MainBillID: Optional[int] = None,
    UnionBillID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billunion"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception): 
        response_status = (status.HTTP_422_UNPROCESSABLE_ENTITY
                           if isinstance(data,ValueError)
                           else status.HTTP_404_NOT_FOUND)
        raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "bills_kns_billunion" table
@app.get('/bills_kns_billunion/{BillUnionID}',
         response_model=bills.KnsBillunion,
         responses={
            404: errors.NO_DATA_FOUND_ERROR
         },
         tags=['bills'],
         )
async def get_bill_union(BillUnionID: int):
    data = DB.get_single_data('bills_kns_billunion', 'BillUnionID',
                              BillUnionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list knesset_kns_govministry table
@app.get("/knesset_kns_govministry/list", status_code=200,
         response_model=List[knesset.KnsGovministry],
         responses={422: errors.LIMIT_ERROR},
         tags=["knesset"])
async def get_govministry_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Name: Optional[str] = None,
    IsActive: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM knesset_kns_govministry"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "knesset_kns_govministry" table
@app.get('/knesset_kns_govministry/{GovMinistryID}',
         response_model=knesset.KnsGovministry,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["knesset"])
async def get_gov_ministry(GovMinistryID: int):
    data = DB.get_single_data('knesset_kns_govministry',
                              'GovMinistryID', GovMinistryID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list plenum_kns_documentplenumsession table
@app.get("/plenum_kns_documentplenumsession/list", status_code=200,
         response_model=List[plenum.DocumentPlenumSession],
         responses={422: errors.LIMIT_ERROR},
         tags=["plenum"])
async def get_documentplenumsession_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    PlenumSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM plenum_kns_documentplenumsession"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "plenum_kns_documentplenumsession" table
@app.get('/plenum_kns_documentplenumsession/{DocumentPlenumSessionID}',
         response_model=plenum.DocumentPlenumSession,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["plenum"])
async def get_document_plenum_session(DocumentPlenumSessionID: int):
    data = DB.get_single_data('plenum_kns_documentplenumsession',
                              'DocumentPlenumSessionID',
                              DocumentPlenumSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_mk_individual_faction_chairpersons table
@app.get("/members_mk_individual_faction_chairpersons/list", 
         status_code=200,
         response_model=List[members.FactionChairpersons],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_faction_chairpersons_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_faction_chairpersons"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for "members_mk_individual_faction_chairpersons" table
@app.get('/members_mk_individual_faction_chairpersons/{mk_individual_id}',
         response_model=members.FactionChairpersons,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["members"])
async def get_faction_chairperson(mk_individual_id: int):
    data = DB.get_single_data('members_mk_individual_faction_chairpersons',
                              'mk_individual_id', mk_individual_id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_mk_individual_govministries table
@app.get("/members_mk_individual_govministries/list", 
         status_code=200,
         response_model=List[members.Govministries],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_individual_govministries_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    govministry_id: Optional[int] = None,
    govministry_name: Optional[str] = None,
    position_id: Optional[int] = None,
    position_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_govministries"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_mk_individual_govministries" table
@app.get('/members_mk_individual_govministries/{mk_individual_id}',
         response_model=members.Govministries,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["members"])
async def get_gov_ministry_member(mk_individual_id: int):
    data = DB.get_single_data('members_mk_individual_govministries',
                              'mk_individual_id', mk_individual_id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list bills_kns_billsplit table
@app.get("/bills_kns_billsplit/list", 
         status_code=200,
         response_model=List[bills.KnsBillsplit],
         responses={422: errors.LIMIT_ERROR},
         tags=["bills"])
async def get_billsplit_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    MainBillID: Optional[int] = None,
    SplitBillID: Optional[int] = None,
    Name: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billsplit"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for "bills_kns_billsplit" table
@app.get('/bills_kns_billsplit/{BillSplitID}',
          response_model=bills.KnsBillsplit,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["bills"])
async def get_bill_split(BillSplitID: int):
    data = DB.get_single_data('bills_kns_billsplit', 'BillSplitID',
                              BillSplitID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list bills_kns_billinitiator table
@app.get("/bills_kns_billinitiator/list", 
         status_code=200,
         response_model=List[bills.KnsBillInitiator],
         responses={422: errors.LIMIT_ERROR},
         tags=["bills"])
async def get_billinitiator_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    BillID: Optional[int] = None,
    PersonID: Optional[int] = None,
    IsInitiator: Optional[bool] = None,
    Ordinal: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billinitiator"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "bills_kns_billinitiator" table
@app.get('/bills_kns_billinitiator/{BillInitiatorID}',
          response_model=bills.KnsBillInitiator,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["bills"])
async def get_bill_initiator(BillInitiatorID: int):
    data = DB.get_single_data('bills_kns_billinitiator',
                              'BillInitiatorID', BillInitiatorID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_plenum_session_voters_stats table
@app.get("/people_plenum_session_voters_stats/list",
         status_code=200,
         responses={422: errors.LIMIT_ERROR},
         response_model=List[people.PlenumSessionVotersStats],
         tags=["people"])
async def get_voters_stats_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset: Optional[int] = None,
    plenum: Optional[int] = None,
    assembly: Optional[int] = None,
    pagra: Optional[int] = None,
    faction_id: Optional[int] = None,
    mk_id: Optional[int] = None,
    voted_sessions: Optional[int] = None,
    total_sessions: Optional[int] = None,
    voted_sessions_percent: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_plenum_session_voters_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list bills_kns_billname table
@app.get("/bills_kns_billname/list", 
         status_code=200,
         response_model=List[bills.KnsBillName],
         responses={422: errors.LIMIT_ERROR},
         tags=["bills"])
async def get_billname_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    BillID: Optional[int] = None,
    Name: Optional[str] = None,
    NameHistoryTypeID: Optional[int] = None,
    NameHistoryTypeDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billname"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_mk_individual_committees table
@app.get("/members_mk_individual_committees/list", 
         status_code=200,
         response_model=List[members.Committees],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_individual_committees_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_individual_id: Optional[int] = None,
    committee_id: Optional[int] = None,
    committee_name: Optional[str] = None,
    position_id: Optional[int] = None,
    position_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_committees"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list votes_view_vote_rslts_hdr_approved table
@app.get("/votes_view_vote_rslts_hdr_approved/list", 
         status_code=200,
         response_model=List[votes.ViewVoteRsltsHdrApproved],
         responses={422: errors.LIMIT_ERROR},
         tags=["votes"])
async def get_vote_rslts_hdr_approved_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset_num: Optional[int] = None,
    session_id: Optional[int] = None,
    sess_item_nbr: Optional[int] = None,
    sess_item_id: Optional[int] = None,
    sess_item_dscr: Optional[str] = None,
    vote_item_id: Optional[int] = None,
    vote_item_dscr: Optional[str] = None,
    vote_date: Optional[date] = None,
    vote_time: Optional[time] = None,
    is_elctrnc_vote: Optional[int] = Query(None, ge=0, le=1),
    vote_type: Optional[int] = None,
    is_accepted: Optional[int] = None,
    total_for: Optional[int] = None,
    total_against: Optional[int] = None,
    total_abstain: Optional[int] = None,
    vote_stat: Optional[int] = None,
    session_num: Optional[int] = None,
    vote_nbr_in_sess: Optional[int] = None,
    reason: Optional[int] = None,
    modifier: Optional[str] = None,
    remark: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_view_vote_rslts_hdr_approved"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "votes_view_vote_rslts_hdr_approved" table
@app.get('/votes_view_vote_rslts_hdr_approved/{id}',
         response_model=votes.ViewVoteRsltsHdrApproved,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["votes"])
async def get_voter_result(id: int):
    data = DB.get_single_data('votes_view_vote_rslts_hdr_approved', 'id', id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_kns_documentcommitteesession_dataservice table
@app.get("/committees_kns_documentcommitteesession_dataservice/list",
         status_code=200,
         response_model=List[committees.KnsDocumentCommitteeSessionDataservice],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_documentcommitteesession_dataservice_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_documentcommitteesession_dataservice"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_kns_documentcommitteesession_dataservice" table
@app.get('/committees_kns_documentcommitteesession_dataservice/{DocumentCommitteeSessionID}',
         response_model=committees.KnsDocumentCommitteeSessionDataservice,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_document_committee_session(DocumentCommitteeSessionID: int):
    data = DB.get_single_data
    (
        'committees_kns_documentcommitteesession_dataservice',
        'DocumentCommitteeSessionID',
        DocumentCommitteeSessionID
    )
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_kns_jointcommittee table
@app.get("/committees_kns_jointcommittee/list",
         status_code=200,
         response_model=List[committees.KnsJointCommittee],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_jointcommittee_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    ParticipantCommitteeID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_jointcommittee"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_kns_jointcommittee" table
@app.get('/committees_kns_jointcommittee/{JointCommitteeID}',
         response_model=committees.KnsJointCommittee,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_joint_committee(JointCommitteeID: int):
    data = DB.get_single_data('committees_kns_jointcommittee',
                              'JointCommitteeID', JointCommitteeID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list votes_vote_rslts_kmmbr_shadow_extra table
@app.get("/votes_vote_rslts_kmmbr_shadow_extra/list",
         status_code=200,
         response_model=List[votes.VoteRsltsKmmbrShadowExtra],
         responses={422: errors.LIMIT_ERROR},
         tags=["votes"])
async def get_vote_rslts_kmmbr_shadow_extra_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    vote_id: Optional[int] = None,
    kmmbr_id: Optional[int] = None,
    kmmbr_name: Optional[str] = None,
    vote_result: Optional[int] = None,
    knesset_num: Optional[int] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    reason: Optional[int] = None,
    modifier: Optional[str] = None,
    remark: Optional[str] = None,
    result_type_name: Optional[str] = None,
    mk_individual_id: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_vote_rslts_kmmbr_shadow_extra"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list plenum_kns_plenumsession table
@app.get("/plenum_kns_plenumsession/list",
         response_model=List[plenum.PlenumSession],
         status_code=200,
         responses={422: errors.LIMIT_ERROR},
         tags=["plenum"])
async def get_plenumsession_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    PlenumSessionID: Optional[int] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    IsSpecialMeeting: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM plenum_kns_plenumsession"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for "plenum_kns_plenumsession" table
@app.get('/bills_kns_plenumsession/{PlenumSessionID}',
         response_model=plenum.PlenumSession,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["bills"])
async def get_plenum_session(PlenumSessionID: int):
    data = DB.get_single_data('plenum_kns_plenumsession',
                              'PlenumSessionID', PlenumSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list bills_kns_documentbill table
@app.get("/bills_kns_documentbill/list",
         status_code=200,
         response_model=List[bills.KnsDocumentBill],
         responses={422: errors.LIMIT_ERROR},
         tags=["bills"])
async def get_documentbill_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    BillID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_documentbill"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "bills_kns_documentbill" table
@app.get('/bills_kns_documentbill/{DocumentBillID}',
         response_model=bills.KnsDocumentBill,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["bills"])
async def get_document_bill(DocumentBillID: int):
    data = DB.get_single_data('bills_kns_documentbill',
                              'DocumentBillID', DocumentBillID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list bills_kns_bill__airflow table
@app.get("/bills_kns_bill__airflow/list",
         status_code=200,
         response_model=List[bills.KnsBillAirflow],
         responses={422: errors.LIMIT_ERROR},
         tags=["bills"])
async def get_bill__airflow_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    SubTypeID: Optional[int] = None,
    SubTypeDesc: Optional[str] = None,
    PrivateNumber: Optional[int] = None,
    CommitteeID: Optional[int] = None,
    StatusID: Optional[int] = None,
    Number: Optional[int] = None,
    PostponementReasonID: Optional[int] = None,
    PostponementReasonDesc: Optional[str] = None,
    PublicationDate: Optional[datetime] = None,
    MagazineNumber: Optional[int] = None,
    PageNumber: Optional[int] = None,
    IsContinuationBill: Optional[bool] = None,
    SummaryLaw: Optional[str] = None,
    PublicationSeriesID: Optional[int] = None,
    PublicationSeriesDesc: Optional[str] = None,
    PublicationSeriesFirstCall: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_bill__airflow"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "bills_kns_bill__airflow" table
@app.get('/bills_kns_bill__airflow/{BillID}',
          response_model=bills.KnsBillAirflow,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["bills"])
async def get_bill_airflow(BillID: int):
    data = DB.get_single_data('bills_kns_bill__airflow', 'BillID', BillID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_presence table
@app.get("/members_presence/list",
         status_code=200,
         response_model=List[members.MembersPresence],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_members_presence_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_id: Optional[int] = None,
    mk_name: Optional[str] = None,
    date: Optional[date] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    year_week_number: Optional[int] = None,
    total_attended_hours: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_presence"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_kns_committee__airflow table
@app.get("/committees_kns_committee__airflow/list",
         status_code=200,
         response_model=List[committees.KnsCommitteeAirflow],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_committee__airflow_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Name: Optional[str] = None,
    CategoryID: Optional[int] = None,
    CategoryDesc: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    CommitteeTypeID: Optional[int] = None,
    CommitteeTypeDesc: Optional[str] = None,
    Email: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    AdditionalTypeID: Optional[int] = None,
    AdditionalTypeDesc: Optional[str] = None,
    ParentCommitteeID: Optional[int] = None,
    CommitteeParentName: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_committee__airflow"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_kns_committee__airflow" table
@app.get('/committees_kns_committee__airflow/{CommitteeID}',
         response_model=committees.KnsCommitteeAirflow,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_single_data_airflow(CommitteeID: int):
    data = DB.get_single_data('committees_kns_committee__airflow',
                              'CommitteeID', CommitteeID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_build_build_meetings table
@app.get("/committees_build_build_meetings/list",
         status_code=200,
         response_model=List[committees.BuildMeetings],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_build_meetings_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    protocol_extension: Optional[str] = None,
    text_filename: Optional[str] = None,
    parts_filename: Optional[str] = None,
    topics: Optional[str] = None,
    mks: Optional[str] = None,
    invitees_name: Optional[str] = None,
    invitees_role: Optional[str] = None,
    legal_advisors: Optional[str] = None,
    manager: Optional[str] = None,
    attended_mk_individual_ids: List[int] = Query(
        [],
        alias="attended_mk_individual_ids",
        example=[736],
        list=True
    )
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val = [attended_mk_individual_ids]
    arrays_number_names = ["attended_mk_individual_ids"]
    arrays_val = [[topics], [mks], [legal_advisors], [manager]]
    arrays_name = ["topics", "mks", "legal_advisors", "manager"]
    objects_val = [invitees_name, invitees_role]
    objects_name = ["invitees_name", "invitees_role"]
    for key, value in query_params:
        if key in arrays_number_names:
            elemts = arrays_number_val[arrays_number_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by'] and \
                key not in arrays_name and \
                key not in objects_name:
            qs_parts.append(f"{key}={value}")

    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    for name, val in zip(objects_name, objects_val):
        if val:
            qs_parts.append(f"{name}=<{val}>")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_build_build_meetings"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_build_build_meetings" table
@app.get('/committees_build_build_meetings/{CommitteeSessionID}',
         response_model=committees.BuildMeetings,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_build_meeting(CommitteeSessionID: int):
    data = DB.get_single_data('committees_build_build_meetings',
                              'CommitteeSessionID', CommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_committees_joined_meetings table
@app.get("/people_committees_joined_meetings/list",
         status_code=200,
         response_model=List[people.CommitteesJoinedMeetings],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_people_committees_joined_meetings_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    text_file_name: Optional[str] = None,
    text_file_size: Optional[int] = None,
    topics: List[str] = Query(
        [],
        alias="topics",
        example=['שינויים בתקציב לשנת 2003'],
        list=True
    )
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays = [topics]
    var_names = ["topics"]
    for key, value in query_params:
        if key in var_names:
            elemts = arrays[var_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_joined_meetings"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "people_committees_joined_meetings" table
@app.get('/people_committees_joined_meetings/{CommitteeSessionID}',
          response_model=people.CommitteesJoinedMeetings,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["people"])
async def get_people_committees_joined_meeting(CommitteeSessionID: int):
    data = DB.get_single_data('people_committees_joined_meetings',
                              'CommitteeSessionID', CommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list bills_kns_billhistoryinitiator table
@app.get("/bills_kns_billhistoryinitiator/list",
         status_code=200,
         response_model=List[bills.KnsBillHistoryInitiator],
         responses={422: errors.LIMIT_ERROR},
         tags=["bills"])
async def get_billhistoryinitiator_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    BillID: Optional[int] = None,
    PersonID: Optional[int] = None,
    IsInitiator: Optional[bool] = None,
    StartDate: Optional[datetime] = None,
    EndDate: Optional[datetime] = None,
    ReasonID: Optional[int] = None,
    ReasonDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billhistoryinitiator"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "bills_kns_billhistoryinitiator" table
@app.get('/bills_kns_billhistoryinitiator/{BillHistoryInitiatorID}',
         response_model=bills.KnsBillHistoryInitiator,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["bills"])
async def get_bill_history_initiator(BillHistoryInitiatorID: int):
    data = DB.get_single_data('bills_kns_billhistoryinitiator',
                              'BillHistoryInitiatorID',
                              BillHistoryInitiatorID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_document_background_material_titles table
@app.get("/committees_document_background_material_titles/list",
         status_code=200,
         response_model=List[committees.DocumentBackgroundMaterialTitles],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_document_background_material_titles_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    CommitteeID: Optional[int] = None,
    FilePath: Optional[str] = None,
    title: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_document_background_material_titles"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_document_background_material_titles" table
@app.get(
    '/committees_document_background_material_titles/{DocumentCommitteeSessionID}',
    response_model=committees.DocumentBackgroundMaterialTitles,
    responses={
        404: errors.NO_DATA_FOUND_ERROR
    },
    tags=["committees"]
)
async def get_background_material_title(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_document_background_material_titles',
                              'DocumentCommitteeSessionID',
                              DocumentCommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_committees_meeting_attendees table
@app.get("/people_committees_meeting_attendees/list",
         status_code=200,
         response_model=List[people.CommitteesMeetingAttendees],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_committees_meeting_attendees_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    download_crc32c: Optional[str] = None,
    download_filename: Optional[str] = None,
    download_filesize: Optional[int] = None,
    parts_crc32c: Optional[str] = None,
    parts_filesize: Optional[int] = None,
    parts_parsed_filename: Optional[str] = None,
    text_crc32c: Optional[str] = None,
    text_filesize: Optional[int] = None,
    text_parsed_filename: Optional[str] = None,
    item_ids: List[int] = Query(
        [],
        alias="item_ids",
        example=[74814],
        list=True
    ),
    item_type_ids: List[int] = Query(
        [],
        alias="item_type_ids",
        example=[11],
        list=True
    ),
    topics: Optional[str] = None,
    committee_name: Optional[str] = None,
    bill_names: Optional[str] = None,
    bill_types: Optional[str] = None,
    related_to_legislation: Optional[bool] = None,
    mks: Optional[str] = None,
    invitees_name: Optional[str] = None,
    legal_advisors: Optional[str] = None,
    manager: Optional[str] = None,
    financial_advisors: Optional[str] = None,
    attended_mk_individual_ids: List[int] = Query(
        [],
        alias="attended_mk_individual_ids",
        example=[],
        list=True
    )
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val = [item_ids, item_type_ids, attended_mk_individual_ids]
    arrays_number_names = ["item_ids", "item_type_ids",
                           "attended_mk_individual_ids"]
    arrays_val = [[topics], [bill_names], [bill_types], [mks],
                  [legal_advisors], [manager], [financial_advisors]]
    arrays_name = ["topics", "bill_names", "bill_types", "mks",
                   "legal_advisors", "manager", "financial_advisors"]
    objects_val = [invitees_name]
    objects_name = ["invitees_name"]
    for key, value in query_params:
        if key in arrays_number_names:
            elemts = arrays_number_val[arrays_number_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by'] and \
                key not in arrays_name and \
                key not in objects_name:
            qs_parts.append(f"{key}={value}")

    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    for name, val in zip(objects_name, objects_val):
        if val:
            qs_parts.append(f"{name}=<{val}>")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "people_committees_meeting_attendees" table
@app.get('/people_committees_meeting_attendees/{CommitteeSessionID}',
         response_model=people.CommitteesMeetingAttendees,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["people"])
async def get_meeting_attendees(CommitteeSessionID: int):
    data = DB.get_single_data('people_committees_meeting_attendees',
                              'CommitteeSessionID',
                              CommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list knesset_kns_knessetdates table
@app.get("/knesset_kns_knessetdates/list",
         response_model=List[knesset.KnsKnessetDates],
         status_code=200,
         responses={422: errors.LIMIT_ERROR},
         tags=["knesset"])
async def get_knessetdates_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    Assembly: Optional[int] = None,
    Plenum: Optional[int] = None,
    PlenumStart: Optional[str] = None,
    PlenumFinish: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM knesset_kns_knessetdates"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "knesset_kns_knessetdates" table
@app.get('/knesset_kns_knessetdates/{KnessetDateID}',
         response_model=knesset.KnsKnessetDates,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["knesset"])
async def get_knesset_dates(KnessetDateID: int):
    data = DB.get_single_data('knesset_kns_knessetdates',
                              'KnessetDateID', KnessetDateID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list votes_view_vote_mk_individual table
@app.get("/votes_view_vote_mk_individual/list",
         status_code=200,
         response_model=List[votes.ViewVoteMkIndividual],
         responses={422: errors.LIMIT_ERROR},
         tags=["votes"])
async def get_vote_mk_individual_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_individual_id: Optional[int] = None,
    mk_individual_name: Optional[str] = None,
    mk_individual_name_eng: Optional[str] = None,
    mk_individual_first_name: Optional[str] = None,
    mk_individual_first_name_eng: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_view_vote_mk_individual"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "votes_view_vote_mk_individual" table
@app.get('/votes_view_vote_mk_individual/{vip_id}',
          response_model=votes.ViewVoteMkIndividual,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["votes"])
async def get_vote_mk_individual(vip_id: int):
    data = DB.get_single_data('votes_view_vote_mk_individual',
                              'vip_id', vip_id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list bills_kns_bill table
@app.get("/bills_kns_bill/list",
         status_code=200,
         response_model=List[bills.KnsBill],
         responses={422: errors.LIMIT_ERROR},
         tags=["bills"])
async def get_bill_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    SubTypeID: Optional[int] = None,
    SubTypeDesc: Optional[str] = None,
    PrivateNumber: Optional[int] = None,
    CommitteeID: Optional[int] = None,
    StatusID: Optional[int] = None,
    Number: Optional[int] = None,
    PostponementReasonID: Optional[int] = None,
    PostponementReasonDesc: Optional[str] = None,
    PublicationDate: Optional[datetime] = None,
    MagazineNumber: Optional[int] = None,
    PageNumber: Optional[int] = None,
    IsContinuationBill: Optional[bool] = None,
    SummaryLaw: Optional[str] = None,
    PublicationSeriesID: Optional[int] = None,
    PublicationSeriesDesc: Optional[str] = None,
    PublicationSeriesFirstCall: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_bill"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "bills_kns_bill" table
@app.get('/bills_kns_bill/{BillID}',
         response_model=bills.KnsBill,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["bills"])
async def get_bill(BillID: int):
    data = DB.get_single_data('bills_kns_bill', 'BillID', BillID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_kns_person__airflow table
@app.get("/members_kns_person__airflow/list",
         status_code=200,
         response_model=List[members.PersonAirflow],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_person__airflow_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    LastName: Optional[str] = None,
    FirstName: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    Email: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_person__airflow"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_kns_person__airflow" table
@app.get('/members_kns_person__airflow/{PersonID}',
         response_model=members.PersonAirflow,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["members"])
async def get_person_airflow(PersonID: int):
    data = DB.get_single_data('members_kns_person__airflow',
                              'PersonID', PersonID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for committees_joined_meetings table
@app.get("/committees_joined_meetings/list",
         status_code=200,
         response_model=List[committees.JoinedMeetings],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_joined_meetings_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    protocol_extension: Optional[str] = None,
    text_filename: Optional[str] = None,
    parts_filename: Optional[str] = None,
    topics: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays = [[topics]]
    var_names = ["topics"]
    for key, value in query_params:
        if key in var_names:
            elemts = arrays[var_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_joined_meetings"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_joined_meetings" table
@app.get('/committees_joined_meetings/{CommitteeSessionID}',
         response_model=committees.JoinedMeetings,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_joined_meeting(CommitteeSessionID: int):
    data = DB.get_single_data('committees_joined_meetings',
                              'CommitteeSessionID',
                              CommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_mk_party_discipline_stats table
@app.get("/people_mk_party_discipline_stats/list",
         status_code=200,
         response_model=List[people.PartyDisciplineStats],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_mk_party_discipline_stats_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset: Optional[int] = None,
    plenum: Optional[int] = None,
    assembly: Optional[int] = None,
    pagra: Optional[int] = None,
    faction_id: Optional[int] = None,
    mk_id: Optional[int] = None,
    undisciplined_votes: Optional[int] = None,
    disciplined_votes: Optional[int] = None,
    total_votes: Optional[int] = None,
    undisciplined_votes_percent: Optional[int] = None,
    disciplined_votes_percent: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_mk_party_discipline_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list knesset_kns_status table
@app.get("/knesset_kns_status/list",status_code=200,
         response_model=List[knesset.KnsStatus],
         responses={422: errors.LIMIT_ERROR},
         tags=["knesset"])
async def get_knesset_status_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Desc: Optional[str] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    OrderTransition: Optional[int] = None,
    IsActive: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM knesset_kns_status"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "knesset_kns_status" table
@app.get('/knesset_kns_status/{StatusID}',
          response_model=knesset.KnsStatus,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["knesset"])
async def get_status(StatusID: int):
    data = DB.get_single_data('knesset_kns_status',
                              'StatusID', StatusID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list votes_vote_rslts_kmmbr_shadow table
@app.get("/votes_vote_rslts_kmmbr_shadow/list",
         status_code=200,
         response_model=List[votes.VoteRsltsKmmbrShadow],
         responses={422: errors.LIMIT_ERROR},
         tags=["votes"])
async def get_vote_rslts_kmmbr_shadow_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    vote_id: Optional[int] = None,
    kmmbr_id: Optional[int] = None,
    kmmbr_name: Optional[str] = None,
    vote_result: Optional[int] = None,
    knesset_num: Optional[int] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    reason: Optional[int] = None,
    modifier: Optional[str] = None,
    remark: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_vote_rslts_kmmbr_shadow"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_committees_meeting_attendees_mks_full_stats table
@app.get("/people_committees_meeting_attendees_mks_full_stats/list",
         status_code=200,
         response_model=List[people.CommitteesMeetingAttendeesMksFullStats],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_attendees_mks_full_stats_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset: Optional[int] = None,
    plenum: Optional[int] = None,
    assembly: Optional[int] = None,
    pagra: Optional[int] = None,
    committee_id: Optional[int] = None,
    faction_id: Optional[int] = None,
    mk_id: Optional[int] = None,
    attended_meetings: Optional[int] = None,
    protocol_meetings: Optional[int] = None,
    open_meetings: Optional[int] = None,
    attended_meetings_percent: Optional[int] = None,
    attended_meetings_relative_percent: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees_mks_full_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_committees_meeting_speaker_stats table
@app.get("/people_committees_meeting_speaker_stats/list",
         status_code=200,
         response_model=List[people.CommitteesMeetingSpeakerStats],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_meeting_speaker_stats_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    parts_crc32c: Optional[str] = None,
    part_index: Optional[int] = None,
    header: Optional[str] = None,
    body_length: Optional[int] = None,
    body_num_words: Optional[int] = None,
    part_categories: Optional[str] = None,
    name_role: Optional[str] = None,
    mk_individual_id: Optional[int] = None,
    mk_individual_faction: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_speaker_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_kns_cmtsitecode table
@app.get("/committees_kns_cmtsitecode/list",
         status_code=200,
         response_model=List[committees.KnsCmtSitecode],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_cmtsitecode_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnsID: Optional[int] = None,
    SiteId: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_cmtsitecode"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_kns_cmtsitecode" table
@app.get('/committees_kns_cmtsitecode/{CmtSiteCode}',
          response_model=committees.KnsCmtSitecode,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["committees"])
async def get_cmt_site_code(CmtSiteCode: int):
    data = DB.get_single_data('committees_kns_cmtsitecode',
                              'CmtSiteCode', CmtSiteCode)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list laws_kns_document_law table
@app.get("/laws_kns_document_law/list", status_code=200,
         response_model=List[laws.DocumentLaw],
         responses={422: errors.LIMIT_ERROR},
         tags=["laws"])
async def get_document_law_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    LawID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_document_law"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for "laws_kns_document_law" table
@app.get('/laws_kns_document_law/{DocumentLawID}',
          response_model=laws.DocumentLaw,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["laws"])
async def get_document_law(DocumentLawID: int):
    data = DB.get_single_data('laws_kns_document_law',
                              'DocumentLawID', DocumentLawID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_meeting_protocols_parts table
@app.get("/committees_meeting_protocols_parts/list",
         status_code=200,
         response_model=List[committees.MeetingProtocolsParts],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_meeting_protocols_parts_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    KnessetNum: Optional[int] = None,
    protocol_extension: Optional[str] = None,
    parsed_filename: Optional[str] = None,
    filesize: Optional[int] = None,
    crc32c: Optional[str] = None,
    error: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_meeting_protocols_parts"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_meeting_protocols_parts" table
@app.get('/committees_meeting_protocols_parts/{DocumentCommitteeSessionID}',
         response_model=committees.MeetingProtocolsParts,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_meeting_protocols_parts(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_meeting_protocols_parts',
                              'DocumentCommitteeSessionID',
                              DocumentCommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list votes_view_vote_rslts_hdr_approved_extra table
@app.get("/votes_view_vote_rslts_hdr_approved_extra/list",
         status_code=200,
         response_model=List[votes.ViewVoteRsltsHdrApprovedExtra],
         responses={422: errors.LIMIT_ERROR},
         tags=["votes"])
async def get_vote_rslts_hdr_approved_extra_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset_num: Optional[int] = None,
    session_id: Optional[int] = None,
    sess_item_nbr: Optional[int] = None,
    sess_item_id: Optional[int] = None,
    sess_item_dscr: Optional[str] = None,
    vote_item_id: Optional[int] = None,
    vote_item_dscr: Optional[str] = None,
    vote_date: Optional[date] = None,
    vote_time: Optional[time] = None,
    is_elctrnc_vote: Optional[int] = None,
    vote_type: Optional[int] = None,
    is_accepted: Optional[int] = None,
    total_for: Optional[int] = None,
    total_against: Optional[int] = None,
    total_abstain: Optional[int] = None,
    vote_stat: Optional[str] = None,
    session_num: Optional[int] = None,
    vote_nbr_in_sess: Optional[int] = None,
    reason: Optional[int] = None,
    modifier: Optional[str] = None,
    remark: Optional[str] = None,
    mk_ids_pro: List[int] = Query([], example=[], list=True),
    mk_ids_against: List[int] = Query([], example=[], list=True),
    mk_ids_abstain: List[int] = Query([], example=[], list=True),
    knesset: Optional[int] = None,
    plenum: Optional[int] = None,
    assembly: Optional[int] = None,
    pagra: Optional[bool] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays = [mk_ids_pro, mk_ids_against, mk_ids_abstain]
    var_names = ["mk_ids_pro", "mk_ids_against", "mk_ids_abstain"]
    for key, value in query_params:
        if key in var_names:
            elemts = arrays[var_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_view_vote_rslts_hdr_approved_extra"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for "votes_view_vote_rslts_hdr_approved_extra" table
@app.get('/votes_view_vote_rslts_hdr_approved_extra/{id}',
         response_model=votes.ViewVoteRsltsHdrApprovedExtra,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["votes"])
async def get_vote_rslts_hdr_approved_extra(id: int):
    data = DB.get_single_data('votes_view_vote_rslts_hdr_approved_extra',
                              'id', id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_build_rendered_meetings_stats table
@app.get("/committees_build_rendered_meetings_stats/list",
         status_code=200,
         response_model=List[committees.BuildRenderedMeetingsStats],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_build_rendered_meetings_stats_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    num_speech_parts: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_build_rendered_meetings_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_build_rendered_meetings_stats" table
@app.get('/committees_build_rendered_meetings_stats/{CommitteeSessionID}',
         response_model=committees.BuildRenderedMeetingsStats,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_rendered_meetings_stats(CommitteeSessionID: int):
    data = DB.get_single_data('committees_build_rendered_meetings_stats',
                              'CommitteeSessionID',
                              CommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list plenum_kns_plmsessionitem table
@app.get("/plenum_kns_plmsessionitem/list", status_code=200,
         response_model=List[plenum.PlmSessionItem],
         responses={422: errors.LIMIT_ERROR},
         tags=["plenum"])
async def get_plmsessionitem_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    ItemID: Optional[int] = None,
    PlenumSessionID: Optional[int] = None,
    ItemTypeID: Optional[int] = None,
    ItemTypeDesc: Optional[str] = None,
    Ordinal: Optional[int] = None,
    Name: Optional[str] = None,
    StatusID: Optional[int] = None,
    IsDiscussion: Optional[int] = Query(None, ge=0, le=1),
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM plenum_kns_plmsessionitem"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "plenum_kns_plmsessionitem" table
@app.get('/plenum_kns_plmsessionitem/{plmPlenumSessionID}',
         response_model=plenum.PlmSessionItem,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["plenum"])
async def get_plmsessionitem(plmPlenumSessionID: int):
    data = DB.get_single_data('plenum_kns_plmsessionitem',
                              'plmPlenumSessionID',
                              plmPlenumSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list lobbyists_v_lobbyist_clients table
@app.get("/lobbyists_v_lobbyist_clients/list", status_code=200,
         response_model=List[lobbyists.LobbyistClients],
         responses={422: errors.LIMIT_ERROR},
         tags=["lobbyists"])
async def get_lobbyist_clients_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    LobbyistID: Optional[int] = None,
    ClientID: Optional[int] = None,
    Name: Optional[str] = None,
    ClientsNames: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM lobbyists_v_lobbyist_clients"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list laws_kns_israel_law table
@app.get("/laws_kns_israel_law/list",
         status_code=200,
         response_model=List[laws.IsraelLaw],
         responses={422: errors.LIMIT_ERROR},
         tags=["laws"])
async def get_israel_law_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    IsBasicLaw: Optional[bool] = None,
    IsFavoriteLaw: Optional[bool] = None,
    IsBudgetLaw: Optional[bool] = None,
    PublicationDate: Optional[datetime] = None,
    LatestPublicationDate: Optional[str] = None,
    LawValidityID: Optional[int] = None,
    LawValidityDesc: Optional[str] = None,
    ValidityStartDate: Optional[datetime] = None,
    ValidityStartDateNotes: Optional[str] = None,
    ValidityFinishDate: Optional[datetime] = None,
    ValidityFinishDateNotes: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       return JSONResponse(content={'error': 'LimitError','msg':str(data)},
                            status_code=response_status)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "laws_kns_israel_law" table
@app.get('/laws_kns_israel_law/{IsraelLawID}',
         response_model=laws.IsraelLaw,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["laws"])
async def get_israel_law(IsraelLawID: int):
    data = DB.get_single_data('laws_kns_israel_law',
                              'IsraelLawID', IsraelLawID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for votes_vote_result_type table
@app.get("/votes_vote_result_type/list",
         status_code=200,
         response_model=List[votes.VoteResultType],
         responses={422: errors.LIMIT_ERROR},
         tags=["votes"])
async def get_vote_result_type_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    result_type_name: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_vote_result_type"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "votes_vote_result_type" table
@app.get('/votes_vote_result_type/{result_type_id}',
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["votes"])
async def get_vote_result_type(result_type_id: int):
    data = DB.get_single_data('votes_vote_result_type',
                              'result_type_id', result_type_id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_kns_documentcommitteesession table
@app.get("/committees_kns_documentcommitteesession/list",
         status_code=200,
         response_model=List[committees.KnsDocumentCommitteeSession],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_documentcommitteesession_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    DocumentCommitteeSessionID: Optional[int] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    download_filename: Optional[str] = None,
    download_filesize: Optional[int] = None,
    download_crc32c: Optional[str] = None,
    download_error: Optional[str] = None,
    text_protocol_extension: Optional[str] = None,
    text_parsed_filename: Optional[str] = None,
    text_filesize: Optional[int] = None,
    text_crc32c: Optional[str] = None,
    text_error: Optional[str] = None,
    parts_protocol_extension: Optional[str] = None,
    parts_parsed_filename: Optional[str] = None,
    parts_filesize: Optional[int] = None,
    parts_crc32c: Optional[str] = None,
    parts_error: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_documentcommitteesession"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for lobbyists_v_lobbyist table
@app.get("/lobbyists_v_lobbyist/list",
         status_code=200,
         response_model=List[lobbyists.Lobbyist],
         responses={422: errors.LIMIT_ERROR},
         tags=["lobbyists"])
async def get_lobbyist_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    IdentityNumber: Optional[str] = None,
    FullName: Optional[str] = None,
    PermitTypeValue: Optional[str] = None,
    Key: Optional[int] = None,
    CorporationName: Optional[str] = None,
    IsIndependent: Optional[bool] = None,
    CorpNumber: Optional[int] = None,
    PracticeFramework: Optional[str] = None,
    IsMemberInFaction: Optional[str] = None,
    MemberInFaction: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM lobbyists_v_lobbyist"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "lobbyists_v_lobbyist" table
@app.get('/lobbyists_v_lobbyist/{LobbyistID}',
          response_model=lobbyists.Lobbyist,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["lobbyists"])
async def get_lobbyist(LobbyistID: int):
    data = DB.get_single_data('lobbyists_v_lobbyist',
                              'LobbyistID', LobbyistID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list laws_kns_israel_law_binding table
@app.get("/laws_kns_israel_law_binding/list",
         status_code=200,
         response_model=List[laws.IsraelLawBinding],
         responses={422: errors.LIMIT_ERROR},
         tags=["laws"])
async def get_israel_law_binding_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    IsraelLawID: Optional[int] = None,
    IsraelLawReplacedID: Optional[int] = None,
    LawID: Optional[int] = None,
    LawTypeID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law_binding"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "laws_kns_israel_law_binding" table
@app.get('/laws_kns_israel_law_binding/{IsraelLawBinding}',
          response_model=laws.IsraelLawBinding,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["laws"])
async def get_israel_law_binding(IsraelLawBinding: int):
    data = DB.get_single_data('laws_kns_israel_law_binding',
                              'IsraelLawBinding', IsraelLawBinding)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_plenum_session_voters table
@app.get("/people_plenum_session_voters/list",
         status_code=200,
         response_model=List[people.PlenumSessionVoters],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_plenum_session_voters_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    IsSpecialMeeting: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None,
    voter_mk_ids: List[int] = Query([], example=[], list=True)
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays = [voter_mk_ids]
    var_names = ["voter_mk_ids"]
    for key, value in query_params:
        if key in var_names:
            elemts = arrays[var_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_plenum_session_voters"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "people_plenum_session_voters" table
@app.get('/people_plenum_session_voters/{PlenumSessionID}',
          response_model=people.PlenumSessionVoters,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["people"])
async def get_plenum_session_voters(PlenumSessionID: int):
    data = DB.get_single_data('people_plenum_session_voters',
                              'PlenumSessionID', PlenumSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_mk_voted_against_majority table
@app.get("/people_mk_voted_against_majority/list",
         status_code=200,
         response_model=List[people.MkVotedAgainstMajority],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_mk_voted_against_majority_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    vote_id: Optional[int] = None,
    mk_id: Optional[int] = None,
    faction_id: Optional[int] = None,
    vote_knesset: Optional[int] = None,
    vote_plenum: Optional[int] = None,
    vote_assembly: Optional[int] = None,
    vote_pagra: Optional[bool] = None,
    vote_datetime: Optional[datetime] = None,
    vote_majority: Optional[str] = None,
    voted_against_majority: Optional[bool] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_mk_voted_against_majority"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_kns_cmtsessionitem table
@app.get("/committees_kns_cmtsessionitem/list",
         status_code=200,
         response_model=List[committees.KnsCmtSessionItem],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_cmtsessionitem_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    ItemID: Optional[int] = None,
    CommitteeSessionID: Optional[int] = None,
    Ordinal: Optional[int] = None,
    StatusID: Optional[int] = None,
    Name: Optional[str] = None,
    ItemTypeID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_cmtsessionitem"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for "committees_kns_cmtsessionitem" table
@app.get('/committees_kns_cmtsessionitem/{CmtSessionItemID}',
          response_model=committees.KnsCmtSessionItem,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["committees"])
async def get_cmtsessionitem(CmtSessionItemID: int):
    data = DB.get_single_data('committees_kns_cmtsessionitem',
                              'CmtSessionItemID',
                              CmtSessionItemID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list laws_kns_israel_law_ministry table
@app.get("/laws_kns_israel_law_ministry/list",
         status_code=200,
         response_model=List[laws.IsraelLawMinistry],
         responses={422: errors.LIMIT_ERROR},
         tags=["laws"])
async def get_israel_law_ministry_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    IsraelLawID: Optional[int] = None,
    GovMinistryID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law_ministry"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "laws_kns_israel_law_ministry" table
@app.get('/laws_kns_israel_law_ministry/{LawMinistryID}',
         response_model=laws.IsraelLawMinistry,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["laws"])
async def get_israel_law_ministry(LawMinistryID: int):
    data = DB.get_single_data('laws_kns_israel_law_ministry',
                              'LawMinistryID', LawMinistryID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_mk_party_discipline_knesset_20 table
@app.get("/people_mk_party_discipline_knesset_20/list",
         status_code=200,
         response_model=List[people.MkPartyDisciplineKnesset20],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_mk_party_discipline_knesset_20_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    vote_id: Optional[int] = None,
    vote_url: Optional[str] = None,
    vote_datetime: Optional[datetime] = None,
    vote_knesset: Optional[int] = None,
    vote_plenum: Optional[int] = None,
    vote_assembly: Optional[int] = None,
    vote_pagra: Optional[bool] = None,
    mk_id: Optional[int] = None,
    mk_name: Optional[str] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    vote_majority: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_mk_party_discipline_knesset_20"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_kns_committeesession table
@app.get("/committees_kns_committeesession/list",
         status_code=200,
         response_model=List[committees.KnsCommitteeSession],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_committeesession_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[date] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    download_crc32c: Optional[str] = None,
    download_filename: Optional[str] = None,
    download_filesize: Optional[int] = None,
    parts_crc32c: Optional[str] = None,
    parts_filesize: Optional[int] = None,
    parts_parsed_filename: Optional[str] = None,
    text_crc32c: Optional[str] = None,
    text_filesize: Optional[int] = None,
    text_parsed_filename: Optional[str] = None,
    item_ids: List[int] = Query([], example=[], list=True),
    item_type_ids: List[int] = Query([], example=[], list=True),
    topics: Optional[str] = None,
    committee_name: Optional[str] = None,
    bill_names: Optional[str] = None,
    bill_types: Optional[str] = None,
    related_to_legislation: Optional[bool] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays = [item_ids, item_type_ids, [topics], [bill_names], [bill_types]]
    var_names = ["item_ids", "item_type_ids", "topics", "bill_names",
                 "bill_types"]
    for key, value in query_params:
        if key in var_names:
            elemts = arrays[var_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_committeesession"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_kns_mksitecode table
@app.get("/members_kns_mksitecode/list",
         status_code=200,
         response_model=List[members.Mksitecode],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_mksitecode_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnsID: Optional[int] = None,
    SiteId: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_mksitecode"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_kns_mksitecode" table
@app.get('/members_kns_mksitecode/{MKSiteCode}',
         response_model=members.Mksitecode,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["members"])
async def get_mksitecode(MKSiteCode: int):
    data = DB.get_single_data('members_kns_mksitecode',
                              'MKSiteCode', MKSiteCode)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_committees_meeting_attendees_mks_stats table
@app.get("/people_committees_meeting_attendees_mks_stats/list",
         status_code=200,
         response_model=List[people.CommitteesMeetingAttendeesMksStats],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_committee_attendees_mks_stats_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset_num: Optional[int] = None,
    committee_id: Optional[int] = None,
    committee_name: Optional[str] = None,
    meeting_start_date: Optional[datetime] = None,
    meeting_topics: Optional[str] = None,
    mk_id: Optional[int] = None,
    mk_name: Optional[str] = None,
    mk_membership_committee_names: Optional[str] = None,
    mk_faction_id: Optional[int] = None,
    mk_faction_name: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees_mks_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for laws_kns_law table
@app.get("/laws_kns_law/list", 
          status_code=200,
          response_model=List[laws.KnsLaw],
          responses={422: errors.LIMIT_ERROR},
          tags=["laws"])
async def get_law_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    SubTypeID: Optional[int] = None,
    SubTypeDesc: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    PublicationDate: Optional[datetime] = None,
    PublicationSeriesID: Optional[int] = None,
    PublicationSeriesDesc: Optional[str] = None,
    MagazineNumber: Optional[str] = None,
    PageNumber: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_law"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "laws_kns_law" table
@app.get('/laws_kns_law/{LawID}',
         response_model=laws.KnsLaw,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["laws"])
async def get_law(LawID: int):
    data = DB.get_single_data('laws_kns_law', 'LawID', LawID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_document_committee_sessions_for_parsing table
@app.get("/committees_document_committee_sessions_for_parsing/list",
         status_code=200,
         response_model=List[committees.DocumentCommitteeSessionsParsing],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_committee_sessions_for_parsing_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    KnessetNum: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_document_committee_sessions_for_parsing"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_document_committee_sessions_for_parsing" table
@app.get('/committees_document_committee_sessions_for_parsing/{DocumentCommitteeSessionID}',
          response_model=committees.DocumentCommitteeSessionsParsing,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["committees"])
async def get_document_committee_sessions_for_parsing(DocumentCommitteeSessionID: int):
    data = DB.get_single_data
    (
        'committees_document_committee_sessions_for_parsing',
        'DocumentCommitteeSessionID',
        DocumentCommitteeSessionID
    )
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data


# Route for list committees_download_document_committee_session table
@app.get("/committees_download_document_committee_session/list",
         status_code=200,
         response_model=List[committees.DownloadDocumentCommitteeSession],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_download_document_committee_session_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    KnessetNum: Optional[int] = None,
    filename: Optional[str] = None,
    filesize: Optional[int] = None,
    crc32c: Optional[str] = None,
    error: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_download_document_committee_session"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_download_document_committee_session" table
@app.get('/committees_download_document_committee_session/{DocumentCommitteeSessionID}',
         response_model=committees.DownloadDocumentCommitteeSession,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_download_document_committee_session(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_download_document_committee_session',
                              'DocumentCommitteeSessionID',
                              DocumentCommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list laws_kns_israel_law_name table
@app.get("/laws_kns_israel_law_name/list",
         status_code=200,
         response_model=List[laws.IsraelLawName],
         responses={422: errors.LIMIT_ERROR},
         tags=["laws"])
async def get_israel_law_name_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    IsraelLawID: Optional[int] = None,
    LawID: Optional[int] = None,
    LawTypeID: Optional[int] = None,
    Name: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law_name"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "laws_kns_israel_law_name" table
@app.get('/laws_kns_israel_law_name/{IsraelLawNameID}',
         response_model=laws.IsraelLawName,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["laws"])
async def get_israel_law_name(IsraelLawNameID: int):
    data = DB.get_single_data('laws_kns_israel_law_name',
                              'IsraelLawNameID', IsraelLawNameID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_members_joined_mks table
@app.get("/people_members_joined_mks/list",
         status_code=200,
         response_model=List[people.MembersJoinedMks],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_joined_mks_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_status_id: Optional[int] = None,
    mk_individual_name: Optional[str] = None,
    mk_individual_name_eng: Optional[str] = None,
    mk_individual_first_name: Optional[str] = None,
    mk_individual_first_name_eng: Optional[str] = None,
    mk_individual_email: Optional[str] = None,
    mk_individual_photo: Optional[str] = None,
    PersonID: Optional[int] = None,
    LastName: Optional[str] = None,
    FirstName: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    Email: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None,
    positions_gender: Optional[str] = None,
    positions_position: Optional[str] = None,
    positions_KnessetNum: Optional[int] = None,
    positions_start_date: Optional[datetime] = None,
    positions_finish_date: Optional[datetime] = None,
    positions_position_id: Optional[int] = None,
    positions_FactionID: Optional[int] = None,
    positions_FactionName: Optional[str] = None,
    positions_CommitteeID: Optional[int] = None,
    positions_CommitteeName: Optional[str] = None,
    positions_DutyDesc: Optional[str] = None,
    positions_GovMinistryID: Optional[int] = None,
    positions_GovernmentNum: Optional[int] = None,
    positions_GovMinistryName: Optional[str] = None,
    altnames: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_val = [[altnames]]
    arrays_name = ["altnames"]
    objects_val = [positions_gender, positions_position,
                   positions_KnessetNum, positions_start_date,
                   positions_finish_date, positions_position_id,
                   positions_FactionID, positions_FactionName,
                   positions_CommitteeID, positions_CommitteeName,
                   positions_DutyDesc, positions_GovMinistryID,
                   positions_GovernmentNum, positions_GovMinistryName]
    objects_name = ["positions_gender", "positions_position",
                    "positions_KnessetNum", "positions_start_date",
                    "positions_finish_date", "positions_position_id",
                    "positions_FactionID", "positions_FactionName",
                    "positions_CommitteeID", "positions_CommitteeName",
                    "positions_DutyDesc", "positions_GovMinistryID",
                    "positions_GovernmentNum", "positions_GovMinistryName"]
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by'] and \
           key not in objects_name and \
           key not in arrays_name:
            qs_parts.append(f"{key}={value}")
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    for name, val in zip(objects_name, objects_val):
        if val:
            qs_parts.append(f"{name}=<{val}>")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_members_joined_mks"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "people_members_joined_mks" table
@app.get('/people_members_joined_mks/{mk_individual_id}',
          response_model=people.MembersJoinedMks,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["people"])
async def get_members_joined_mks(mk_individual_id: int):
    data = DB.get_single_data('people_members_joined_mks',
                              'mk_individual_id', mk_individual_id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list laws_kns_law_binding table
@app.get("/laws_kns_law_binding/list",
         status_code=200,
         response_model=List[laws.LawBinding],
         responses={422: errors.LIMIT_ERROR},
         tags=["laws"])
async def get_law_binding_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    LawID: Optional[int] = None,
    LawTypeID: Optional[int] = None,
    IsraelLawID: Optional[int] = None,
    ParentLawID: Optional[int] = None,
    LawParentTypeID: Optional[int] = None,
    BindingType: Optional[int] = None,
    BindingTypeDesc: Optional[str] = None,
    PageNumber: Optional[str] = None,
    AmendmentType: Optional[int] = None,
    AmendmentTypeDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_law_binding"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "laws_kns_law_binding" table
@app.get('/laws_kns_law_binding/{LawBindingID}',
         response_model=laws.LawBinding,
         responses={
            404: errors.NO_DATA_FOUND_ERROR
         },
         tags=["laws"])
async def get_law_binding(LawBindingID: int):
    data = DB.get_single_data('laws_kns_law_binding',
                              'LawBindingID', LawBindingID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list knesset_kns_itemtype table
@app.get("/knesset_kns_itemtype/list",
         status_code=200,
         response_model=List[knesset.KnsItemtype],
         responses={422: errors.LIMIT_ERROR},
         tags=["knesset"])
async def get_knesset_itemtype_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Desc: Optional[str] = None,
    TableName: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM knesset_kns_itemtype"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "knesset_kns_itemtype" table
@app.get('/knesset_kns_itemtype/{ItemTypeID}',
          response_model=knesset.KnsItemtype,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["knesset"])
async def get_itemtype(ItemTypeID: int):
    data = DB.get_single_data('knesset_kns_itemtype', 'ItemTypeID', ItemTypeID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_meeting_protocols_text table
@app.get("/committees_meeting_protocols_text/list",
         status_code=200,
         response_model=List[committees.MeetingProtocolsText],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_committee_meeting_protocols_text_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    KnessetNum: Optional[int] = None,
    protocol_extension: Optional[str] = None,
    parsed_filename: Optional[str] = None,
    filesize: Optional[str] = None,
    crc32c: Optional[str] = None,
    error: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_meeting_protocols_text"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_meeting_protocols_text" table
@app.get('/committees_meeting_protocols_text/{DocumentCommitteeSessionID}',
          response_model=committees.MeetingProtocolsText,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["committees"])
async def get_meeting_protocols_text(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_meeting_protocols_text',
                              'DocumentCommitteeSessionID',
                              DocumentCommitteeSessionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list people_committees_meeting_attendees_mks table
@app.get("/people_committees_meeting_attendees_mks/list",
         status_code=200,
         response_model=List[people.CommitteesMeetingAttendeesMks],
         responses={422: errors.LIMIT_ERROR},
         tags=["people"])
async def get_committee_attendees_mks_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    protocol_extension: Optional[str] = None,
    text_filename: Optional[str] = None,
    parts_filename: Optional[str] = None,
    topics: Optional[str] = None,
    mks: Optional[str] = None,
    invitees_name: Optional[str] = None,
    invitees_role: Optional[str] = None,
    legal_advisors: Optional[str] = None,
    manager: Optional[str] = None,
    attended_mk_individual_ids: List[int] = Query(
        [], alias="attended_mk_individual_ids",
        example=[736],
        list=True
    )
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val = [attended_mk_individual_ids]
    arrays_number_names = ["attended_mk_individual_ids"]
    arrays_val = [[topics], [mks], [legal_advisors], [manager]]
    arrays_name = ["topics", "mks", "legal_advisors", "manager"]
    objects_val = [invitees_name, invitees_role]
    objects_name = ["invitees_name", "invitees_role"]
    for key, value in query_params:
        if key in arrays_number_names:
            elemts = arrays_number_val[arrays_number_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
            if key not in ['limit', 'offset', 'order_by'] and \
               key not in objects_name and \
               key not in arrays_name:
                qs_parts.append(f"{key}={value}")

    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    for name, val in zip(objects_name, objects_val):
        if val:
            qs_parts.append(f"{name}=<{val}>")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees_mks"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_kns_person table
@app.get("/members_kns_person/list",
         status_code=200,
         response_model=List[members.Person],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_person_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    PersonID: Optional[int] = None,
    LastName: Optional[str] = None,
    FirstName: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    Email: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_person"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_kns_person" table
@app.get('/members_kns_person/{PersonID}',
          response_model=members.Person,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["members"])
async def get_person(PersonID: int):
    data = DB.get_single_data('members_kns_person', 'PersonID', PersonID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_mk_individual table
@app.get("/members_mk_individual/list",
         status_code=200,
         response_model=List[members.Individual],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_mk_individual_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_status_id: Optional[int] = None,
    mk_individual_name: Optional[str] = None,
    mk_individual_name_eng: Optional[str] = None,
    mk_individual_first_name: Optional[str] = None,
    mk_individual_first_name_eng: Optional[str] = None,
    mk_individual_email: Optional[str] = None,
    mk_individual_photo: Optional[str] = None,
    PersonID: Optional[int] = None,
    LastName: Optional[str] = None,
    FirstName: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    Email: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None,
    altnames: Optional[str] = None,
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_val = [[altnames]]
    arrays_name = ["altnames"]
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by'] and \
           key not in arrays_name:
            qs_parts.append(f"{key}={value}")
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_mk_individual" table
@app.get('/members_mk_individual/{mk_individual_id}',
         response_model=members.Individual,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["members"])
async def get_individual(mk_individual_id: int):
    data = DB.get_single_data('members_mk_individual',
                              'mk_individual_id', mk_individual_id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_factions table
@app.get("/members_factions/list",
         status_code=200,
         response_model=List[members.Factions],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_factions_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knessets: List[int] = Query([], alias="knessets", example=[], list=True),
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val = [knessets]
    arrays_number_names = ["knessets"]
    for key, value in query_params:
        if key in arrays_number_names:
            elemts = arrays_number_val[arrays_number_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_factions"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for "members_factions" table
@app.get('/members_factions/{id}',
         response_model=members.Factions,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["members"])
async def get_factions(id: int):
    data = DB.get_single_data('members_factions', 'id', id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list laws_kns_israel_law_classification table
@app.get("/laws_kns_israel_law_classification/list",       
         status_code=200,
         response_model=List[laws.IsraelLawClassification],
         responses={422: errors.LIMIT_ERROR},
         tags=["laws"])
async def get_israel_law_classification_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    IsraelLawID: Optional[int] = None,
    ClassificiationID: Optional[int] = None,
    ClassificiationDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law_classification"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "laws_kns_israel_law_classification" table
@app.get('/laws_kns_israel_law_classification/{LawClassificiationID}',
         response_model=laws.IsraelLawClassification,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["laws"])
async def get_israel_law_classification(LawClassificiationID: int):
    data = DB.get_single_data('laws_kns_israel_law_classification',
                              'LawClassificiationID',
                              LawClassificiationID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_mk_individual_names table
@app.get("/members_mk_individual_names/list",
         status_code=200,
         response_model=List[members.IndividualNames],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_mk_individual_names_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    names: Optional[str] = None,
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_val = [[names]]
    arrays_name = ["names"]
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by'] and \
           key not in arrays_name:
            qs_parts.append(f"{key}={value}")
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_names"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_mk_individual_names" table
@app.get('/members_mk_individual_names/{mk_individual_id}',
         response_model=members.IndividualNames,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["members"])
async def get_individual_names(mk_individual_id: int):
    data = DB.get_single_data('members_mk_individual_names',
                              'mk_individual_id',
                              mk_individual_id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_faction_memberships table
@app.get("/members_faction_memberships/list",
         status_code=200,
         response_model=List[members.FactionMemberships],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_members_faction_memberships_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    member_mk_ids: List[int] = Query(
        [], alias="member_mk_ids",
        example=[],
        list=True
    ),
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val = [member_mk_ids]
    arrays_number_names = ["member_mk_ids"]
    for key, value in query_params:
        if key in arrays_number_names:
            elemts = arrays_number_val[arrays_number_names.index(key)]
            qs_parts.append(f"{key}={elemts}")
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_faction_memberships"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_faction_memberships" table
@app.get('/members_faction_memberships/{faction_id}',
          response_model=members.FactionMemberships,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["members"])
async def get_faction_memberships(faction_id: int):
    data = DB.get_single_data('members_faction_memberships',
                              'faction_id', faction_id)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_kns_persontoposition table
@app.get("/members_kns_persontoposition/list",
         status_code=200,
         response_model=List[members.PersonToPosition],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_person_to_position_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    PersonID: Optional[int] = None,
    PositionID: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    GovMinistryID: Optional[int] = None,
    GovMinistryName: Optional[str] = None,
    DutyDesc: Optional[str] = None,
    FactionID: Optional[int] = None,
    FactionName: Optional[str] = None,
    GovernmentNum: Optional[int] = None,
    CommitteeID: Optional[int] = None,
    CommitteeName: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_persontoposition"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_kns_persontoposition" table
@app.get('/members_kns_persontoposition/{PersonToPositionID}',
          response_model=members.PersonToPosition,
          responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
          tags=["members"])
async def get_persontoposition(PersonToPositionID: int):
    data = DB.get_single_data('members_kns_persontoposition',
                              'PersonToPositionID',
                              PersonToPositionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list committees_kns_committee table
@app.get("/committees_kns_committee/list",
         status_code=200,
         response_model=List[committees.KnsCommittee],
         responses={422: errors.LIMIT_ERROR},
         tags=["committees"])
async def get_committee_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Name: Optional[str] = None,
    CategoryID: Optional[int] = None,
    CategoryDesc: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    CommitteeTypeID: Optional[int] = None,
    CommitteeTypeDesc: Optional[str] = None,
    Email: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    AdditionalTypeID: Optional[int] = None,
    AdditionalTypeDesc: Optional[str] = None,
    ParentCommitteeID: Optional[int] = None,
    CommitteeParentName: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_committee"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "committees_kns_committee" table
@app.get('/committees_kns_committee/{CommitteeID}',
         response_model=committees.KnsCommittee,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["committees"])
async def get_single_data(CommitteeID: int):
    data = DB.get_single_data('committees_kns_committee',
                              'CommitteeID', CommitteeID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_mk_individual_factions table
@app.get("/members_mk_individual_factions/list",
         status_code=200,
         response_model=List[members.IndividualFactions],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_mk_individual_factions_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_individual_id: Optional[int] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_factions"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for list members_kns_position table
@app.get("/members_kns_position/list",
         status_code=200,
         response_model=List[members.Position],
         responses={422: errors.LIMIT_ERROR},
         tags=["members"])
async def get_position_list(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    Description: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_position"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Route for single "members_kns_position" table
@app.get('/members_kns_position/{PositionID}',
         response_model=members.Position,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=["members"])
async def get_position(PositionID: int):
    data = DB.get_single_data('members_kns_position',
                              'PositionID', PositionID)
    if isinstance(data, TypeError):
       response_status = (status.HTTP_404_NOT_FOUND)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



# Aggragation
@app.get('/minister_by_individual/{id}',
         status_code=200,
         response_model=current_minister.MinisterByIndividual,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=['Current ministers'],
         description = """
             Retrieve information about a minister based on their individual ID.
             
             This route returns data about a minister, including their personal details and legislative history.
             The keys in the 'data' dictionary provide the following information:

             - 'mk_individual_id': The unique identifier for the individual minister.
             - 'FirstName': The first name of the minister.
             - 'LastName': The last name of the minister.
             - 'GenderDesc': The gender of the minister.
             - 'Email': The email address of the minister.
             - 'altnames': Alternate names or aliases of the minister.
             - 'mk_individual_photo': URL to the minister's photo.
             - 'faction_name': The political faction or party the minister belongs to.
             - 'ministers': List of ministerial roles held by the individual.
             - 'IsChairPerson': Indicates whether the minister is a chairperson (true or false).
             - 'knessets': List of Knessets (Israeli parliaments) the minister has served in.
             - 'committees': List of committees the minister has been associated with (may contain null values).
             - 'year_total_hours_attended': A historical record of the minister's yearly hours attended in sessions.

             You can use this data to gain insights into the minister's political career and activities.
             """,
         summary="Get current minister by individual identifier")
@app.get('/minister_by_personal/{id}',
         status_code=200,
         response_model=current_minister.MinisterByPersonal,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=['Current ministers'],
         description = """
             Retrieve information about a minister based on their personal ID.
             
             This route returns data about a minister, including their personal details and legislative history.
             The keys in the 'data' dictionary provide the following information:

             - 'PersonID': The unique identifier for the individual minister.
             - 'FirstName': The first name of the minister.
             - 'LastName': The last name of the minister.
             - 'GenderDesc': The gender of the minister.
             - 'Email': The email address of the minister.
             - 'altnames': Alternate names or aliases of the minister.
             - 'mk_individual_photo': URL to the minister's photo.
             - 'faction_name': The political faction or party the minister belongs to.
             - 'ministers': List of ministerial roles held by the individual.
             - 'IsChairPerson': Indicates whether the minister is a chairperson (true or false).
             - 'knessets': List of Knessets (Israeli parliaments) the minister has served in.
             - 'committees': List of committees the minister has been associated with (may contain null values).
             - 'year_total_hours_attended': A historical record of the minister's yearly hours attended in sessions.

             You can use this data to gain insights into the minister's political career and activities.
             """,
         summary="Get current minister by personal identifier")
def get_minister(id: int, request: Request):
    request_path = request.scope['path']
    id_field = (
        "mk_individual_id"
        if request_path == f'/minister_by_individual/{str(id)}' else 'PersonID'
    )
    query = QUERY.get_minister_query(id_field)
    data = DB.get_fully_today_member(query, (id,))
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data



@app.get('/member_kns_by_individual/{id}',
         status_code=200,
         response_model=current_knesset_member.KnessetMemberByIndividual,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=['Current knesset members'],
         description="""
             Retrieve detailed information about a specific Knesset member based on their unique individual ID.         

             The 'data' dictionary provides the following information:

             - 'mk_individual_id': The unique identifier for the individual Knesset member.
             - 'FirstName': The first name of the Knesset member.
             - 'LastName': The last name of the Knesset member.
             - 'GenderDesc': The gender of the Knesset member.
             - 'Email': The email address of the Knesset member.
             - 'altnames': Alternate names or aliases of the Knesset member.
             - 'mk_individual_photo': URL to the Knesset member's photo.
             - 'faction_name': The political faction or party associated with the Knesset member.
             - 'IsChairPerson': Indicates whether the Knesset member holds a chairperson position (true or false).
             - 'knessets': List of Knessets (Israeli parliaments) the Knesset member has served in.
             - 'committees': List of committees the Knesset member has been associated with, if any.
             - 'year_total_hours_attended': A historical record of the Knesset member's yearly hours attended in sessions.

             This information provides a comprehensive overview of the Knesset member's political career and activities.
             """,
         summary="Get current member knesset by individual identifier")
@app.get('/member_kns_by_personal/{id}',
         status_code=200,
         response_model=current_knesset_member.KnessetMemberByPersonal,
         responses={
            404: errors.NO_DATA_FOUND_ERROR,
          },
         tags=['Current knesset members'],
         description="""
             Retrieve detailed information about a specific Knesset member based on their unique personal ID.         

             The 'data' dictionary provides the following information:

             - 'PersonID': The unique identifier for the individual Knesset member.
             - 'FirstName': The first name of the Knesset member.
             - 'LastName': The last name of the Knesset member.
             - 'GenderDesc': The gender of the Knesset member.
             - 'Email': The email address of the Knesset member.
             - 'altnames': Alternate names or aliases of the Knesset member.
             - 'mk_individual_photo': URL to the Knesset member's photo.
             - 'faction_name': The political faction or party associated with the Knesset member.
             - 'IsChairPerson': Indicates whether the Knesset member holds a chairperson position (true or false).
             - 'knessets': List of Knessets (Israeli parliaments) the Knesset member has served in.
             - 'committees': List of committees the Knesset member has been associated with, if any.
             - 'year_total_hours_attended': A historical record of the Knesset member's yearly hours attended in sessions.

             This information provides a comprehensive overview of the Knesset member's political career and activities.
             """,
         summary="Get current member knesset by personal identifier")
def get_member_kns(id: int, request: Request):
    request_path = request.scope['path']
    id_field = (
        "mk_individual_id"
        if request_path == f'/member_kns_by_individual/{str(id)}' else 'PersonID'
    )
    query = QUERY.get_member_kns_query(id_field)
    data = DB.get_fully_today_member(query, (id,))
    if isinstance(data, Exception):
       response_status = (status.HTTP_404_NOT_FOUND
                           if isinstance(data, TypeError)
                           else status.HTTP_422_UNPROCESSABLE_ENTITY)
       raise HTTPException(status_code=response_status, detail={'error': type(data).__name__,'msg':str(data)})
    return data
