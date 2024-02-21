from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date

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
    start_date: str = Field(default=None, description="2023-01-02")
    end_date: str = Field(default=None, description="2023-01-02")



class MetaDataBaseModel(BaseModel):
    created_at: str = Field(default=None, description="2023-01-01")
    modified_at: str = Field(default=None, description="2023-01-02")
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
    medication_records: List[MedicationBaseModel]
    meta_data: MetaDataBaseModel
