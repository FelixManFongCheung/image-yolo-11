from ultralytics import YOLO
from config import Config

class ModelSingleton:
    _instance = None
    _model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._model = YOLO(Config.MODEL_PATH)
        return cls._instance

    def get_model(self):
        return self._model