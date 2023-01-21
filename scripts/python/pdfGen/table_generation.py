from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


def table_handler(elements, colour_1, colour_2):
    text_list = []
    column_headers = ["Test 1", "Test 2", "Test 3", "Test 4", "Test 5"]

    font_size = 8
    centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
    for column in column_headers:
        paragraph_text = f"<font size='{font_size}'><b>{column}</b></font>"
        column_names_paragraph = Paragraph(paragraph_text, centered)
        text_list.append(column_names_paragraph)

    data = [text_list]
    formatted_row = []

    alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                  ParagraphStyle(name="02", alignment=TA_LEFT),
                  ParagraphStyle(name="03", alignment=TA_CENTER),
                  ParagraphStyle(name="04", alignment=TA_CENTER),
                  ParagraphStyle(name="05", alignment=TA_CENTER)]

    for row in range(10):

        row_data = [str(row), "Miércoles, 11 de diciembre de 2019",
                    "17:30", "19:24", "1:54"]

        for index, item in enumerate(row_data):
            text = "<font size='%s'>%s</font>" % (font_size - 1, item)
            paragraph = Paragraph(text, alignStyle[index])
            formatted_row.append(p)

        data.append(formatted_row)
        formatted_row = []

    # Row for total
    totalRow = ["Total de Horas", "", "", "", "30:15"]
    for item in totalRow:
        ptext = "<font size='%s'>%s</font>" % (font_size - 1, item)
        p = Paragraph(ptext, alignStyle[1])
        formatted_row.append(p)
    data.append(formatted_row)

    # print(data)
    table = Table(data, colWidths=[50, 200, 80, 80, 80])
    table_style = TableStyle([  # ('GRID',(0, 0), (-1, -1), 0.5, grey),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
        ('LINEABOVE', (0, 0), (-1, -1), 1, colour_1),
        ('BACKGROUND', (0, 0), (-1, 0), colour_2),
        ('BACKGROUND', (0, -1), (-1, -1), colour_1),
        ('SPAN', (0, -1), (-2, -1))
    ])
    table.setStyle(table_style)
    elements.append(table)

    return elements