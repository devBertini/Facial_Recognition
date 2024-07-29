FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    build-essential \
    libmariadb-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    cmake \
    gfortran \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip-tools pip wheel

RUN pip install setuptools==71.0.4

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-build-isolation -r requirements.txt

COPY app/ .

CMD ["python", "main.py"]
