from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from app.core.base_model import user_data_basemodel, medication_records_basemodel, medication_basemodel, meta_data_basemodel
import os, cv2, io
from PIL import Image
import uuid


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
def create_base_model(user_id="", prescription_Id="", form_json=None):
    medication_records = []
    for record_data in form_json["user_data"]["medication_records"]:
        medication = medication_basemodel(
            record_id=str(uuid.uuid4()),
            name=record_data["name"],
            dosage_per_day=record_data["dosage_per_day"],
            quantity_per_dose=record_data["quantity_per_dose"],
            total_quantity=record_data["total_quantity"],
            unit=record_data["unit"],
            frequency_morning=record_data["frequency_morning"],
            frequency_afternoon=record_data["frequency_afternoon"],
            frequency_evening=record_data["frequency_evening"],
            start_date=datetime.fromisoformat(record_data["start_date"]),
            end_date=datetime.fromisoformat(record_data["end_date"]),
        )
        medication_records.append(medication)
    medication_records = medication_records_basemodel(medication_records)

    meta_data = meta_data_basemodel(
        created_at=form_json["meta_data"]["created_at"],
        modified_at=form_json["meta_data"]["modified_at"],
        schema_version=form_json["meta_data"]["schema_version"],
        user_name=form_json["meta_data"]["user_name"],
        user_id=user_id,
        age=form_json["meta_data"]["age"],
        gender=form_json["meta_data"]["gender"],
        doctor_name=form_json["meta_data"]["doctor_name"],
        hospital_name=form_json["meta_data"]["hospital_name"],
        address=form_json["meta_data"]["address"],
        pathological=form_json["meta_data"]["pathological"],
        note=form_json["meta_data"]["note"],
    )

    return user_data_basemodel(medication_records_id=prescription_Id, medication_records=medication_records, meta_data=meta_data)

import base64
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

