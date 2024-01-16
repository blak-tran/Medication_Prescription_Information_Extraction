from fastapi import FastAPI, File
from app.core.utils import save_Image_from_bytes
from app.modules.Chatbot_core.chatbot_model import llm_model
from app.modules.OCR.SCANNER_DATA import app_scanner

app = FastAPI()
STATUS = 200 

@app.post("/predict/")
async def upload_image(message: str = None, image: bytes = File(...)):
    error = None

    try:
        temp_img_path = save_Image_from_bytes(image)
        data = app_scanner.tracking_data(temp_img_path)
        data_ehance = llm_model.standardize_data(data)
        metadata = llm_model.Json_tracking(data_ehance)
    except Exception as e:
        error = "Traceback: " + str(e)
        STATUS = 404
        print(f"An error occurred: {e}")

    response = {"status": STATUS, "metadata": metadata, "error": error}
    return response
