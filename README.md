# Setup Instructions:

## Script Dependencies
Before Running this script, install Dependencies:
- Run `pip install -r requirements.txt`

## Config setup
### Proper config setup inside the script must be done.
- SRC_DIR = r""
    - The absolute path to your minecraft server
- DEST_DIR = r""
    - The absolute path for where you wish to save the backups
- LOG_DIR = r""
    - The absolute path for where you wish the logfile to be saved at.
- MAX_BACKUPS = 10 
    - the number of backups to store. The script will remove the oldest backup if backups exceed or match the MAX_BACKUPS
- SERVER_HOST = ""
    - IP of your minecraft server.
- SERVER_PORT = number
    - Port of your minecraft server.
- RCON_PORT = number
    - Port to access RCON on the server.
- RCON_PASSWORD = ""
    - The password to authenticate on the server
- START_COMMAND = r""
    - Either a bat file located in the root directory of your mc server or a string to start the minecraft server with defined java arguments.
- TIMEOUT = 60
    - time in seconds until the script will fail if the server does not shut down within that time limit.
 
## Minecraft Server Configuration:
### In the server.properties file:
- You Must enable RCON.
- You Must Set your RCON password.

## Setup on linux systems:
- You may have to setup a venv in python before you can install the dependencies.
- I use screens for linux environments, so you should also install screens if you do not have it.
