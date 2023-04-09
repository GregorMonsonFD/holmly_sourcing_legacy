from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.pagesizes import LETTER, inch
from scripts.python.pdfGen.page_format_handler import page_format_handler, colour_handler, front_page, information_page
import pandas as pd

def report_generator(**kwargs):
    ds_nodash = kwargs['ds']

    path = f'/home/eggzo/airflow/tmp_data/holmly_daily_report_{ds_nodash}.pdf'
    input_df = pd.read_csv(f'/home/eggzo/airflow/tmp_data/report_content_{ ds_nodash }.csv', header=None)

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
            Top properties
        """

    elements = information_page(elements, colours, "Top Yield Properties", summary, input_df)

    # Build
    doc = SimpleDocTemplate(path, pagesize=LETTER)
    doc.multiBuild(elements, canvasmaker=page_format_handler)