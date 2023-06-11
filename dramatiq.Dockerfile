FROM python:3.11-slim

WORKDIR /code
COPY requirements-worker.txt .
RUN pip install -r requirements-worker.txt
RUN apt-get update && \
    apt-get install ffmpeg libsm6 libxext6  -y
COPY ./src/worker worker/
CMD [ "dramatiq", "worker" ]
