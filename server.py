from flask import Flask
from flask_cors import CORS
import api.db as DB

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
    data=DB.get_data_list("SELECT * FROM members_kns_person")
    if  isinstance(data, Exception):
        if str(data)=='No row found':
            status_code=404
        else:
            status_code=400
        return {'success': False, 'data' :str(data)},status_code     
    return {'success': True, 'data' :data }, status_code 
    
if __name__ == "__main__":
    app.run(debug=True)