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
        This is a test description, if you are reading this you
        are a part of a select few who see my project in it's
        infancy. Infancy is a great word because this project
        requires a lot of attention hand holding and is draining
        . I hope you read this and sympathise
        with me. -Gregor
    """

elements = information_page(elements, colours.gc(0), colours.gc(3), "Top Properties", summary)

# Build
doc = SimpleDocTemplate(path, pagesize=LETTER)
doc.multiBuild(elements, canvasmaker=page_format_handler)