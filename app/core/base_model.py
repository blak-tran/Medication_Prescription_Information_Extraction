from dataclasses import dataclass
from typing import List

@dataclass
class MedicationRecord:
    record_id: str
    name: str
    dosage_per_day: int
    quantity_per_dose: int
    total_quantity: int
    unit: str
    frequency_morning: int
    frequency_afternoon: int
    frequency_evening: int
    start_date: str
    end_date: str

@dataclass
class UserData:
    medication_records: List[MedicationRecord]

@dataclass
class Metadata:
    created_at: str
    modified_at: str
    schema_version: str
    user_name: str

@dataclass
class BaseModel:
    user_data: UserData
    metadata: Metadata