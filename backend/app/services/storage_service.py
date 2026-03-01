import os
import uuid
from datetime import datetime
from fastapi import UploadFile
import shutil

UPLOAD_FOLDER = "uploads"


def save_audio_file(file: UploadFile) -> str:
    """
    Saves uploaded audio file to backend/uploads
    Returns saved file path
    """

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    unique_filename = (
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
        f"{uuid.uuid4().hex}_{file.filename}"
    )

    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path