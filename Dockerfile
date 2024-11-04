FROM python:3.9-alpine3.13
LABEL maintainer="arraieot"

WORKDIR .

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install fastapi uvicorn && \
    pip install --no-cache-dir --upgrade -r /tmp/requirements.txt


COPY ./app /app


CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
