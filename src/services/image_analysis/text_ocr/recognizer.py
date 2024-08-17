import os, easyocr

def main(lang, saveonfile):
    reader = easyocr.Reader([lang])
    result = reader.readtext('example.png')
    for filename in os.listdir("customs/image_analysis"):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            result = reader.readtext(os.path.join("customs/image_analysis", filename))
            print(result)