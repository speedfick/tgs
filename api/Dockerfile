FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app /app

EXPOSE 5000
RUN pip install -r requirements.txt

CMD ["python", "api.py"] 