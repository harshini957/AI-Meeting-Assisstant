from deepgram import DeepgramClient, PrerecordedOptions
from app.core.config import settings


def transcribe_audio(file_path: str) -> str:
    client = DeepgramClient(settings.DEEPGRAM_API_KEY)

    with open(file_path, "rb") as audio:
        buffer_data = audio.read()

    options = PrerecordedOptions(
        model="nova-2",
        smart_format=True
    )

    response = client.listen.prerecorded.v("1").transcribe_file(
        {"buffer": buffer_data},
        options
    )

    transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]

    return transcript