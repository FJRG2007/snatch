import os, base64, requests
from src.utils.basics import terminal

def main(saveonfile):
    GEOSPY_API_KEY = os.getenv("GEOSPY_API_KEY")
    if not GEOSPY_API_KEY: return terminal("e", "You must configure the GeoSpy API Key to continue.")
    for filename in os.listdir("customs/image_analysis"):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            with open(filename, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            response = requests.post(f"https://dev.geospy.ai/predict?image={encoded_string}&top_k=5", headers={"Authorization": f"Bearer {GEOSPY_API_KEY}"})
            print(response.text)