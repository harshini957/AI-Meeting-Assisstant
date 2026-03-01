# # from celery import Celery
# #
# # celery = Celery(
# #     "ai_meeting_assistant",
# #     broker="redis://localhost:6379/0",
# #     backend="redis://localhost:6379/0"
# # )
# #
# # celery.conf.task_routes = {
# #     "app.tasks.meeting_tasks.process_meeting": {"queue": "meeting_queue"}
# # }
#
# from celery import Celery
#
# celery = Celery(
#     "ai_meeting_assistant",
#     broker="redis://localhost:6379/0",
#     backend="redis://localhost:6379/0"
# )
#
# celery.conf.update(
#     task_serializer="json",
#     accept_content=["json"],
#     result_serializer="json",
#     timezone="UTC",
#     enable_utc=True,
# )
#
# # Optional: auto-discover tasks
# celery.autodiscover_tasks(["app.tasks"])

from celery import Celery

celery = Celery(
    "ai_meeting_assistant",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# 🔥 ADD THIS LINE
celery.autodiscover_tasks(["app.tasks"])

import app.tasks.meeting_tasks