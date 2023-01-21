from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import inch


def row_maker(row_list: list, styles, font_size):
    text_list = []

    for index, column in enumerate(row_list):
        paragraph_text = f"<font size='{font_size}'><b>{column}</b></font>"

        if not isinstance(styles, list):
            column_names_paragraph = Paragraph(paragraph_text, styles)
        else:
            column_names_paragraph = Paragraph(paragraph_text, styles[index])

        text_list.append(column_names_paragraph)

    return text_list

def table_handler(elements, colour_1, colour_2):
    #column_headers = ["Test 1", "Test 2", "Test 3", "Test 4", "Test 5", "Test 6"]
    font_size = 8
    #header_style = ParagraphStyle(name="centered", alignment=TA_CENTER)

    column_style =   [ParagraphStyle(name="01", alignment=TA_RIGHT),
                      ParagraphStyle(name="02", alignment=TA_LEFT),
                      ParagraphStyle(name="03", alignment=TA_CENTER),
                      ParagraphStyle(name="04", alignment=TA_CENTER),
                      ParagraphStyle(name="05", alignment=TA_CENTER),
                      ParagraphStyle(name="06", alignment=TA_CENTER)]

    #header_row = row_maker(column_headers, header_style, font_size)

    large_thumbnail_x = 1.2*inch
    small_thumbnail_x = large_thumbnail_x/1.4

    large_thumbnail_y = 0.9 * inch
    small_thumbnail_y = large_thumbnail_y / 1.4

    image = Image('https://media.rightmove.co.uk/9k/8449/128204576/8449_FAL220223_IMG_00_0000.jpeg', large_thumbnail_x, large_thumbnail_y)
    image_2 = Image('https://media.rightmove.co.uk/9k/8449/128204576/8449_FAL220223_IMG_01_0000.jpeg', small_thumbnail_x, small_thumbnail_y)
    image_3 = Image('https://media.rightmove.co.uk/9k/8449/128204576/8449_FAL220223_IMG_02_0000.jpeg', small_thumbnail_x, small_thumbnail_y)

    for i in range(3):
        data = []
        image_data = [image, image_2, image_3]
        full_address = "123 Falkirk Bolevard"
        city = "Falkirk"
        postcode = "FK1 1AA"
        price = "£123,456"
        down_payment = "£12,345"
        monthly_interest = "£1000"
        estimated_rent = "£1500"
        profit = "£500"
        property_yield = "5.0%"

        rows = [["image", "image_2", "image_3", "image_2", "image_3", f"Loan Interest:\t{monthly_interest}"]
        ,["placeholder", "placeholder", "placeholder", "placeholder", "placeholder", f"Est. Rent:\t{estimated_rent}"]
        ,["placeholder", f"Rank {i+1}", "Full Address: ", full_address, f"Price: {price}",f"Est. Profit:\t{profit}" ]
        ,["placeholder", "City: ", city, postcode, f"Down Payment: {down_payment}", f"Est. Yield:\t{property_yield}"]]

        for i, row in enumerate(rows):
            formatted_row = row_maker(row, column_style, font_size)

            if i == 0:
                formatted_row[0] = image_data[0]
                formatted_row[1] = image_data[1]
                formatted_row[2] = image_data[2]
                formatted_row[3] = image_data[1]
                formatted_row[4] = image_data[2]

            data.append(formatted_row)

        table = Table(data, colWidths=[100, 90, 90, 90, 100])
        table_style = TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (-1, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colour_1),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colour_2),
            #('BACKGROUND', (0, -1), (-1, -1), colour_1),
            ('SPAN', (0, 0), (0, -1)),
            ('SPAN', (1, 0), (1, 1)),
            ('SPAN', (2, 0), (2, 1)),
            ('SPAN', (3, 0), (3, 1)),
            ('SPAN', (4, 0), (4, 1)),
        ])
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(10,20))

    return elements