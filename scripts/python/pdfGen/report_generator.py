from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.graphics.shapes import Line, LineShape, Drawing
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

    def get_colour(self, index):
        return(self.colour_theme[index])

path = 'hello_world.pdf'
styleSheet = getSampleStyleSheet()
colours = colour_handler()
elements = []

# colors - Azul turkeza 367AB3
#colorOhkaGreen0
#colorOhkaGreen1
#colorOhkaGreen2
#colorOhkaGreenLineas

colours.add_colour(45, 166, 153)
colours.add_colour(182, 227, 166)
colours.add_colour(140, 222, 192)
colours.add_colour(50, 140, 140)

#colorOhkaBlue0
#colorOhkaBlue1

colours.add_colour(54, 122, 179)
colours.add_colour(122, 180, 225)

elements = front_page(elements)
elements = header(elements, True, colours.get_colour(0), colours.get_colour(3))
#elements = remoteSessionTableMaker(elements, colours.get_colour(4), colours.get_colour(5), colours.get_colour(3))
#nextPagesHeader(False, colours.get_colour(0), colours.get_colour(3))
#elements = remoteSessionTableMaker(elements, colours.get_colour(4), colours.get_colour(5), colours.get_colour(3))
#nextPagesHeader(False, colours.get_colour(0), colours.get_colour(3))
#elements = remoteSessionTableMaker(elements, colours.get_colour(4), colours.get_colour(5), colours.get_colour(3))
#nextPagesHeader(False, colours.get_colour(0), colours.get_colour(3))
#elements = remoteSessionTableMaker(elements, colours.get_colour(4), colours.get_colour(5), colours.get_colour(3))
# Build
print(elements)
doc = SimpleDocTemplate(path, pagesize=LETTER)
doc.multiBuild(elements, canvasmaker=page_format_handler)