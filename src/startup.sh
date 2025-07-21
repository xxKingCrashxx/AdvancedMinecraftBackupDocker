#!/bin/bash
set -e

mkdir -p /app/logs /app/server /app/backups

# Create log files only if missing (because mounts may already have them)
[ -f /app/logs/cron.log ] || touch /app/logs/cron.log
[ -f /app/logs/backup.log ] || touch /app/logs/backup.log

echo "[INFO] Checked and created missing log files."

crontab /app/cronfile
echo "[INFO] Loaded crontab from /app/cronfile"

cron -f