from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

pdfmetrics.registerFont(TTFont('Poppins-Bold', './fonts/Poppins-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Light', './fonts/Poppins-Light.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Medium', './fonts/Poppins-Medium.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Regular', './fonts/Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-SemiBold', './fonts/Poppins-SemiBold.ttf'))

def front_page(elements):

    title_style = ParagraphStyle('title', fontName='Poppins-Bold', fontSize=70, leading=72,
                                 alignment=TA_LEFT, leftIndent=0)

    subtitle_style = ParagraphStyle('title', fontName='Poppins-SemiBold', fontSize=40, leading=72,
                                 alignment=TA_LEFT, leftIndent=0)

    summary_style = ParagraphStyle('summary', fontName='Poppins-Light', fontSize=12, leading=20, justifyBreaks=1,
                                   alignment=TA_LEFT, justifyLastLine=1)

    title_text = 'Scottish Property Sourcing'

    subtitle_text = 'Test Report'

    summary_text = """
    Report Type: Testing Formatting<br/>
    Publication Date: 01-Jan-2023<br/>
    """

    title = Paragraph(title_text, title_style)
    elements.append(title)

    spacer = Spacer(10, 185)
    elements.append(spacer)

    subtitle = Paragraph(subtitle_text, subtitle_style)
    elements.append(subtitle)

    spacer = Spacer(10, 10)
    elements.append(spacer)

    paragraph_report_summary = Paragraph(summary_text, summary_style)
    elements.append(paragraph_report_summary)
    elements.append(PageBreak())

    return elements

def header(elements, is_second_page, colour_1, colour_2):
    if is_second_page:
        psHeaderText = ParagraphStyle('Hed0', fontSize=16, alignment=TA_LEFT, borderWidth=3,
                                      textColor=colour_1)
        text = 'Top Properties:'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        elements.append(paragraphReportHeader)

        spacer = Spacer(10, 10)
        elements.append(spacer)

        d = Drawing(500, 1)
        line = Line(-15, 0, 483, 0)
        line.strokeColor = colour_2
        line.strokeWidth = 2
        d.add(line)
        elements.append(d)

        spacer = Spacer(10, 1)
        elements.append(spacer)

        d = Drawing(500, 1)
        line = Line(-15, 0, 483, 0)
        line.strokeColor = colour_2
        line.strokeWidth = 0.5
        d.add(line)
        elements.append(d)

        spacer = Spacer(10, 22)
        elements.append(spacer)

        return elements

class page_format_handler(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.width, self.height = LETTER

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if (self._pageNumber > 1):
                self.draw_canvas(page_count)
            elif (self._pageNumber <= 1):
                self.draw_front_page()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        copyright = f'© 2022 - {datetime.today().year} Holmly Ltd. All Rights Reserved'
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        self.setFont('Poppins-Bold', 16)
        self.drawImage("sps_logo.png", self.width - inch * 9 + 30, self.height - 45, width=100, height=35,
                       preserveAspectRatio=True, mask='auto')
        self.drawString(66, 755, "Scottish Property Sourcing")
        self.line(30, 740, LETTER[0] - 50, 740)
        self.line(66, 78, LETTER[0] - 66, 78)
        self.setFont('Poppins-Light', 10)
        self.drawString(LETTER[0] - x, 65, page)
        self.drawString(66, 65, copyright)
        self.restoreState()

    def draw_front_page(self):
        self.saveState()
        self.setFont('Poppins-Light', 10)
        self.drawImage("sps_logo.png", inch * 4 - 20, -inch * 0.3, width=700, height=700,
                       preserveAspectRatio=True, mask='auto')
        self.restoreState()
