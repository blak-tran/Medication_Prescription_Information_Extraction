from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MedicationBaseModel(BaseModel):
    record_id: str = None
    name: str = None
    dosage_per_day: int = None
    quantity_per_dose: int = None
    total_quantity: int = None
    unit: str = None
    frequency_morning: int = None
    frequency_afternoon: int = None
    frequency_evening: int = None
    start_date: datetime = None
    end_date: datetime = None


class MedicationRecordsBaseModel(BaseModel):
    medication_records: List[MedicationBaseModel]

class MetaDataBaseModel(BaseModel):
    created_at: str = None
    modified_at: str = None
    schema_version: str = None
    user_name: str = None
    user_id: str = None
    age: str = None
    gender: str = None
    doctor_name: str = None
    hospital_name: str = None
    address: str = None
    pathological: str = None
    note: str = None
class UserDataBaseModel(BaseModel):
    medication_records_id: str
    medication_records: MedicationRecordsBaseModel
    meta_data: MetaDataBaseModel
