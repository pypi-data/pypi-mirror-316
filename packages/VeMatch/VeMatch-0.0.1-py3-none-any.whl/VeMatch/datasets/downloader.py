import os
import requests
import zipfile
from tqdm import tqdm

DEFAULT_DATASETS_PATH = os.path.expanduser("~/.VeMatch")

def download_dataset(dataset_name, download_url, default_path=DEFAULT_DATASETS_PATH):
    os.makedirs(default_path, exist_ok=True)
    dataset_path = os.path.join(default_path, dataset_name)

    if os.path.exists(dataset_path):
        return dataset_path

    file_path = f"{dataset_path}.zip"
    print(f"Downloading '{dataset_name}'...")
    response = requests.get(download_url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(file_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

    print(f"Extracting '{dataset_name}'...")

    with zipfile.ZipFile(file_path) as zip_ref:
        zip_ref.extractall(path=dataset_path)
    print(f"Extracted to {dataset_path}.")

    os.remove(file_path)

    return dataset_path
