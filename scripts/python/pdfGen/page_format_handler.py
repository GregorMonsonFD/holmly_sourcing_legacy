from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

def front_page(elements):
    img = Image('sps.png', kind='proportional')
    img.drawHeight = 0.5 * inch
    img.drawWidth = 2.4 * inch
    img.hAlign = 'LEFT'
    elements.append(img)

    spacer = Spacer(30, 100)
    elements.append(spacer)

    img = Image('sps.png')
    img.drawHeight = 2.5 * inch
    img.drawWidth = 5.5 * inch
    elements.append(img)

    spacer = Spacer(10, 250)
    elements.append(spacer)

    psDetalle = ParagraphStyle('summary', fontSize=10, leading=14, justifyBreaks=1, alignment=TA_LEFT,
                               justifyLastLine=1)
    text = """Scottish Property Sourcing Test Report<br/>
    Report Type: Testing Formatting<br/>
    Publication Date: 01-Jan-2023<br/>
    """
    paragraphReportSummary = Paragraph(text, psDetalle)
    elements.append(paragraphReportSummary)
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
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        self.drawImage("sps.png", self.width - inch * 8 - 5, self.height - 50, width=100, height=25,
                       preserveAspectRatio=True)
        self.drawImage("sps.png", self.width - inch * 2, self.height - 50, width=100, height=25,
                       preserveAspectRatio=True, mask='auto')
        self.line(30, 740, LETTER[0] - 50, 740)
        self.line(66, 78, LETTER[0] - 66, 78)
        self.setFont('Helvetica', 10)
        self.drawString(LETTER[0] - x, 65, page)
        self.restoreState()
