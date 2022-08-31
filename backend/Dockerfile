# --- Stage 1 ---
FROM python:3.10

COPY . /application
WORKDIR /application

RUN ls -la .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
