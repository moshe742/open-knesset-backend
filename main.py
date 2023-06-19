from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import api.db as DB

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['*']
)


@app.get('/')
async def root():
    return {'success': True, 'data': []}


@app.get('/db')
async def db_tables():
    return {'success': True, 'data': DB.get_data(
        "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")}


@app.get('/members')
async def members_presence():
    return {'success': True, 'data': DB.get_data('SELECT * FROM members_presence ORDER BY date DESC')}


@app.get('/discribe')
async def get_discribe():
    return {'success': True, 'data': DB.get_discribe('members_presence')}


@app.get('/members_kns/list', status_code=200)
async def get_members_kns_person_list(limit: int = 0, offset: int = 0, order_by: str | None = None, qs: str = None):
    data = DB.get_data_list("SELECT * FROM members_kns_person", limit, offset, order_by, qs)
    if isinstance(data, Exception):
        Response.status_code = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return {'success': False, 'data': str(data)}
    return {'success': True, 'data': data}


@app.get('/minister_by_individual/<int:id>', status_code=200)
@app.get('/minister_by_personal/<int:id>', status_code=200)
def get_minister(person_id):
    id_field = (
        "mk_individual_id"
        if request_path == f'/minister_by_individual/{str(person_id)}' else 'PersonID'
    )
    query = QUERY.get_minister_query(id_field)
    data = DB.get_fully_today_kns_member(query, (person_id,))
    if isinstance(data, Exception):
        response.status_code = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return {'success': False, 'data': str(data)}
    return {'success': True, 'data': data}


@app.get('/committee_sessions')
async def committee_sessions(knesset_num: int):
    data = DB.get_committee('committees_kns_committeesession', 'KnessetNum', knesset_num)
    return {'success': True, 'data': data}


@app.get('/committee')
async def committee_sessions_by_id(committee_id: int):
    data = DB.get_committee('committees_kns_committee', 'CommitteeID', committee_id)
    return {'success': True, 'data': data}


@app.get('/committee_sessions/documents')
async def committee_sessions_by_id(committee_session_id: int):
    data = DB.get_committee('committees_kns_documentcommitteesession', 'CommitteeSessionID', committee_session_id)
    return {'success': True, 'data': data}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('static/images/hasadna-logo.ico')


# favicon_api = FastAPI()
#
#
# # favicon
# @favicon_api.get('/favicon.ico')
# def favicon():
#     return url_for('static', filename='/images/hasadna-logo.ico')
