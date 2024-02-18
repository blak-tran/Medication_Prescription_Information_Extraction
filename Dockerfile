FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04
LABEL maintainer "pillsy@gmail.com"

RUN rm -f /etc/apt/sources.list.d/cuda.list
RUN rm -f /etc/apt/sources.list.d/nvidia-ml.list

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app/

# Add the Deadsnakes PPA for newer Python versions
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa

# Now you can install Python 3.11
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    libgl1-mesa-glx \
    gcc \
    git \
    curl \
    build-essential \
    cmake \
    pkg-config \
    libgl1-mesa-glx

# Install pip for Python 3.11
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.11 get-pip.py

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
RUN update-alternatives  --set python /usr/bin/python3.11

RUN pip install --upgrade pip
RUN pip install cmake

RUN pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/

ENV NVIDIA_DRIVER_CAPABILITIES=all

RUN chmod +x ./run_service.sh
CMD ["./run_service.sh"]
