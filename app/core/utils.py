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

    if "user_data" in form_json and "medication_records" in form_json["user_data"]:
        for record_data in form_json["user_data"]["medication_records"]:
            start_date = None
            end_date = None

            if "start_date" in record_data and record_data["start_date"] is not None:
                start_date = datetime.fromisoformat(record_data["start_date"])

            if "end_date" in record_data and record_data["end_date"] is not None:
                end_date = datetime.fromisoformat(record_data["end_date"])

            medication = medication_basemodel(
                record_id=str(uuid.uuid4()),
                name=record_data.get("name", ""),
                dosage_per_day=record_data.get("dosage_per_day", ""),
                quantity_per_dose=record_data.get("quantity_per_dose", ""),
                total_quantity=record_data.get("total_quantity", ""),
                unit=record_data.get("unit", ""),
                frequency_morning=record_data.get("frequency_morning", ""),
                frequency_afternoon=record_data.get("frequency_afternoon", ""),
                frequency_evening=record_data.get("frequency_evening", ""),
                start_date=start_date,
                end_date=end_date,
            )
            medication_records.append(medication)

    medication_records = medication_records_basemodel(medication_records)

    meta_data = meta_data_basemodel(
        created_at=form_json.get("meta_data", {}).get("created_at", ""),
        modified_at=form_json.get("meta_data", {}).get("modified_at", ""),
        schema_version=form_json.get("meta_data", {}).get("schema_version", ""),
        user_name=form_json.get("meta_data", {}).get("user_name", ""),
        user_id=user_id,
        age=form_json.get("meta_data", {}).get("age", ""),
        gender=form_json.get("meta_data", {}).get("gender", ""),
        doctor_name=form_json.get("meta_data", {}).get("doctor_name", ""),
        hospital_name=form_json.get("meta_data", {}).get("hospital_name", ""),
        address=form_json.get("meta_data", {}).get("address", ""),
        pathological=form_json.get("meta_data", {}).get("pathological", ""),
        note=form_json.get("meta_data", {}).get("note", ""),
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

