from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class medication_basemodel:
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
    medication_records_id: str
    medication_records: medication_records_basemodel
    meta_data: meta_data_basemodel
