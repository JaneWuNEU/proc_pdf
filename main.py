from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import sys
sys.path.append(".")
import os
from PyPDF2 import PdfFileReader

def get_author_from_meta():
    pdfs = os.listdir("./data")
    i = 0
    for pdf in pdfs:
        pdf_toread = PdfFileReader(open("./data/"+pdf, "rb"))
        pdf_info = pdf_toread.getXmpMetadata()
        author_list = pdf_info.dc_creator
        if len(author_list)==0:
            i = i+1
        else:
            print(pdf)


def get_fellow_list():
    # key => author => excel
    pass
