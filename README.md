# Google Drive Uploader Telegram Bot
**A Telegram bot to upload files from Telegram or Direct links to Google Drive.**
- Find it on Telegram as [Google Drive Uploader](https://t.me/uploadgdrivebot)

## Features
- [X] Telegram files support.
- [X] Direct Links support.
- [X] Custom Upload Folder.
- [X] TeamDrive Support.
- [X] Clone/Copy Google Drive Files.
- [X] Delete Google Drive Files.
- [X] Empty Google Drive trash.
- [X] youtube-dl support.
- [X] 中文界面提示与指引。

## ToDo 
- [ ] Handle more exceptions.
- [ ] LOGGER support.
- [ ] Service account support.
- [ ] Update command.

## Deploying

### Deploy on [Heroku](https://heroku.com)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Deploy on Replit
Replit lets you host the bot in a browser-based workspace. The steps below assume you already
have a Replit account.

1. **Create or import the project.**
   - Visit [replit.com](https://replit.com) and click **Create Repl**.
   - Choose the **Python** template, or select **Import from GitHub** and paste this repository
     URL to clone it directly. If you start from a blank Python Repl, delete the default files
     and run `git clone https://github.com/viperadnan-git/google-drive-telegram-bot` in the
     Shell panel.
2. **Install dependencies.** Open the **Shell** tab and run:
   ```sh
   pip install -r requirements.txt
   ```
   Replit will automatically cache the installed packages. If the install is interrupted, rerun
   the command until it completes without errors.
3. **Configure environment secrets.**
   - Click the **Tools → Secrets** sidebar (the padlock icon).
   - Add each required configuration value (see the [Configuration Values](#configuration-values)
     section) as a secret. The secret name becomes the environment variable inside the Repl.
   - For values that include quotes or special characters, paste them exactly as provided—Replit
     stores the raw string for you.
4. **Launch the bot.** In the Shell panel, start the bot with:
   ```sh
   python3 -m bot
   ```
   The console will display the bot logs. Leave this tab open while testing commands from
   Telegram to confirm everything is working.
5. **Keep the bot running.** Replit stops inactive Repls after some time unless you enable a
   persistent option:
   - Upgrade to **Replit Hacker** and turn on **Always On** from the Repl sidebar to keep the
     process alive.
   - Alternatively, use the **Deployments** feature (Static/Autoscale) to run the bot as a
     background service.
   - If neither option is available, consider an external uptime monitor (e.g., UptimeRobot)
     that pings a lightweight web endpoint you expose via the bot to prevent sleeping.
6. **Troubleshooting tips.**
   - If the Repl restarts unexpectedly, review the **Shell** logs for Python exceptions or
     missing environment variables.
   - Use `pip install --upgrade pip` when encountering dependency build errors.
   - Ensure `python3 -m bot` is running in the foreground; closing the Shell tab stops the bot
     unless Always On or Deployments is configured.
   - Replit containers have limited storage; periodically clean the `downloads/` directory or
     connect an external storage solution if you hit the quota.

### Installation
- Install required modules.
```sh
apt install -y git python3 ffmpeg
```
- Clone this git repository.
```sh 
git clone https://github.com/viperadnan-git/google-drive-telegram-bot
```
- Change Directory
```sh 
cd google-drive-telegram-bot
```
- Install requirements with pip3
```sh 
pip3 install -r requirements.txt
```

### Configuration
**There are two Ways for configuring this bot.**
1. Add values to Environment Variables. And add a `ENV` var to Anything to enable it.
2. Add values in [config.py](./bot/config.py). And make sure that no `ENV` environment variables existing.

### Configuration Values
- `BOT_TOKEN` - Get it by contacting to [BotFather](https://t.me/botfather)
- `APP_ID` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)
- `API_HASH` - Get it by creating app on [my.telegram.org](https://my.telegram.org/apps)
- `SUDO_USERS` - List of Telegram User ID of sudo users, seperated by space.
- `SUPPORT_CHAT_LINK` - Telegram invite link of support chat.
- `DATABASE_URL` - Postgres database url.
- `DOWNLOAD_DIRECTORY` - Custom path for downloads. Must end with a forward `/` slash. (Default to `./downloads/`)

### Deploy 
```sh 
python3 -m bot
```

## Credits
- [Dan](https://github.com/delivrance) for creating [PyroGram](https://pyrogram.org)
- [Spechide](https://github.com/Spechide) for [gDriveDB.py](./bot/helpers/sql_helper/gDriveDB.py)
- [Shivam Jha](https://github.com/lzzy12) for [Clone Feature](./bot/helpers/gdrive_utils/gDrive.py) from [python-aria-mirror-bot](https://github.com/lzzy12/python-aria-mirror-bot)

## Copyright & License
- Copyright (©) 2020 by [Adnan Ahmad](https://github.com/viperadnan-git)
- Licensed under the terms of the [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](./LICENSE)