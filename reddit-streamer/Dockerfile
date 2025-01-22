FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv && \
    venv/bin/pip install --no-cache-dir --upgrade pip && \
    venv/bin/pip install --no-cache-dir -r requirements.txt

COPY stream_reddit.py .

ENV PYTHONPATH="/app/src:$PYTHONPATH"

CMD ["venv/bin/python", "stream_reddit.py"]
