# open-knesset-backend

# install:

python -m venv venv

# windows:

venv\Scripts\activate

# macos:

. venv/bin/activate

# install all requirements:

pip install -r requirements.txt

# create file .env:

<!-- export OKNESSET_DB_USER="USER NAME"
export OKNESSET_DB_PASSWORD="PASSWORD"
export OKNESSET_DB_HOST="HOST"
export OKNESSET_DB_PORT="PORT"
export OKNESSET_DB_NAME="postgres" -->

# update the file 
config.py

# execute:

<!-- set FLASK_APP=server.py
flask run -->

uvicorn main:app --reload