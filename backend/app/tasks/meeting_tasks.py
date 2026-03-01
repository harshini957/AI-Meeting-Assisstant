from app.core.celery_app import celery
from app.core.database import SessionLocal
from app.models.meeting import Meeting
from app.services.deepgram_service import transcribe_audio
from app.services.gemini_service import generate_action_items


@celery.task
def process_meeting(meeting_id: str):
    db = SessionLocal()
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

        if not meeting:
            return

        # Step 1: Transcribe
        transcript = transcribe_audio(meeting.audio_path)
        meeting.transcript = transcript
        db.commit()

        # Step 2: Generate Action Items
        action_items = generate_action_items(transcript)
        meeting.action_items = action_items
        meeting.status = "completed"

        db.commit()

    except Exception as e:
        meeting.status = "failed"
        db.commit()
        print("Processing error:", e)

    finally:
        db.close()