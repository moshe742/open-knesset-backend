from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import api.db as DB

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.route('/')
async def index():
    return {'success': True, 'data': []}


@app.route('/db')
async def db_tables():
    return {'success': True, 'data': DB.get_data("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")}, 200


@app.route('/members')
async def members_presence():
    return {'success': True, 'data': DB.get_data('SELECT * FROM members_presence ORDER BY date DESC')}, 200


@app.route('/discribe')
async def get_discribe():
    return {'success': True, 'data': DB.get_discribe('members_presence')}, 200


@app.route('/members_kns/list')
async def get_members_kns_person_list():
    status_code=200
    data=DB.get_data_list("SELECT * FROM members_kns_person")
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code
    return {'success': True, 'data':data }, status_code


# favicon_api = FastAPI()
#
#
# # favicon
# @favicon_api.get('/favicon.ico')
# def favicon():
#     return url_for('static', filename='/images/hasadna-logo.ico')
