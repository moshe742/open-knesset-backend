from flask import Flask
from flask_cors import CORS
import api.db as DB

app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
app.secret_key = 'oknesset#@@#'
app.config['ENV'] = "development"

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
    
if __name__ == "__main__":
    app.run(debug=True)