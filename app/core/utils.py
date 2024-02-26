from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from app.core.base_model import UserDataBaseModel, MetaDataBaseModel, MedicationBaseModel
import os, cv2, io
from PIL import Image
from uuid import uuid4
import base64


def load_environments():
    # Load environment variables from the .env file in the specified root directory
    dotenv_path = os.path.join("./app/environments", ".env")
    load_dotenv(dotenv_path)
    
    
load_environments()
TEMP_ROOT_PATH = os.getenv("temp_path")
temp_img_path = os.path.join(TEMP_ROOT_PATH,"temp_img.png")
# Define the list of date formats you expect
DATES_FORMATS = ["%d-%m-%Y", "%d%m/%Y"]

def get_datetime_with_timezone():
    # Get the current time in UTC
    current_time_utc = datetime.utcnow()

    # Create a timezone offset of +7 hours for UTC+7 (Hanoi, Vietnam)
    timezone_offset = timedelta(hours=7)

    # Add the timezone offset to the current time
    datetime_with_timezone = current_time_utc.replace(tzinfo=timezone.utc) + timezone_offset

    return datetime_with_timezone

def parse_date_with_flexible_formats(date_str, formats):
    """
    Attempts to parse a date string using a list of possible formats.

    :param date_str: The date string to parse.
    :param formats: A list of string formats to try.
    :return: A datetime object if parsing succeeds, or None if all formats fail.
    """
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def calculate_drink_duration(data: list[MedicationBaseModel]):
    calculation_base_date = get_datetime_with_timezone()

    for record in data:
        start_date = calculation_base_date

        if record.dosage_per_day > 0:
            num_days = record.total_quantity / record.dosage_per_day
            end_date = start_date + timedelta(days=round(num_days))

            # Assuming direct assignment is valid and expected to update the model
            record.start_date = start_date.strftime("%d-%m-%Y")
            record.end_date = end_date.strftime("%d-%m-%Y")
        
    return data

# Function to create an instance of BaseModel from form_json
def create_base_model(medication_records: list = None, 
                      meta_data: MetaDataBaseModel = None, 
                      prescription_Id: str = None):
    
    medication_records_full_info = calculate_drink_duration(medication_records.items)
    
    for idx, _ in enumerate(medication_records_full_info):
        medication_records_full_info[idx].record_id = str(uuid4())
        medication_records_full_info[idx].start_date = parse_date_with_flexible_formats(str(medication_records_full_info[idx].start_date), DATES_FORMATS)
        medication_records_full_info[idx].end_date = parse_date_with_flexible_formats(str(medication_records_full_info[idx].end_date), DATES_FORMATS)
    
    
    if meta_data.created_at is None:
        meta_data.created_at = get_datetime_with_timezone()
    meta_data.created_at = parse_date_with_flexible_formats(meta_data.created_at, DATES_FORMATS)
            
    
    if meta_data.modified_at is None:
        meta_data.modified_at = get_datetime_with_timezone()
    meta_data.modified_at = parse_date_with_flexible_formats(meta_data.modified_at, DATES_FORMATS)
    
    return UserDataBaseModel(medication_records_id=prescription_Id, medication_records=medication_records_full_info, meta_data=meta_data)

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

