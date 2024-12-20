from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow
from lxfx.models.utils import createLogger
from lxfx.project_config import PROJECT_DIR, DATA_DIR, DB_DIR, TMP_DIR, LOGS_DIR, CREDENTIALS_DIR
import sys
import os
import time
import logging

def create_log_files():
    models_log_file = os.path.join(LOGS_DIR, f"models_{time.strftime('%Y-%m-%d-%H-%M-%S')}.log") 
    gui_log_file = os.path.join(LOGS_DIR, f"gui_{time.strftime('%Y-%m-%d-%H-%M-%S')}.log") 
    console_log_file = os.path.join(LOGS_DIR, f"console_{time.strftime('%Y-%m-%d-%H-%M-%S')}.log")
    db_log_file = os.path.join(LOGS_DIR, f"db_{time.strftime('%Y-%m-%d-%H-%M-%S')}.log")
    credentials_log_file = os.path.join(LOGS_DIR, f"credentials_{time.strftime('%Y-%m-%d-%H-%M-%S')}.log")
    dataCollection_log_file = os.path.join(LOGS_DIR, f"dataCollection_{time.strftime('%Y-%m-%d-%H-%M-%S')}.log")

    # create log files
    open(models_log_file, "w").close()
    open(gui_log_file, "w").close()
    open(console_log_file, "w").close()
    open(db_log_file, "w").close()
    open(credentials_log_file, "w").close()
    open(dataCollection_log_file, "w").close()

    return models_log_file, gui_log_file, console_log_file, db_log_file, credentials_log_file, dataCollection_log_file

def initializeApplication():
    # Create directories if they don't exist
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)

    # create log files
    create_log_files()

if __name__ == '__main__':
    initializeApplication()
    # create necessary loggers 
    MODELS_LOG_FILE,GUI_LOG_FILE, CONSOLE_LOG_FILE, DB_LOG_FILE, CREDENTIALS_LOG_FILE, DATA_COLLECTION_LOG_FILE = create_log_files()
    console_logger = createLogger(is_consoleLogger=True, log_level=logging.INFO, name="console")

    models_logger = createLogger(log_level=logging.INFO, filename=MODELS_LOG_FILE, name="models")
    gui_logger = createLogger(log_level=logging.INFO, filename=GUI_LOG_FILE, name="gui")
    console_logger = createLogger(log_level=logging.INFO, filename=CONSOLE_LOG_FILE, name="console")
    db_logger = createLogger(log_level=logging.INFO, filename=DB_LOG_FILE, name="db")
    credentials_logger = createLogger(log_level=logging.INFO, filename=CREDENTIALS_LOG_FILE, name="credentials")
    dataCollection_logger = createLogger(log_level=logging.INFO, filename=DATA_COLLECTION_LOG_FILE, name="dataCollection")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
