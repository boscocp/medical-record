FROM python:3.13-slim

ENV PYTHONPATH=/
WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get clean

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config && \
    apt-get clean



COPY src/ ./src

COPY requirements.txt .

RUN pip install -r requirements.txt

USER nobody

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]