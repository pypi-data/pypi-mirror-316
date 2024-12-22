import os
from typing import Any

import yaml


def load_dataset_config() -> dict[str, Any]:
    """Loads the dataset configuration from a YAML file.

    This function reads the `datasets.yaml` file located in the same directory
    as this script, parses it using the YAML library, and returns the configuration
    as a dictionary.

    Returns:
        dict[str, Any]: A dictionary containing the dataset configuration.
    """
    config_path = os.path.join(os.path.dirname(__file__), "datasets.yaml")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
