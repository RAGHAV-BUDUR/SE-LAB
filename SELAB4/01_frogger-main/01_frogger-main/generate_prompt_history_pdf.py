import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

# Register system TrueType font for clean unicode em-dash support
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))

pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prompt_history.pdf')

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=50,
    rightMargin=50,
    topMargin=50,
    bottomMargin=50,
)

styles = getSampleStyleSheet()

header_num_style = ParagraphStyle(
    'HeaderNum',
    fontName='Arial-Bold',
    fontSize=10,
    leading=13,
    alignment=1,
    textColor=colors.black,
)

header_style = ParagraphStyle(
    'HeaderPrompt',
    fontName='Arial-Bold',
    fontSize=10,
    leading=13,
    textColor=colors.black,
)

num_style = ParagraphStyle(
    'RowNum',
    fontName='Arial',
    fontSize=10,
    leading=14,
    alignment=1,
    textColor=colors.black,
)

body_style = ParagraphStyle(
    'RowPrompt',
    fontName='Arial',
    fontSize=10,
    leading=14,
    textColor=colors.black,
)

prompts = [
    (1, 'Task 1 \u2014 Fix Vehicle Collision Detection'),
    (2, 'Task 2 \u2014 Implement Lives and Respawn<br/><br/>Add a 3-life system with appropriate frog respawn behaviour after a collision.'),
    (3, 'Task 3 \u2014 Implement Goal and Score Tracking<br/><br/>Detect successful goal completion and implement score tracking with an appropriate win state.'),
    (4, 'Task 4 \u2014 Add a 30-Second Timer<br/><br/>Add a 30-second countdown for each attempt and handle timeout appropriately'),
]

table_data = [
    [Paragraph('<b>#</b>', header_num_style), Paragraph('<b>Prompt</b>', header_style)]
]

for num, text in prompts:
    table_data.append([
        Paragraph(str(num), num_style),
        Paragraph(text, body_style)
    ])

# Table width: 40 + 472 = 512 pt (fits within 612 pt page width with 50 pt margins)
table = Table(table_data, colWidths=[40, 472])
table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))

doc.build([table])
print(f'PDF generated successfully: {pdf_path}')
