import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_LOG_FILE = os.path.join(BASE_DIR, "activity_log.txt")


def log_activity(action, record_id, log_file=None):
    file_path = log_file or DEFAULT_LOG_FILE
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{action}: {record_id}\n")
