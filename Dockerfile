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

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["python", "main.py"]
