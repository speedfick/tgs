FROM python:3.12-slim

COPY app /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "sensor.py"] 