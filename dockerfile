FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY src/advanced_mc_server_backup.py .
COPY src/setup.py .
RUN chmod 755 advanced_mc_server_backup.py setup.py
COPY src/cronfile .
COPY requirements.txt .
RUN mkdir server logs backups
RUN pip install -r requirements.txt
RUN crontab cronfile
CMD ["python3", "setup.py"]