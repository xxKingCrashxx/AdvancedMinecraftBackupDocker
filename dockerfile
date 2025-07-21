FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY src/advanced_mc_server_backup.py .
RUN chmod 766 advanced_mc_server_backup.py
COPY src/cronfile .
COPY requirements.txt .
RUN mkdir server logs backups
RUN pip install -r requirements.txt
RUN crontab cronfile
CMD ["sh", "-c", "cron && tail -f /app/logs/cron.log"]