from .facial_dec_rec.detector import main as detector
# from .facial_dec_rec.recognizer import main as recognizer
from .text_ocr.recognizer import main as ocr

def main(lang, saveonfile):
    detector(saveonfile)
    ocr(lang, saveonfile)