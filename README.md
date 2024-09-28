# DeepNude-Detector

## Description

This project is a tool for detecting nudity in images, allowing users to analyze both local images and images from URLs. It utilizes the **NudeNet** library to classify and detect explicit content. Additionally, it offers an option to automatically censor images identified as inappropriate.

## Features

- Detects inappropriate content in images.
- Allows users to choose between analyzing local images or downloading images from a URL.
- Automatically blurs images detected as inappropriate.
- Generates random names for downloaded and censored images to prevent file overwriting.

## How It Works

1. The user can choose to analyze either a local image or download an image from a URL.
2. The system detects if the image contains explicit content based on a configurable minimum score.
3. If requested, the image is censored and saved locally with a randomly generated name in the format `censored_<random_name>.jpg`.

## Requirements

- Python 3.x
- Libraries:
  - NudeNet
  - OpenCV
  - Pillow (PIL)
  - Requests

## Contribution

Feel free to open issues and submit pull requests for improvements or bug fixes. This project is under active development, and feedback is always appreciated.
