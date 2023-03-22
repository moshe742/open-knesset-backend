import os


OKNESSET_DB_HOST = os.environ.get('OKNESSET_DB_HOST') or 'localhost'
OKNESSET_DB_PORT = int(os.environ.get('OKNESSET_DB_PORT') or '5432')
OKNESSET_DB_NAME = os.environ.get('OKNESSET_DB_NAME') or 'postgres'
OKNESSET_DB_USER = os.environ.get('OKNESSET_DB_USER') or 'postgres'
OKNESSET_DB_PASSWORD = os.environ.get('OKNESSET_DB_PASSWORD') or '123456'
