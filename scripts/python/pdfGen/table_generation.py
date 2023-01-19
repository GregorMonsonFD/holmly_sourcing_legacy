from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

def remoteSessionTableMaker(elements, colour_1, colour_2, colour_3):
    psHeaderText = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                  textColor=colour_1)
    text = 'SESIONES REMOTAS'
    paragraphReportHeader = Paragraph(text, psHeaderText)
    elements.append(paragraphReportHeader)

    spacer = Spacer(10, 22)
    elements.append(spacer)
    """
    Create the line items
    """
    d = []
    textData = ["No.", "Fecha", "Hora Inicio", "Hora Fin", "Tiempo Total"]

    fontSize = 8
    centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
    for text in textData:
        ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
        titlesTable = Paragraph(ptext, centered)
        d.append(titlesTable)

    data = [d]
    lineNum = 1
    formattedLineData = []

    alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                  ParagraphStyle(name="02", alignment=TA_LEFT),
                  ParagraphStyle(name="03", alignment=TA_CENTER),
                  ParagraphStyle(name="04", alignment=TA_CENTER),
                  ParagraphStyle(name="05", alignment=TA_CENTER)]

    for row in range(10):
        lineData = [str(lineNum), "Miércoles, 11 de diciembre de 2019",
                    "17:30", "19:24", "1:54"]
        # data.append(lineData)
        columnNumber = 0
        for item in lineData:
            ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
            p = Paragraph(ptext, alignStyle[columnNumber])
            formattedLineData.append(p)
            columnNumber = columnNumber + 1
        data.append(formattedLineData)
        formattedLineData = []

    # Row for total
    totalRow = ["Total de Horas", "", "", "", "30:15"]
    for item in totalRow:
        ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
        p = Paragraph(ptext, alignStyle[1])
        formattedLineData.append(p)
    data.append(formattedLineData)

    # print(data)
    table = Table(data, colWidths=[50, 200, 80, 80, 80])
    tStyle = TableStyle([  # ('GRID',(0, 0), (-1, -1), 0.5, grey),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
        ('LINEABOVE', (0, 0), (-1, -1), 1, colour_2),
        ('BACKGROUND', (0, 0), (-1, 0), colour_3),
        ('BACKGROUND', (0, -1), (-1, -1), colour_2),
        ('SPAN', (0, -1), (-2, -1))
    ])
    table.setStyle(tStyle)
    elements.append(table)

    return elements