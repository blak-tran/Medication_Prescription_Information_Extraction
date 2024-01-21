from fastapi import FastAPI, File
from app.core.utils import save_Image_from_bytes
from app.modules.Chatbot_core.chatbot_model import llm_model
from app.modules.OCR.SCANNER_DATA import app_scanner
import jwt, base64

app = FastAPI()
jwt_object = jwt()


@app.post("/api/v1/predict-ocr/")
async def predict_ocr(token = None, image: bytes = File(...)):
    error = ""
    STATUS = 200 
    user_info = jwt.decode(token, options={"verify_signature": False})
    print("Process user_info: ", user_info)
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

    response = {"status": STATUS, "token": token, "data": data, "result_image": img_bytes, "error": error}
    return response


@app.post("/api/v1/predict-info/")
async def predict_info(token = None, data: str = None):
    error = ""
    STATUS = 200
    user_info = jwt.decode(token, options={"verify_signature": False})
    user_id = user_info['AccountId']
    print("Process user_info: ", user_info)
    try:
        data_ehance = llm_model.standardize_data(data)
        data = llm_model.Json_tracking(user_id, data_ehance)
    except Exception as e:
        error = "Traceback: " + str(e)
        STATUS = 404
        print(f"An error occurred: {e}")

    response = {"status": STATUS, "token": token, "user_data": data, "error": error}
    return response
