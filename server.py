from flask import Flask,request
from flask_cors import CORS
import api.db as DB
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
    data=DB.get_data_list("SELECT * FROM members_kns_person")
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code
    return {'success': True, 'data' :data }, status_code 
    
@app.route('/by_individual/<int:id>')
@app.route('/by_personal/<int:id>')
def get_member_kns(id):
    status_code=200
    id_field = "mk_individual_id" if request.path == "/by_individual/" + str(id) else "PersonID"
    query = f"""
                SELECT 
                    f."{id_field}",
                    f."FirstName",
                    f."LastName",
                    f."GenderDesc",
                    f."IsCurrent",
                    f."Email",
                    f."altnames",
                    f."mk_individual_photo",
                    m."faction_name",
                    COALESCE(array_to_string(kns.knesset_array::text[], ', '), '') AS "knesset",
                    COALESCE(json_agg(DISTINCT c."committee_name" || ' (' || c."position_name" || ')') ) AS "committees",
                    CASE WHEN ch."mk_individual_id" IS NOT NULL THEN true ELSE false END AS "IsChairPerson",
                    CONCAT('[', STRING_AGG(DISTINCT CONCAT(year, '-', total_attended_hours), ','), ']') AS year_total_hours_attended
                FROM members_faction_memberships m
                JOIN members_mk_individual f
                    ON f."mk_individual_id" = ANY(ARRAY(SELECT jsonb_array_elements_text(m."member_mk_ids")::integer))
                LEFT JOIN members_mk_individual_committees c
                    ON c."mk_individual_id" = f."mk_individual_id" AND c.finish_date IS NULL
                LEFT JOIN members_mk_individual_faction_chairpersons ch
                    ON ch."mk_individual_id" = f."mk_individual_id"
                LEFT JOIN (
                    SELECT 
                        jsonb_array_elements_text(m.member_mk_ids)::integer AS member_mk_id,
                        array_agg(DISTINCT m.knesset) AS knesset_array
                    FROM members_faction_memberships m
                    GROUP BY member_mk_id
                ) kns ON f."mk_individual_id" = kns.member_mk_id
                LEFT JOIN (
                  SELECT members_presence.mk_id, members_presence.year, SUM(members_presence.total_attended_hours) AS total_attended_hours
                  FROM members_presence
                  GROUP BY members_presence.mk_id, members_presence.year
                ) AS members_presence
                ON f."mk_individual_id" = members_presence.mk_id
                WHERE m.finish_date = CURRENT_DATE AND f."{id_field}"={id}
                GROUP BY f."{id_field}", m."faction_name", f."FirstName", f."LastName", f."GenderDesc", f."IsCurrent", f."Email", f."altnames", f."mk_individual_photo", ch."mk_individual_id", kns."knesset_array";
    """
    data = DB.get_fully_today_kns_member(query, (id,))
    if isinstance(data, Exception):
        status_code = 404 if str(data)=='No row found' else 400
        return {'success': False, 'data' :str(data)},status_code 

    return {'success': True, 'data' :data }, status_code 


        
if __name__ == "__main__":
    app.run(debug=True)
