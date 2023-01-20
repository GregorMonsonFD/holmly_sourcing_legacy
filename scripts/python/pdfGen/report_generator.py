from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.lib.colors import Color
from page_format_handler import page_format_handler, front_page, header
from table_generation import remoteSessionTableMaker


class colour_handler():

    def __init__(self):
        self.colour_theme = []

    def add_colour(self, r, g, b):
        self.colour_theme.append(
            Color((r / 255), (g / 255), (b / 255), 1)
        )

    def gc(self, index):
        return(self.colour_theme[index])

path = 'hello_world.pdf'
styleSheet = getSampleStyleSheet()
colours = colour_handler()
elements = []

# colors - Azul turkeza 367AB3

colours.add_colour(45, 166, 153)    #colorOhkaGreen0
colours.add_colour(182, 227, 166)   #colorOhkaGreen1
colours.add_colour(140, 222, 192)   #colorOhkaGreen2
colours.add_colour(50, 140, 140)    #colorOhkaGreenLineas

colours.add_colour(54, 122, 179)    #colorOhkaBlue0
colours.add_colour(122, 180, 225)   #colorOhkaBlue1

elements = front_page(elements)
elements = header(elements, True, colours.gc(0), colours.gc(3))
#elements = remoteSessionTableMaker(elements, colours.gc(4), colours.gc(5), colours.gc(3))
#nextPagesHeader(False, colours.gc(0), colours.gc(3))
#elements = remoteSessionTableMaker(elements, colours.gc(4), colours.gc(5), colours.gc(3))
#nextPagesHeader(False, colours.gc(0), colours.gc(3))
#elements = remoteSessionTableMaker(elements, colours.gc(4), colours.gc(5), colours.gc(3))
#nextPagesHeader(False, colours.gc(0), colours.gc(3))
#elements = remoteSessionTableMaker(elements, colours.gc(4), colours.gc(5), colours.gc(3))
# Build
doc = SimpleDocTemplate(path, pagesize=LETTER)
doc.multiBuild(elements, canvasmaker=page_format_handler)