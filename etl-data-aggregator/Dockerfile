FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv && \
venv/bin/pip install --no-cache-dir --upgrade pip && \
venv/bin/pip install --no-cache-dir -r requirements.txt


COPY main.py .

ENV PYTHONPATH="/app/src:$PYTHONPATH"

# docker run --rm sentiment-stream-etl-data-aggregator bash -c "source venv/bin/activate && python main.py" Code to run this container when needed. Otherwise it doesnt keep running since its a batch etl job
# CMD ["venv/bin/python", "main.py"]
