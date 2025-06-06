# Simple Image Text Label

Tool for filtering and labeling images in a handwritten text dataset.

![screen](./docs/screen.jpg)

## Features

- Web-based UI accessible via browser
- Displays images and allows label editing, with file handling logic defined in sitl_handler.py
- Organizes the dataset into four categories: QUEUE, PASS, DROP, and FIX

## Usage

```sh
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python -m sitl --handler sitl_handler.py
```
