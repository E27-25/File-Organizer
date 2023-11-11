import pytesseract
from pytesseract import image_to_string

from tika import parser
from PyPDF2 import PdfFileReader

import os
import sys

#import warnings
#import time

def get_text_from_pdf_tika(path_to_pdf):
    """ Get text from PDF [Tika] """
    result = parser.from_file(path_to_pdf)
    #warnings.filterwarnings('ignore')
    return result['content']

def get_text_from_pdf_PyPDF2(path_to_pdf):
    """ Get text from PDF [PyPDF2] """
    #warnings.filterwarnings('ignore')
    reader = PdfFileReader(path_to_pdf)
    pg = reader.numPages
    result = ''
    for i in range(pg):
        result += (reader.getPage(i).extract_text())
    return result

def get_text_from_img(img):
    """ Get text from IMG [Tesseract] """
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    pytesseract.pytesseract.tesseract_cmd = fr'{script_directory}\Tesseract-OCR\tesseract.exe'
    text_ocr = image_to_string(img)
    return text_ocr

if __name__ == '__main__':
    img = 'Test_Data\pic_test.png'
    path_to_pdf = 'Test_Data\String.pdf'

    #t0 = time.monotonic()
    get_text_from_pdf_tika(path_to_pdf)
    #t1 = time.monotonic()
    #print(f"1) tika extract text from pdf (many pg): {t1-t0:.5f}")

    #t0 = time.monotonic()
    print(get_text_from_img(img))
    #t1 = time.monotonic()
    #print(f"2) OCE pytesseractt extract text from img (1 img):: {t1-t0:.5f}")

    #t0 = time.monotonic()
    get_text_from_pdf_PyPDF2(path_to_pdf)
    #t1 = time.monotonic()
    #print(f"3) PyPDF2 extract text from pdf (many pg): {t1-t0:.5f}")
