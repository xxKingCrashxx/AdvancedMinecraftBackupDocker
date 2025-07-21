#!/bin/bash
set -e

# Create log files only if missing (because mounts may already have them)
[ -f /app/logs/cron.log ] || touch /app/logs/cron.log

echo "[INFO] Checked and created missing log files."

crontab /app/cronfile
echo "[INFO] Loaded crontab from /app/cronfile"

cron -f