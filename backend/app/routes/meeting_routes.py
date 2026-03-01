from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.meeting import Meeting
from app.services.storage_service import save_audio_file
from app.tasks.meeting_tasks import process_meeting
from sqlalchemy import and_
from app.services.pdf_service import generate_action_items_pdf
from starlette.responses import StreamingResponse
from fastapi.responses import Response

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.post("/")
def create_meeting(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files allowed")

    # Save file
    file_path = save_audio_file(file)

    # Create DB record
    meeting = Meeting(
        audio_path=file_path,
        status="uploaded"
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return {
        "meeting_id": str(meeting.id),
        "status": meeting.status
    }


@router.post("/{meeting_id}/process")
def trigger_processing(meeting_id: str, db: Session = Depends(get_db)):
    updated_rows = (
        db.query(Meeting)
        .filter(Meeting.id == meeting_id)
        .filter(Meeting.status == "uploaded")
        .update({"status": "processing"})
    )

    db.commit()


    if updated_rows == 0:
        raise HTTPException(
            status_code=400,
            detail="Meeting not found or already processing/completed"
        )

    process_meeting.delay(meeting_id)

    return {
        "message": "Processing started",
        "status": "processing"
    }

#  Get Status
@router.get("/{meeting_id}/status")
def get_status(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return {"status": meeting.status}


# Get Action Items
@router.get("/{meeting_id}/action-items")
def get_action_items(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if meeting.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Processing not completed yet"
        )

    return {"action_items": meeting.action_items}


# Get Transcript (Optional)
@router.get("/{meeting_id}/transcript")
def get_transcript(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return {"transcript": meeting.transcript}


# @router.get("/{meeting_id}/download-pdf")
# def download_pdf(meeting_id: str, db: Session = Depends(get_db)):
#     meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
#
#     if not meeting:
#         raise HTTPException(status_code=404, detail="Meeting not found")
#
#     if meeting.status != "completed":
#         raise HTTPException(status_code=400, detail="Processing not completed yet")
#
#     pdf_buffer = generate_action_items_pdf(
#         meeting_id,
#         meeting.action_items
#     )
#
#     return StreamingResponse(
#         pdf_buffer,
#         media_type="application/pdf",
#         headers={
#             "Content-Disposition": f"attachment; filename=meeting_{meeting_id}.pdf"
#         }
#     )

@router.get("/{meeting_id}/download-pdf")
def download_pdf(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if meeting.status != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed yet")

    pdf_buffer = generate_action_items_pdf(meeting_id, meeting.action_items)
    pdf_bytes = pdf_buffer.read()  # read all bytes upfront

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=meeting_{meeting_id}.pdf"
        }
    )