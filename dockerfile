FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY src/startup.sh .
COPY src/advanced_mc_server_backup.py .
RUN chmod 755 advanced_mc_server_backup.py startup.sh
COPY src/cronfile .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["bash", "startup.sh"]