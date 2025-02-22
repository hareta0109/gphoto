# Metadata Setting Script

This project is a Python script that sets metadata for image files and updates the file creation and modification dates.

## Features

- Set metadata such as title, description, capture date, and GPS information for image files
- Update the file creation and modification dates to reflect the metadata capture date

## Requirements

- Python 3.12
- `Poetry` for dependency management
- `exiftool` command-line tool

## Installation

1. Install Poetry if you haven't already:

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. Install the required dependencies using Poetry:

    ```sh
    poetry install
    ```

3. Install `exiftool`. On macOS, you can use Homebrew:

    ```sh
    brew install exiftool
    ```

## Usage

1. Navigate to the directory where the script is located:

    ```sh
    cd /path/to/your/project
    ```

2. Start a Poetry shell:

    ```sh
    poetry shell
    ```

3. Run the script:

    ```sh
    python gphoto/main.py
    ```

4. The script will process image files and metadata files in the `data/Takeout/Google Photos` directory and output them to the `data/out` directory.

## Google Photos Export

This script is primarily designed to work with data exported from Google Photos. When you export your data from Google Photos, you will receive both media files (such as JPEG images) and metadata files (in JSON format). The metadata files contain additional information about the media files, such as titles, descriptions, capture dates, and GPS information.

### Media and Metadata Files

- **Media Files**: These are the actual image or video files (e.g., `.jpg`, `.mp4`) exported from Google Photos.
- **Metadata Files**: These are JSON files that contain metadata for the corresponding media files. Each media file will have a corresponding metadata file with the same name but a `.json` extension.

For example:

- `IMG_20210101_123456.jpg` (media file)
- `IMG_20210101_123456.json` (metadata file)

The script reads the metadata from the JSON files and applies it to the corresponding media files.

## File Structure

- `main.py`: Main script file
- `README.md`: This file
- `data/Takeout/Google Photos`: Input directory
- `data/out`: Output directory

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
