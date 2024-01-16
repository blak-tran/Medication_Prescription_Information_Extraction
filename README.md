#Medication Prescription Information Extraction
##Introduction
This FastAPI application provides an endpoint (/predict/) for processing and predicting metadata from images, combined with a chatbot.

##Prerequisites
Make sure you have Python installed on your system. You can install the required dependencies using:

```bash
pip install fastapi
```

Additionally, ensure that the required modules (app.core.utils and app.modules.Chatbot_core.chatbot_model, and app.modules.OCR.SCANNER_DATA) are available.

##Usage
Clone this repository:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the FastAPI application:
```bash
uvicorn main:app --reload
```

Access the API at http://127.0.0.1:8000/predict/ using a tool like httpie or curl.

Endpoint Details
/predict/
Method: POST
Parameters:
message (optional): A string message.
image (required): An image file in bytes format.
Response:
status: HTTP status code (200 if successful, 404 if an error occurred).
metadata: Extracted metadata from the image.
error: Error details (if any).
Error Handling
If an error occurs during the processing of the image, the status code will be set to 404, and the error details will be available in the error field of the response.

Disclaimer
This is a simple example README. Ensure to customize it based on your project's specific requirements and structure.

