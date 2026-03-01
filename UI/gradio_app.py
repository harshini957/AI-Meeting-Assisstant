# # import requests
# # import gradio as gr
# # import time
# # import os
# #
# # BACKEND_URL = "http://127.0.0.1:8002"
# #
# #
# # def upload_and_process(audio_path):
# #     if audio_path is None:
# #         return (
# #             "Please record audio first.",
# #             None,
# #             None,
# #             gr.update(visible=False)
# #         )
# #
# #     # Step 1: Upload
# #     with open(audio_path, "rb") as f:
# #         files = {"file": ("audio.wav", f, "audio/wav")}
# #         response = requests.post(f"{BACKEND_URL}/meetings/", files=files)
# #
# #     if response.status_code != 200:
# #         return (
# #             "Upload failed.",
# #             None,
# #             None,
# #             gr.update(visible=False)
# #         )
# #
# #     meeting_id = response.json()["meeting_id"]
# #
# #     # Step 2: Trigger Processing
# #     requests.post(f"{BACKEND_URL}/meetings/{meeting_id}/process")
# #
# #     return (
# #         "Processing started...",
# #         meeting_id,
# #         None,
# #         gr.update(visible=False)
# #     )
# #
# #
# # def poll_status(meeting_id):
# #     if not meeting_id:
# #         return None, "No meeting found.", gr.update(visible=False)
# #
# #     # Poll every 3 seconds (max 20 attempts)
# #     for _ in range(20):
# #         time.sleep(3)
# #         response = requests.get(f"{BACKEND_URL}/meetings/{meeting_id}/status")
# #
# #         if response.status_code != 200:
# #             return None, "Error checking status.", gr.update(visible=False)
# #
# #         status = response.json()["status"]
# #
# #         if status == "completed":
# #             # Fetch action items
# #             action_response = requests.get(
# #                 f"{BACKEND_URL}/meetings/{meeting_id}/action-items"
# #             )
# #
# #             if action_response.status_code == 200:
# #                 action_items = action_response.json()["action_items"]
# #                 return (
# #                     action_items,
# #                     "Processing completed.",
# #                     gr.update(visible=True)
# #                 )
# #
# #         if status == "failed":
# #             return None, "Processing failed.", gr.update(visible=False)
# #
# #     return None, "Still processing... Try again.", gr.update(visible=False)
# #
# #
# # def download_pdf(meeting_id):
# #     response = requests.get(
# #         f"{BACKEND_URL}/meetings/{meeting_id}/download-pdf"
# #     )
# #
# #     if response.status_code != 200:
# #         return None
# #
# #     file_path = f"{meeting_id}.pdf"
# #
# #     with open(file_path, "wb") as f:
# #         f.write(response.content)
# #
# #     return file_path
# #
# #
# # with gr.Blocks() as demo:
# #     gr.Markdown("# 🎙️ AI Meeting Assistant")
# #
# #     meeting_id_state = gr.State()
# #
# #     audio_input = gr.Audio(
# #         sources=["microphone"],
# #         type="filepath",
# #         label="Record your meeting"
# #     )
# #
# #     process_button = gr.Button("Upload & Generate Action Items")
# #
# #     status_output = gr.Textbox(label="Status")
# #
# #     action_output = gr.JSON(label="Action Items")
# #
# #     download_file = gr.File(label="Download PDF", visible=False)
# #
# #     # Step 1: Upload & trigger processing
# #     process_button.click(
# #         fn=upload_and_process,
# #         inputs=audio_input,
# #         outputs=[
# #             status_output,
# #             meeting_id_state,
# #             action_output,
# #             download_file
# #         ]
# #     ).then(
# #         fn=poll_status,
# #         inputs=meeting_id_state,
# #         outputs=[
# #             action_output,
# #             status_output,
# #             download_file
# #         ]
# #     )
# #
# #     # Step 2: Download PDF
# #     download_file.change(
# #         fn=download_pdf,
# #         inputs=meeting_id_state,
# #         outputs=download_file
# #     )
# #
# # demo.launch()
#
# import requests
# import gradio as gr
# import time
# import os
#
# BACKEND_URL = "http://127.0.0.1:8002"
#
#
# def upload_and_process(audio_path):
#     if audio_path is None:
#         return "Please record audio first.", None, None, gr.update(visible=False)
#
#     with open(audio_path, "rb") as f:
#         files = {"file": ("audio.wav", f, "audio/wav")}
#         response = requests.post(f"{BACKEND_URL}/meetings/", files=files)
#
#     if response.status_code != 200:
#         return "Upload failed.", None, None, gr.update(visible=False)
#
#     meeting_id = response.json()["meeting_id"]
#
#     requests.post(f"{BACKEND_URL}/meetings/{meeting_id}/process")
#
#     return "Processing started...", meeting_id, None, gr.update(visible=False)
#
#
# def poll_status(meeting_id):
#     if not meeting_id:
#         return None, "No meeting found.", gr.update(visible=False)
#
#     for _ in range(20):
#         time.sleep(3)
#         response = requests.get(f"{BACKEND_URL}/meetings/{meeting_id}/status")
#
#         if response.status_code != 200:
#             return None, "Error checking status.", gr.update(visible=False)
#
#         status = response.json()["status"]
#
#         if status == "completed":
#             action_response = requests.get(
#                 f"{BACKEND_URL}/meetings/{meeting_id}/action-items"
#             )
#
#             if action_response.status_code == 200:
#                 action_items = action_response.json()["action_items"]
#                 return action_items, "Processing completed.", gr.update(visible=True)
#
#         if status == "failed":
#             return None, "Processing failed.", gr.update(visible=False)
#
#     return None, "Still processing... Try again.", gr.update(visible=False)
#
#
# def download_pdf(meeting_id):
#     if not meeting_id:
#         return None
#
#     response = requests.get(
#         f"{BACKEND_URL}/meetings/{meeting_id}/download-pdf"
#     )
#
#     # Check HTTP status
#     if response.status_code != 200:
#         print("PDF request failed:", response.status_code)
#         return None
#
#     # Check if response actually contains PDF data
#     if not response.content or len(response.content) < 100:
#         print("PDF content is empty or too small.")
#         return None
#
#     file_path = f"{meeting_id}.pdf"
#
#     with open(file_path, "wb") as f:
#         f.write(response.content)
#
#     # Double check file exists and size > 0
#     if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
#         print("File was not written correctly.")
#         return None
#
#     return file_path
#
#
# with gr.Blocks() as demo:
#     gr.Markdown("# 🎙️ AI Meeting Assistant")
#
#     meeting_id_state = gr.State()
#
#     audio_input = gr.Audio(
#         sources=["microphone"],
#         type="filepath",
#         label="Record your meeting"
#     )
#
#     process_button = gr.Button("Upload & Generate Action Items")
#
#     status_output = gr.Textbox(label="Status")
#     action_output = gr.JSON(label="Action Items")
#
#     # 👇 This is the important part
#     download_button = gr.Button("Download PDF", visible=False)
#     download_file = gr.File(label="Your PDF will appear here")
#
#     # Upload + Process
#     process_button.click(
#         fn=upload_and_process,
#         inputs=audio_input,
#         outputs=[
#             status_output,
#             meeting_id_state,
#             action_output,
#             download_button   # 👈 controls visibility
#         ]
#     ).then(
#         fn=poll_status,
#         inputs=meeting_id_state,
#         outputs=[
#             action_output,
#             status_output,
#             download_button
#         ]
#     )
#
#     #  This actually downloads
#     download_button.click(
#         fn=download_pdf,
#         inputs=meeting_id_state,
#         outputs=download_file
#     )
#
# demo.launch()

