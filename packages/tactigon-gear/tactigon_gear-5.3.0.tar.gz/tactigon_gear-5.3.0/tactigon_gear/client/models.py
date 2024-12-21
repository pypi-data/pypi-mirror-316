from os import path
from dataclasses import dataclass, field
from typing import List

@dataclass
class UserData:
    user_id: str
    auth_key: str

    @classmethod
    def FromJSON(cls, json):
        return cls(**json)


@dataclass
class ClientConfig:
    MODEL_NAME: str

    SERVER_URL: str = "https://tgear.eu.pythonanywhere.com"
    MODEL_GESTURES: List[str] = field(default_factory=list)
    MODEL_SPLIT_RATIO: float = 0.3
    MODEL_DATA_PATH: str = "data/models/"
    MODEL_SESSIONS: List[str] = field(default_factory=list)

    TRAINING_SESSIONS: List[str] = field(default_factory=list)

    @property
    def model_data_full_path(self):
        return path.join(self.MODEL_DATA_PATH, self.MODEL_NAME)
    
    @classmethod
    def FromJSON(cls, json):
        return cls(**json)


@dataclass
class DataCollectionConfig:
    SESSION_INFO: str
    HAND: str
    RAW_DATA_PATH: str = "data/raw"
    GESTURE_NAME: List[str] = field(default_factory=list)

    @property
    def raw_data_full_path(self) -> str:
        return path.join(self.RAW_DATA_PATH)

    @classmethod
    def FromJSON(cls, json):
        return cls(**json)
    

@dataclass
class HAL:
    SERIAL_COM_PORT: str
    NUM_SAMPLE: int
    
    BLE_RIGHT_ADDRESS: str
    BLE_RIGHT_NAME: str
    BLE_RIGHT_ENABLE: bool
    
    BLE_LEFT_ADDRESS: str
    BLE_LEFT_NAME: str
    BLE_LEFT_ENABLE: bool

    INTERFACE: str = "Bluetooth"

    @classmethod
    def FromJSON(cls, json: dict):
        return cls(**json)