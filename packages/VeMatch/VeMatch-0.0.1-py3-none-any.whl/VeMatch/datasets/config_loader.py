import yaml
import os

def load_dataset_config():
    config_path = os.path.join(os.path.dirname(__file__), "datasets.yaml")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
