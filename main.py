from fastapi import FastAPI, File
from app.core.utils import save_Image_from_bytes
from app.modules.Chatbot_core.chatbot_model import llm_model
from app.modules.OCR.SCANNER_DATA import app_scanner
import jwt, base64

app = FastAPI()


@app.post("/api/v1/predict-ocr/")
async def predict_ocr(user_Id: str = None, 
                      prescription_Id: str = None, 
                      image: bytes= None ):
    error = ""
    STATUS = 200 
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

    response = {"status": STATUS, 
                "user_Id": user_Id, 
                "prescription_Id": prescription_Id,
                "data": data, 
                "imageBase64": img_bytes, 
                "error": error}
    
    return response


@app.post("/api/v1/predict-info/")
async def predict_info(user_Id: str = None, 
                      prescription_Id: str = None,
                      data: str = None):
    error = ""
    STATUS = 200

    try:
        data_ehance = llm_model.standardize_data(data)
        data = llm_model.Json_tracking(user_Id, prescription_Id, data_ehance)
    except Exception as e:
        error = "Traceback: " + str(e)
        STATUS = 404
        print(f"An error occurred: {e}")

    response = {"status": STATUS, "user_data": data, "error": error}
    return response