import requests
import gradio as gr
import time
import os
import tempfile

BACKEND_URL = "http://127.0.0.1:8002"


def upload_and_process(audio_path):
    if audio_path is None:
        return "Please record audio first.", None, None, gr.update(visible=False)

    with open(audio_path, "rb") as f:
        files = {"file": ("audio.wav", f, "audio/wav")}
        response = requests.post(f"{BACKEND_URL}/meetings/", files=files)

    if response.status_code != 200:
        return "Upload failed.", None, None, gr.update(visible=False)

    meeting_id = response.json()["meeting_id"]

    requests.post(f"{BACKEND_URL}/meetings/{meeting_id}/process")

    return "Processing started...", meeting_id, None, gr.update(visible=False)


def poll_status(meeting_id):
    if not meeting_id:
        return None, "No meeting found.", gr.update(visible=False)

    for _ in range(20):
        time.sleep(3)
        response = requests.get(f"{BACKEND_URL}/meetings/{meeting_id}/status")

        if response.status_code != 200:
            return None, "Error checking status.", gr.update(visible=False)

        status = response.json()["status"]

        if status == "completed":
            action_response = requests.get(
                f"{BACKEND_URL}/meetings/{meeting_id}/action-items"
            )
            if action_response.status_code == 200:
                action_items = action_response.json()["action_items"]
                return action_items, "Processing completed.", gr.update(visible=True)

        if status == "failed":
            return None, "Processing failed.", gr.update(visible=False)

    return None, "Still processing... Try again.", gr.update(visible=False)


