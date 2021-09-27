from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def extract_pdf_contents(path):
    output_string = StringIO()
    with open(path, 'rb') as input_pdf:
        parser = PDFParser(input_pdf)
        document = PDFDocument(parser)
        resource_manager = PDFResourceManager()
        converter = TextConverter(resource_manager, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, converter)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
    for line in output_string.getvalue().splitlines():
        if line.strip():
            print(line)
