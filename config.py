import json

class Config:
    def __init__(self):
        file_path = "configs/config.json"
        self.config = json.load(open(file_path, encoding='utf-8'))
    def get(self, param):
        return self.config.get(param)