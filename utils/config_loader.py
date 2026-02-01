import json
import os

class ConfigLoader:
    @staticmethod
    def get_config():
        config_path = os.path.join(os.getcwd(), 'config', 'settings.json')
        with open(config_path, 'r') as f:
            return json.load(f)