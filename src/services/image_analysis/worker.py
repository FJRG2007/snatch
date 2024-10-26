from .text_ocr.recognizer import main as ocr
from .facial_dec_rec.detector import main as detector

def main(lang, saveonfile):
    detector(saveonfile)
    ocr(lang, saveonfile)