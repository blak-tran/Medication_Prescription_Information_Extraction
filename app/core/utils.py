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
def create_base_model(user_id="", form_json=None):
    medication_records = []
    for record_data in form_json["user_data"]["medication_records"]:
        medication = record_data["medication"]
        medication = medication_basemodel( 
            record_id= str(uuid.uuid4()),
            name=medication["name"],
            dosage_per_day=int(medication["dosage_per_day"]),
            quantity_per_dose=int(medication["quantity_per_dose"]),
            total_quantity=int(medication["total_quantity"]),
            unit=medication["unit"],
            frequency_morning=int(medication["frequency"]["morning"]),
            frequency_afternoon=int(medication["frequency"]["afternoon"]),
            frequency_evening=int(medication["frequency"]["evening"]),
            start_date=datetime.fromisoformat(medication["start_date"]) if medication["start_date"] else "",
            end_date=datetime.fromisoformat(medication["end_date"]) if medication["end_date"] else "",
            )
        medication_records.append(medication)
    import pdb; pdb.set_trace()
    medication_records = medication_records_basemodel(medication_records)

    meta_data = meta_data_basemodel(
        created_at=get_datetime_with_timezone(),
        modified_at=get_datetime_with_timezone(),
        schema_version=form_json["user_data"]["meta_data"].get("schema_version"),
        user_name=form_json["user_data"]["meta_data"].get("user_name"),
        user_id=user_id,
        age=form_json["user_data"]["meta_data"].get("age"),
        gender=form_json["user_data"]["meta_data"].get("gender"),
        doctor_name=form_json["user_data"]["meta_data"].get("doctor_name"),
        hospital_name=form_json["user_data"]["meta_data"].get("hospital_name"),
        address=form_json["user_data"]["meta_data"].get("address"),
        pathological=form_json["user_data"]["meta_data"].get("pathological"),
        note=form_json["user_data"]["meta_data"].get("note"),
    )

    return user_data_basemodel(medication_records=medication_records, meta_data=meta_data)


def save_Image_from_bytes(image: bytes):
    # Process the uploaded image
    image = Image.open(io.BytesIO(image))
    # Save the Image locally
    image.save(temp_img_path)
    img_read = cv2.imread(temp_img_path)
    return img_read

