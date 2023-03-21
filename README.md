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

export DB_USERNAME="USER NAME"
export DB_PASSWORD="PASSWORD"
export HOST="HOST"
export PORT="PORT"
export DATABASE="postgres"

# execute:

set FLASK_APP=server.py
flask run
