FROM python:3.11-slim

WORKDIR /code
COPY requirements-worker.txt .
RUN pip install -r requirements-worker.txt
RUN \
    --mount type=cache,target=/var/cache/apt apt-get update && \
    apt-get install ffmpeg libsm6 libxext6  -y
COPY ./src/worker worker/
CMD [ "dramatiq", "worker" ]
