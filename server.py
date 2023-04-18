from flask import Flask,request
from flask_cors import CORS
import api.db as DB
import api.queries as QUERY
import json
app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
app.secret_key = 'oknesset#@@#'
app.config['ENV'] = "development"
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return {'success': True, 'data' : []}, 200
    
@app.route('/db')
def db_tables():
    return {'success': True, 'data' : DB.get_data("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")}, 200

@app.route('/members')
def members_presence():
    return {'success': True, 'data' : DB.get_data('SELECT * FROM members_presence ORDER BY date DESC')}, 200

@app.route('/discribe')
def get_discribe():
    return {'success': True, 'data' : DB.get_discribe('members_presence')}, 200
    
@app.route('/members_kns/list')
def get_members_kns_person_list():
    status_code=200
    data=DB.get_data_list("SELECT * FROM members_mk_individual")
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code
    return {'success': True, 'data' :data }, status_code 
    
@app.route('/member_kns_by_individual/<int:id>')
@app.route('/member_kns_by_personal/<int:id>')
def get_member_kns(id):
    status_code=200
    id_field = "mk_individual_id" if request.path == "/member_kns_by_individual/" + str(id) else "PersonID"
    query = QUERY.get_member_kns_query(id_field)
    data = DB.get_fully_today_kns_member(query, (id,))
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code 

    return {'success': True, 'data' :data }, status_code 

@app.route('/minister_by_individual/<int:id>')
@app.route('/minister_by_personal/<int:id>')
def get_minister(id):
    status_code=200
    id_field = "mk_individual_id" if request.path == "/minister_by_individual/" + str(id) else "PersonID"
    query = QUERY.get_minister_query(id_field)
    data = DB.get_fully_today_kns_member(query, (id,))
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code 

    return {'success': True, 'data' :data }, status_code         
if __name__ == "__main__":
    app.run(debug=True)
