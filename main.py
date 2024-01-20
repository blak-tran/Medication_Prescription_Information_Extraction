from fastapi import FastAPI, File
from app.core.utils import save_Image_from_bytes
from app.modules.Chatbot_core.chatbot_model import llm_model
from app.modules.OCR.SCANNER_DATA import app_scanner
import base64

app = FastAPI()

@app.post("/api/v1/predict-ocr/")
async def predict_ocr(message: str = None, image: bytes = File(...)):
    error = ""
    STATUS = 200 
    print("Process message: ", message)
    try:
        img = save_Image_from_bytes(image)
        result_path, data = app_scanner.tracking_data(img)
        
        # Read the image as bytes
        with open(result_path, "rb") as img_file:
            img_bytes = base64.b64encode(img_file.read()).decode()
            
    except Exception as e:
        error = "Traceback: " + str(e)
        STATUS = 404
        print(f"An error occurred: {e}")

    response = {"status": STATUS, "data": data, "result_image": img_bytes, "error": error}
    return response


@app.post("/api/v1/predict-info/")
async def predict_info(message: str = None, data: str = None):
    error = ""
    STATUS = 200
    print("Process message: ", message)
    try:
        data_ehance = llm_model.standardize_data(data)
        metadata = llm_model.Json_tracking(data_ehance)
    except Exception as e:
        error = "Traceback: " + str(e)
        STATUS = 404
        print(f"An error occurred: {e}")

    response = {"status": STATUS, "metadata": metadata, "error": error}
    return response
