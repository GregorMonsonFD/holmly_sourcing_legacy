from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from page_format_handler import page_format_handler, colour_handler, front_page, information_page

path = 'hello_world.pdf'
styleSheet = getSampleStyleSheet()
colours = colour_handler()
elements = []

# colors - Azul turkeza 367AB
colours.add_colour('colorGreen0', 39, 198, 190, 1)
colours.add_colour('colorTitleGreen0', 39, 198, 200, 0.8)
colours.add_colour('colorGreen0Transparent', 39, 198, 190, 0.07)

colours.add_colour('colorBlue0', 39, 119, 181, 1)
colours.add_colour('colorBlue0Transparent', 39, 119, 181, 0.07)

colours.add_colour('transparent', 255, 255, 255, 1)

elements = front_page(elements)

summary = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """

elements = information_page(elements, colours, "Top Properties", summary)

# Build
doc = SimpleDocTemplate(path, pagesize=LETTER)
doc.multiBuild(elements, canvasmaker=page_format_handler)