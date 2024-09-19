# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && \
    apt-get install -y \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libglib2.0-dev \
        libsm6 \
        libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# 暴露端口
EXPOSE 5001

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5003"]
