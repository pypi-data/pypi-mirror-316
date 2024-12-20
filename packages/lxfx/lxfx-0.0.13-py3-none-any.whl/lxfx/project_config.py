# project_config.py
import os

# ~/.lxfx/
PROJECT_DIR = os.path.join(os.path.expanduser("~"), ".lxfx")

# ~/.lxfx/data/
DATA_DIR = os.path.join(PROJECT_DIR, "data")

# ~/.lxfx/data/db/
DB_DIR = os.path.join(DATA_DIR, "db")

# ~/.lxfx/data/db/lxfx.db
DB_FILE = os.path.join(DB_DIR, "lxfx.db")

# ~/.lxfx/data/tmp/
TMP_DIR = os.path.join(DATA_DIR, "tmp")

# ~/.lxfx/data/tmp/lxfx.db
TMP_DB_FILE = os.path.join(TMP_DIR, "lxfx.db")

# ~/.lxfx/data/logs/
LOGS_DIR = os.path.join(DATA_DIR, "logs")

# ~/.lxfx/data/logs/lxfx.log
LOGS_FILE = os.path.join(LOGS_DIR, "lxfx.log")

# ~/.lxfx/data/credentials/
CREDENTIALS_DIR = os.path.join(DATA_DIR, "credentials")

# ~/.lxfx/data/credentials/credentials.json
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, "credentials.json")