from fastapi import FastAPI, File
from app.core.utils import save_Image_from_bytes
from app.modules.Chatbot_core.chatbot_model import llm_model
from app.modules.OCR.SCANNER_DATA import app_scanner
import base64

app = FastAPI()


@app.post("/api/v1/predict-ocr/")
async def predict_ocr(message: dict):
    user_Id = message.get("user_Id")
    prescription_Id = message.get("prescription_Id")
    image = message.get("imageBase64")
    
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
                "data": str(data), 
                "imageBase64": img_bytes, 
                "error": error}
    print(response)
    
    return response


@app.post("/api/v1/predict-info/")
async def predict_info(message: dict):
    user_Id = message.get("user_Id")
    prescription_Id = message.get("prescription_Id")
    data = message.get("data")
    error = ""
    STATUS = 200
    try:
        data_ehance = await llm_model.data_generator(str(data))
        json_data = await llm_model.Json_tracking(user_Id, prescription_Id, data_ehance)
    except Exception as e:
        error = "Traceback: " + str(e)
        STATUS = 404
        print(f"An error occurred: {e}")

    response = {"status": STATUS, "user_data": json_data, "error": error}
    print(response)
    return response
