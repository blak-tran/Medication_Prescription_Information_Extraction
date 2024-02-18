from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from app.core.base_model import UserDataBaseModel, MedicationRecordsBaseModel, MedicationBaseModel, MetaDataBaseModel
import os, cv2, io
from PIL import Image
import uuid
import base64


def load_environments():
    # Load environment variables from the .env file in the specified root directory
    dotenv_path = os.path.join("./app/environments", ".env")
    load_dotenv(dotenv_path)
    
    
load_environments()
TEMP_ROOT_PATH = os.getenv("temp_path")
temp_img_path = os.path.join(TEMP_ROOT_PATH,"temp_img.png")

def get_datetime_with_timezone():
    # Get the current time in UTC
    current_time_utc = datetime.utcnow()

    # Create a timezone offset of +7 hours for UTC+7 (Hanoi, Vietnam)
    timezone_offset = timedelta(hours=7)

    # Add the timezone offset to the current time
    datetime_with_timezone = current_time_utc.replace(tzinfo=timezone.utc) + timezone_offset

    # Extract the date without the time information
    date_only = datetime_with_timezone.date()

    return datetime_with_timezone


# Function to create an instance of BaseModel from form_json
def create_base_model(medication_records: list = None, 
                      meta_data: MetaDataBaseModel = None, 
                      prescription_Id: str = None):
    
    medication_records = MedicationRecordsBaseModel(medication_records=medication_records.items)
    
    return UserDataBaseModel(medication_records_id=prescription_Id, medication_records=medication_records, meta_data=meta_data)

def save_Image_from_bytes(encoded_image):
    # Decode the base64-encoded image
    decoded_image = base64.b64decode(encoded_image)

    # Process the decoded image
    image = Image.open(io.BytesIO(decoded_image))

    # Save the image locally
    image.save(temp_img_path)

    # Read the saved image using OpenCV
    img_read = cv2.imread(temp_img_path)

    return img_read