def download_pdf(meeting_id):
    """Called by the Download PDF button. Fetches PDF and returns a local file path."""
    if not meeting_id:
        print("No meeting_id available.")
        return None

    print(f"Fetching PDF for meeting: {meeting_id}")

    response = requests.get(f"{BACKEND_URL}/meetings/{meeting_id}/download-pdf")

    if response.status_code != 200:
        print(f"PDF request failed with status: {response.status_code}, body: {response.text}")
        return None

    if not response.content or len(response.content) < 100:
        print("PDF content is empty or too small.")
        return None

    # Save to a temp file that Gradio can serve
    file_path = os.path.join(os.getcwd(), f"meeting_{meeting_id}.pdf")

    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"PDF saved to: {file_path} ({os.path.getsize(file_path)} bytes)")
    return file_path


def load_existing_meeting(meeting_id_input):
    """Lets user load a completed meeting by ID without re-processing."""
    if not meeting_id_input or not meeting_id_input.strip():
        return None, "Please enter a meeting ID.", None, gr.update(visible=False)

    meeting_id = meeting_id_input.strip()

    # Check status
    status_response = requests.get(f"{BACKEND_URL}/meetings/{meeting_id}/status")
    if status_response.status_code != 200:
        return None, "Meeting not found.", None, gr.update(visible=False)

    status = status_response.json()["status"]

    if status != "completed":
        return None, f"Meeting status is '{status}', not completed yet.", None, gr.update(visible=False)

    # Fetch action items
    action_response = requests.get(f"{BACKEND_URL}/meetings/{meeting_id}/action-items")
    if action_response.status_code != 200:
        return None, "Failed to fetch action items.", None, gr.update(visible=False)

    action_items = action_response.json()["action_items"]
    return meeting_id, "Meeting loaded successfully.", action_items, gr.update(visible=True)


with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ AI Meeting Assistant")

    meeting_id_state = gr.State()

    # ── Tab 1: Record & Process ──────────────────────────────────────────────
    with gr.Tab("Record Meeting"):
        audio_input = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Record your meeting"
        )
        process_button = gr.Button("Upload & Generate Action Items", variant="primary")
        status_output = gr.Textbox(label="Status", interactive=False)
        action_output = gr.JSON(label="Action Items")

        # Shows after processing completes
        # download_button = gr.Button("⬇️ Download PDF", visible=False, variant="secondary")
        # download_file = gr.File(label="Your PDF (click the filename to download)")
        #
        # process_button.click(
        #     fn=upload_and_process,
        #     inputs=audio_input,
        #     outputs=[status_output, meeting_id_state, action_output, download_button]
        # ).then(
        #     fn=poll_status,
        #     inputs=meeting_id_state,
        #     outputs=[action_output, status_output, download_button]
        # )
        #
        # download_button.click(
        #     fn=download_pdf,
        #     inputs=meeting_id_state,
        #     outputs=download_file
        # )

    # ── Tab 2: Load Existing Meeting ─────────────────────────────────────────
    with gr.Tab("Load Existing Meeting"):
        gr.Markdown("Already have a meeting ID? Enter it below to load results and download the PDF.")

        meeting_id_input = gr.Textbox(label="Meeting ID", placeholder="Paste your meeting UUID here")
        load_button = gr.Button("Load Meeting", variant="primary")

        load_status = gr.Textbox(label="Status", interactive=False)
        load_action_output = gr.JSON(label="Action Items")

        # Always visible in this tab — no need to hide it
        load_download_button = gr.Button("⬇️ Download PDF", visible=False, variant="secondary")
        load_download_file = gr.File(label="Your PDF (click the filename to download)")

        load_button.click(
            fn=load_existing_meeting,
            inputs=meeting_id_input,
            outputs=[meeting_id_state, load_status, load_action_output, load_download_button]
        )

        load_download_button.click(
            fn=download_pdf,
            inputs=meeting_id_state,
            outputs=load_download_file
        )

demo.launch()