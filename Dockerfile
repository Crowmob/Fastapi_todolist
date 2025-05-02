FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN touch /var/log/cron.log

CMD cron && uvicorn main:app --host 0.0.0.0 --port 80