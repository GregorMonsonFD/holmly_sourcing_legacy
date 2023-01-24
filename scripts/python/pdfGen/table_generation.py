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
    font_size = 8

    column_style =   [ParagraphStyle(name="01", alignment=TA_RIGHT),
                      ParagraphStyle(name="02", alignment=TA_LEFT),
                      ParagraphStyle(name="03", alignment=TA_RIGHT),
                      ParagraphStyle(name="04", alignment=TA_LEFT),
                      ParagraphStyle(name="05", alignment=TA_CENTER),
                      ParagraphStyle(name="06", alignment=TA_RIGHT),
                      ParagraphStyle(name="07", alignment=TA_LEFT),]

    #header_row = row_maker(column_headers, header_style, font_size)

    thumbnail_x = 1*inch
    thumbnail_y = 0.8*inch

    image = Image('https://media.rightmove.co.uk/9k/8449/128204576/8449_FAL220223_IMG_00_0000.jpeg', thumbnail_x, thumbnail_y)
    image_2 = Image('https://media.rightmove.co.uk/9k/8449/128204576/8449_FAL220223_IMG_01_0000.jpeg', thumbnail_x, thumbnail_y)
    image_3 = Image('https://media.rightmove.co.uk/9k/8449/128204576/8449_FAL220223_IMG_02_0000.jpeg', thumbnail_x, thumbnail_y)

    for rank in range(10):
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
        link = "https://www.rightmove.co.uk/properties/128204576#/?channel=RES_BUY"

        #rows = [
        #
        #["image", "image_2", "image_3", "image_2", "image_3", f"Loan Interest:\t{monthly_interest}"]
        #,["placeholder", "placeholder", "placeholder", "placeholder", "placeholder", f"Est. Rent:\t{estimated_rent}"]
        #,["placeholder", f"Rank {i+1}", "Full Address: ", full_address, f"Price: {price}",f"Est. Profit:\t{profit}" ]
        #,["placeholder", "City: ", city, postcode, f"Down Payment: {down_payment}", f"Est. Yield:\t{property_yield}"]
        #
        #]

        rows = [

            ["Rank: ", f"{rank + 1}", "Full Address: ", f"{full_address}, {postcode}", "placeholder", "Price: ", price]
            , ["image", "image_2", "image_3", "image_2", "image_3", "Down Payment: ", down_payment]
            , ["placeholder", "placeholder", "placeholder", "placeholder", "placeholder", "Interest: ", monthly_interest]
            , ["placeholder", "placeholder", "placeholder", "placeholder", "placeholder", "Rent: ", estimated_rent]
            , ["placeholder", "placeholder", "placeholder", "placeholder", "placeholder", "Profit: ", profit]
            , ["Link: ", link, "placeholder", "placeholder", "placeholder", "Yield: ", property_yield]
        ]

        for i, row in enumerate(rows):
            formatted_row = row_maker(row, column_style, font_size)

            if i == 1:
                formatted_row[0] = image_data[0]
                formatted_row[1] = image_data[1]
                formatted_row[2] = image_data[2]
                formatted_row[3] = image_data[1]
                formatted_row[4] = image_data[2]

            data.append(formatted_row)

        table = Table(data, colWidths=[75, 75, 75, 75, 95, 75, 75])
        table_style = TableStyle([
            ('ALIGN', (0, 0), (-3, -1), 'CENTER'),
            ('ALIGN', (0, 1), (4, 1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (5, 0), (6, 5), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colour_1),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colour_2),
            #('BACKGROUND', (0, -1), (-1, -1), colour_1),
            ('SPAN', (3, 0), (4, 0)),
            ('SPAN', (0, 1), (0, 4)),
            ('SPAN', (1, 1), (1, 4)),
            ('SPAN', (2, 1), (2, 4)),
            ('SPAN', (3, 1), (3, 4)),
            ('SPAN', (4, 1), (4, 4)),
            ('SPAN', (1, 5), (4, 5)),
        ])
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(10,20))

    return elements