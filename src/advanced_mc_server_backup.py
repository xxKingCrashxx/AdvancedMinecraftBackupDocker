#Author: King_Crash
#Date: 14 April 2025

from shutil import make_archive 
import sys
import platform
from datetime import datetime
from os import path, listdir, remove, stat, makedirs, getenv
from mcrcon import MCRcon
import socket
import time
import subprocess

#change variables as needed.
#Config
SRC_DIR = getenv("SRC_DIR", "/server")
LOG_DIR = getenv("LOG_DIR", "/logs")
DEST_DIR = getenv("DEST_DIR", "/backups")
MAX_BACKUPS = int(getenv("MAX_BACKUPS", "10"))
SERVER_HOST = getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(getenv("SERVER_PORT", "25565"))
RCON_PORT = int(getenv("RCON_PORT", "25575"))
RCON_PASSWORD = getenv("RCON_PASSWORD", "")
CONTAINER_NAME = getenv("CONTAINER_NAME", "minecraft_server")

host_platform = platform.system()

#helper function that gets the st_ctime of all the zip files located in the DEST_DIR
#searches for the dir with the smallest "existence" time and stores it in a new list
#function returns the dir with the oldest time using the max_existence
def get_oldest_backup(dirs: list) -> str: 
	dir_existence_time = [None] * len(dirs)
	min_existence = sys.float_info.max

	for i, dir in enumerate(dirs):
		res = stat(path.join(DEST_DIR, dir)).st_ctime
		dir_existence_time[i] = res

		if min_existence > res:
			min_existence = res
	old_dir_index = dir_existence_time.index(min_existence)
	return dirs[old_dir_index]

def log_to_file(log_level, message):
	timestamp = datetime.now().isoformat()
	log_entry = f"[{log_level}] [{timestamp}] {message}"

	print(log_entry)
	try:
		makedirs(LOG_DIR, exist_ok=True)
		log_path = path.join(LOG_DIR, "minecraft-backup-log.txt")

		with open(log_path, mode="a", encoding="utf-8") as fs:
			fs.write(log_entry + "\n")

	except (FileNotFoundError, PermissionError, OSError) as e:
		print(f"[ERROR] Could not write to log file: {e}. Fallback to terminal.")

def stop_server():
	try:
		log_to_file("INFO", "Sending RCON Stop command...")
		with MCRcon(SERVER_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
			mcr.command("say [BACK UP] Server backup script starting, please leave the server...")

			count_start = 10
			while count_start != 0:
				mcr.command(f"say [BACK UP] Server Restarting in: {count_start}")
				count_start = count_start - 1
				time.sleep(1)
			mcr.command("say [BACK UP] Server is closing...")
			mcr.command("save-all")
			mcr.command("stop")

			# wait for server to fully shut down.
			subprocess.run(["docker", "wait", CONTAINER_NAME], check=True)
			log_to_file("INFO", "Server is offline.")

	except Exception as e:
		log_to_file("ERROR", f"Failed to send RCON command {e}")
		exit(1)

def restart_server():
	log_to_file("INFO", "Restarting Server...")
	try:
		subprocess.run(["docker", "start", CONTAINER_NAME], check=True)
	except Exception as e:
		log_to_file("ERROR", f"Failed to start server: {e}")
		exit(1)
	log_to_file("INFO", "Server has restarted successfully.")

def backup_folder():
	timestamp = datetime.now().isoformat()
	safe_timestamp = timestamp.replace(":", "-").replace(".", "-")
	
	backup_file_name = f"backup-{safe_timestamp}.zip"
	backup_file_dir = path.join(DEST_DIR, backup_file_name)

	if not path.exists(SRC_DIR):
		print(f"directory: {SRC_DIR} does not exist")
		exit(-1)

	if not path.exists(DEST_DIR):
		print(f"directory: {DEST_DIR} does not exist")
		exit(-1)

	dirs = listdir(DEST_DIR)
	if MAX_BACKUPS <= len(dirs):
		old_dir = get_oldest_backup(dirs)
		remove(path.join(DEST_DIR, dirs.pop(dirs.index(old_dir))))
		log_to_file("INFO", f"removed old log: {old_dir}")

	if (backup_file_name) in dirs:
			remove((backup_file_dir))

	make_archive(base_name=backup_file_dir, format="zip", root_dir=SRC_DIR)
	log_to_file("INFO", f"{backup_file_name}.zip has been successfully created")

def main():
	stop_server()
	backup_folder()
	restart_server()

if __name__ == '__main__':
	main()
