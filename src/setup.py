
import os
import subprocess
import os.path as path


CRON_LOG = path.join(os.getcwd(), "logs", "cron.log")
BACKUP_LOG = path.join(os.getcwd(), "logs", "minecraft-backup-log.txt")
# file paths is a list of full paths including the name of the file
# to generate a info.log file in the logs/ directory for example:
# generate_files([path.join(os.getcwd(), logs, info.log)])
def generate_files(file_paths):
    for file in file_paths:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        file_exists = path.exists(file)
        if file_exists:
            continue
        else:
            open(file, "a").close()

def set_cron_job(cronfile_path):
    if not path.exists(cronfile_path):
        raise FileNotFoundError(f"Cronfile not found at: {cronfile_path}")
    subprocess.run(["crontab", cronfile_path], check=True)
    print(f"Loaded cronfile: {cronfile_path}")
    subprocess.run(["cron", "-f"])
    

def main():
    generate_files(
        [
            CRON_LOG,
            BACKUP_LOG
        ]
    )
    set_cron_job(path.join(os.getcwd(), "cronfile"))

if __name__ == "__main__":
    main()