from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def generate_action_items_pdf(meeting_id: str, action_items: list):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("AI Meeting Assistant - Action Items", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    if not action_items or not isinstance(action_items, list):
        elements.append(Paragraph("No action items found.", styles["Normal"]))
        doc.build(elements)
        buffer.seek(0)
        return buffer

    # 🔥 Dynamically extract headers from JSON keys
    headers = list(action_items[0].keys())

    # Table data (header row first)
    table_data = [headers]

    for item in action_items:
        row = [str(item.get(key, "")) for key in headers]
        table_data.append(row)

    # Create table
    table = Table(table_data, repeatRows=1)

    # Add borders + styling
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),  # Header background
        ("GRID", (0, 0), (-1, -1), 1, colors.black),         # Borders
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer