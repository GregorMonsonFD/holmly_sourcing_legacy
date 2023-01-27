from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.utils import ImageReader
from rightmove_image_extract import scrape_images
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

def table_handler(elements, link, colours):
    image_list = scrape_images(link)
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

    image_data = []

    for i in range(5):
        image_data.append(Image(image_list[i], thumbnail_x, thumbnail_y))


    for rank in range(10):
        data = []
        full_address = "123 Falkirk Bolevard"
        city = "Falkirk"
        postcode = "FK1 1AA"
        price = "£123,456"
        down_payment = "£12,345"
        monthly_interest = "£1000"
        estimated_rent = "£1500"
        profit = "£500"
        property_yield = "5.0%"

        rows = [

            ["Rank: ", f"{rank + 1}", "Full Address: ", f"{full_address}, {postcode}", "placeholder", "Price: ", price]
            , ["image", "image_2", "image_3", "image_2", "image_3", "Down Payment: ", down_payment]
            , ["placeholder", "placeholder", "placeholder", "placeholder", "placeholder", "Interest: ", monthly_interest]
            , ["placeholder", "placeholder", "placeholder", "placeholder", "placeholder", "Rent: ", estimated_rent]
            , ["placeholder", "placeholder", "placeholder", "placeholder", "placeholder", "Profit: ", profit]
            , [f'<link href="{link}" color="blue"><u>Rightmove Link</u></link>', "placeholder", "placeholder", "placeholder", "placeholder", "Yield: ", property_yield]
        ]

        for i, row in enumerate(rows):
            formatted_row = row_maker(row, column_style, font_size)

            if i == 1:

                for image_index in range(5):
                    formatted_row[image_index] = image_data[image_index]

            data.append(formatted_row)

        table = Table(data, colWidths=[75, 75, 75, 75, 95, 75, 75])

        table_style_list = [
            ('ALIGN', (0, 0), (-3, -1), 'CENTER'),
            ('ALIGN', (0, 1), (4, 1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (5, 0), (6, 5), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colours.gc('colorGreen0')), #colorGreen0Transparent
            ('LINEBELOW', (0, 0), (-1, -1), 1, colours.gc('colorGreen0')),
            ('SPAN', (3, 0), (4, 0)),
            ('SPAN', (0, 1), (0, 4)),
            ('SPAN', (1, 1), (1, 4)),
            ('SPAN', (2, 1), (2, 4)),
            ('SPAN', (3, 1), (3, 4)),
            ('SPAN', (4, 1), (4, 4)),
            ('SPAN', (1, 5), (4, 5)),
        ]

        for i in range(6):
            if i%2 == 0:
                table_style_list.append(
                    ('BACKGROUND', (0, i), (-1, i), colours.gc('colorGreen0Transparent'))
                )
            else:
                table_style_list.append(
                    ('BACKGROUND', (0, i), (-1, i), colours.gc('colorBlue0Transparent'))
                )

        table_style_list.append(('BACKGROUND', (0, 1), (4, 4), colours.gc('transparent')))
        table_style_list.append(('BACKGROUND', (0, 0), (-1, 0), colours.gc('colorTitleGreen0')))

        table_style = TableStyle(table_style_list)
        table.setStyle(table_style)
        elements.append(KeepTogether(table))
        elements.append(Spacer(10,20))

    return elements