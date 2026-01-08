# usb-webcam-api

A FastAPI application to stream video from a USB webcam.

## Setup

1.  **Create the virtual environment:**
    ```bash
    uv venv
    ```

2.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## Running the application

```bash
uvicorn main:app --reload
```
