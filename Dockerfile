FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04
LABEL maintainer "pillsy@gmail.com"

RUN rm -f /etc/apt/sources.list.d/cuda.list
RUN rm -f /etc/apt/sources.list.d/nvidia-ml.list

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get clean

RUN apt-get update && apt-get install -y python3 python3-dev git wget
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

RUN apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y
RUN apt-get update

RUN apt-get install python3-tk -y
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives  --set python /usr/bin/python3

RUN pip install --upgrade pip
RUN pip install cmake

RUN pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/

ENV NVIDIA_DRIVER_CAPABILITIES=all

RUN ls
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port","80"]