from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from page_format_handler import page_format_handler, colour_handler, front_page, information_page

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

summary = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """

elements = information_page(elements, colours.gc(0), colours.gc(3), "Top Properties", summary)

# Build
doc = SimpleDocTemplate(path, pagesize=LETTER)
doc.multiBuild(elements, canvasmaker=page_format_handler)