# Medication Prescription Information Extraction
## Introduction

This FastAPI application provides an endpoint (/predict/) for processing and predicting metadata from images, combined with a chatbot.

## Prerequisites

Additionally, ensure that the required modules (app.core.utils and app.modules.Chatbot_core.chatbot_model, and app.modules.OCR.SCANNER_DATA) are available.

## Usage
Clone this repository:

```bash
git clone git@github.com:blak-tran/exe202_project_Medication_Prescription_Information_Extraction.git
cd exe202_project_Medication_Prescription_Information_Extraction
```

## Pretrained model
https://drive.google.com/drive/folders/1CPn2kOxE1rXo7ZB13E23RdmhbI1zplpy?usp=sharing

Install dependencies:
```bash
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
```

```bash
pip install -r requirements.txt
```

## Install mmocr
```bash
pip install -U openmim
mim install mmengine
mim install mmcv
mim install mmdet

git clone https://github.com/open-mmlab/mmocr.git && cd mmocr
pip install -v -e .

cd ../

```

Docker build:
```bash
docker build . -t pillsy_ai_deployment:2.0 -f Dockerfile
```
Docker Run:
```bash
sudo docker run -p 8003:8000 --runtime nvidia -d --restart=unless-stopped pillsy_ai_deployment:2.0
```

Run the FastAPI application:
```bash
uvicorn main:app --reload
```

Access the API at http://127.0.0.1:8000/predict/ using a tool like httpie or curl.

