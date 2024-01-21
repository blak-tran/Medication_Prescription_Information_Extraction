from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class medication_basemodel:
    record_id: str 
    name: str
    dosage_per_day: int
    quantity_per_dose: int
    total_quantity: int
    unit: str
    frequency_morning: int
    frequency_afternoon: int
    frequency_evening: int
    start_date: datetime
    end_date: datetime

@dataclass
class medication_records_basemodel:
    medication_records: List[medication_basemodel]
@dataclass
class meta_data_basemodel:
    created_at: Optional[str]
    modified_at: Optional[str]
    schema_version: Optional[str]
    user_name: Optional[str]
    user_id: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    doctor_name: Optional[str]
    hospital_name: Optional[str]
    address: Optional[str]
    pathological: Optional[str]
    note: Optional[str]

@dataclass
class user_data_basemodel:
    medication_records: medication_records_basemodel
    meta_data: meta_data_basemodel
