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

## File Structure

- `main.py`: Main script file
- `README.md`: This file
- `data/Takeout/Google Photos`: Input directory
- `data/out`: Output directory

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
