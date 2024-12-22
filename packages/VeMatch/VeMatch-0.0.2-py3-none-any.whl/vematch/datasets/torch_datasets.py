import os
import re
from typing import Any

import torch
from torchvision.io import read_image

from vematch.datasets import config_loader, downloader

__all__ = ["load_data", "ImageDataset"]


class ImageDataset(torch.utils.data.Dataset):
    """A dataset class for handling image data with labels.

    This class is used to represent datasets with images and their corresponding
    labels. It supports optional image transformations.

    Args:
        images (list[str]): A list of file paths to the images.
        labels (list[int]): A list of labels corresponding to the images.
        transform (callable, optional): A function or transform to apply to the images.

    Attributes:
        images (list[str]): The image file paths.
        labels (list[int]): The corresponding labels.
        transform (callable, optional): The transform applied to images.
    """

    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = read_image(self.images[idx])
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label


def load_data(dataset_name: str, dir_path: str = "~/.VeMatch",custom_config: dict[str, Any] = None,):
    """Loads and prepares the dataset for training, gallery, and query usage.

    This function retrieves dataset configurations, checks if the dataset is already present locally,
    downloads and extracts it if necessary, or allows users to directly provide a path to pre-structured
    local data. Creates dataset objects for training, gallery, and query partitions.

    Args:
        dataset_name (str): The name of the dataset to load. If `custom_config` is provided, 
                            this serves as an identifier for the custom dataset path.
        dir_path (str, optional): The base directory where datasets are stored. Defaults to `~/.VeMatch`.
        custom_config (dict[str, Any], optional): Custom dataset configuration. This parameter can include:

            - `url` (str, optional): The URL to download the dataset if it's not available locally.
            - `query` (str, optional): The name of the folder or file that contains the query images.
            - `gallery` (str, optional): The name of the folder or file that contains the gallery images.
            - `train` (str, optional): The name of the folder or file that contains the training images.
            - `label-extraction` (dict, optional): Defines how to extract labels from image file names.

            Refer to the :doc:`In-Built Datasets <inbuilt/index>` and :doc:`Label-Extraction <inbuilt/label_extraction>` for more information.

    Returns:
        tuple[ImageDataset, ImageDataset, ImageDataset]: The datasets for training, gallery, and query partitions.

    Raises:
        ValueError: If `dataset_name` is invalid (when `custom_config` is not provided).
        FileNotFoundError: If `dataset_name` is not found locally and no download URL is available for custom datasets.

    References:
        For details on dataset configurations and custom dataset support, see the :doc:`In-built Datasets <inbuilt/index>`.

        For details about label extraction see :doc:`Label-Extraction <inbuilt/label_extraction>`.
    """
    config = custom_config or config_loader.load_dataset_config()

    if dataset_name not in config.keys() and not custom_config:
        raise ValueError(
            f"Invalid dataset name. See the \"In-built Datasets\" for valid options."
        )

    dataset_config = config[dataset_name]
    dir_path = os.path.expanduser(dir_path)

    dataset_path = os.path.join(dir_path, dataset_name)

    if not os.path.exists(dataset_path):
        if custom_config and "url" not in dataset_config:
            raise FileNotFoundError(
                f"Dataset '{dataset_name}' not found locally and no URL is available for downloading. "
                f"Please provide a valid local path or a download URL in the custom configuration."
            )
        print(f"Dataset '{dataset_name}' not found locally. Downloading...")
        dataset_path = downloader.download_dataset(dataset_name, dataset_config["url"], dir_path)
    else:
        print(f"Using local dataset at '{dataset_path}'.")

    default_transform = ()

    train, gallery, query = __get_images(dataset_path, dataset_config)
    train = ImageDataset(*train, default_transform)
    gallery = ImageDataset(*gallery, default_transform)
    query = ImageDataset(*query, default_transform)

    return train, gallery, query


def __get_label(image: str, config: dict[str, Any]) -> int:
    """Extracts the label for an image based on the dataset configuration.

    This function uses the provided label extraction method (e.g., regex) from the configuration
    to determine the label for the given image.

    Args:
        image (str): The file name or path of the image.
        config (dict[str, Any]): The configuration dictionary containing label extraction details.

    Returns:
        int: The label extracted from the image file name or path.
    """
    extraction = config["label-extraction"]

    if extraction["method"] == "regex":
        pattern = extraction["pattern"]
        match = re.match(pattern, image)
        return int(match.group(1))
    else:
        raise ValueError("Invalid label extraction method.")


def __get_images(path: str, config: dict[str, Any]) -> tuple[list[str], list[int]]:
    """Retrieves image paths and labels from the specified dataset directories.

    This private function iterates over the `train`, `gallery`, and `query` categories,
    and collects the image paths and their corresponding labels using the provided configuration.

    Args:
        path (str): The base path where the dataset is stored.
        config (dict[str, Any]): The configuration dictionary for the dataset.

    Returns:
        tuple[list[str], list[int]]: Lists of image paths and corresponding labels for each category.
    """
    data = []

    for category in ["train", "gallery", "query"]:
        images, labels = [], []
        folder_path = os.path.join(path, config[category])

        for image in os.listdir(folder_path):
            images.append(os.path.join(folder_path, image))
            labels.append(__get_label(image, config))

        data.append((images, labels))

    return data
