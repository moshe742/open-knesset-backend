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
    print('hello')
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
    print(limit, offset)
    data = DB.get_data_list("SELECT * FROM members_kns_person", limit, offset, order_by, qs)
    if isinstance(data, Exception):
        Response.status_code = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return {'success': False, 'data': str(data)}
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
