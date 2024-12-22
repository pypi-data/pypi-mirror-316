import os
import zipfile

import requests
from tqdm import tqdm


def download_dataset(
    dataset_name: str, download_url: str, dir_path: str = "~/.VeMatch"
) -> str:
    """Downloads and extracts a dataset from a given URL.

    This function downloads a dataset from the provided URL, extracts it to a specified path,
    and returns the path where the dataset is stored. If the dataset already exists at the
    given location, it simply returns the path without downloading or extracting it again.

    Args:
        dataset_name (str): The name of the dataset to be downloaded.
        download_url (str): The URL from which to download the dataset.
        dir_path (str, optional): The path where the dataset will be stored. Defaults to `~/.VeMatch`.

    Returns:
        str: The path to the directory where the dataset was extracted.

    """
    dir_path = os.path.expanduser(dir_path)
    os.makedirs(dir_path, exist_ok=True)
    dataset_path = os.path.join(dir_path, dataset_name)

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
