from dotenv import load_dotenv
from datetime import datetime, timedelta
from app.core.base_model import MedicationRecord, UserData, Metadata, BaseModel
import os, cv2, io
from PIL import Image


def load_environments():
    # Load environment variables from the .env file in the specified root directory
    dotenv_path = os.path.join("./app/environments", ".env")
    load_dotenv(dotenv_path)
    
    
load_environments()
TEMP_ROOT_PATH = os.getenv("temp_path")
temp_img_path = os.path.join(TEMP_ROOT_PATH,"temp_img.png")

def convert_to_datetime_with_timezone(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt + timedelta(hours=7)  # Add 7 hours for UTC+7 (Hanoi, Vietnam)


# Function to create an instance of BaseModel from form_json
def create_base_model(form_json):
    medication_records = []
    for record_data in form_json["user_data"]["medication_records"]:
        medication = record_data["medication"]
        medication_records.append(
            MedicationRecord(
                record_id=record_data["record_id"],
                name=medication["name"],
                dosage_per_day=int(medication["dosage_per_day"]),
                quantity_per_dose=int(medication["quantity_per_dose"]),
                total_quantity=int(medication["total_quantity"]),
                unit=medication["unit"],
                frequency_morning=int(medication["frequency"]["morning"]),
                frequency_afternoon=int(medication["frequency"]["afternoon"]),
                frequency_evening=int(medication["frequency"]["evening"]),
                start_date=datetime.fromisoformat(medication["start_date"]),
                end_date=datetime.fromisoformat(medication["end_date"]),
            )
        )

    user_data = UserData(medication_records=medication_records)

    metadata = Metadata(
        created_at=form_json["metadata"].get("created_at"),
        modified_at=form_json["metadata"].get("modified_at"),
        schema_version=form_json["metadata"].get("schema_version"),
        user_name=form_json["metadata"].get("user_name"),
        age=form_json["metadata"].get("age"),
        gender=form_json["metadata"].get("gender"),
        doctor_name=form_json["metadata"].get("doctor_name"),
        hospital_name=form_json["metadata"].get("hospital_name"),
        address=form_json["metadata"].get("address"),
        pathological=form_json["metadata"].get("pathological"),
        note=form_json["metadata"].get("note"),
    )

    return BaseModel(user_data=user_data, metadata=metadata)


def save_Image_from_bytes(image: bytes):
    # Process the uploaded image
    image = Image.open(io.BytesIO(image))
    # Save the Image locally
    image.save(temp_img_path)
    img_read = cv2.imread(temp_img_path)
    return img_read

