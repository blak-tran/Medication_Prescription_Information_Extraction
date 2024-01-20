#Medication Prescription Information Extraction
##Introduction
This FastAPI application provides an endpoint (/predict/) for processing and predicting metadata from images, combined with a chatbot.

##Prerequisites

Additionally, ensure that the required modules (app.core.utils and app.modules.Chatbot_core.chatbot_model, and app.modules.OCR.SCANNER_DATA) are available.

##Usage
Clone this repository:

```bash
git clone git@github.com:blak-tran/exe202_project_Medication_Prescription_Information_Extraction.git
cd exe202_project_Medication_Prescription_Information_Extraction
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Docker build:
```bash
docker build . -t pillsy_ai_deployment:2.0 -f Dockerfile
```
Docker Run:
```bash
sudo docker run --runtime nvidia -d --restart=unless-stopped --gpus '"device=0"' Pillsy_AI_Deployment:2.0
```

Run the FastAPI application:
```bash
uvicorn main:app --reload
```

Access the API at http://127.0.0.1:8000/predict/ using a tool like httpie or curl.

