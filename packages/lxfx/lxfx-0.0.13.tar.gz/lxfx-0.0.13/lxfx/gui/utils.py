from lxfx.project_config import TMP_DIR

import os
import uuid

def generate_random_file_path(ext: str):
    random_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(TMP_DIR, random_filename)
