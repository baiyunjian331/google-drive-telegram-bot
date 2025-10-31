---
title: Google Drive Telegram Bot
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "3.38.0"
app_file: app.py
pinned: false
---

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
- [X] yt-dlp support.
- [X] 提供完整的中文提示信息，优化中文使用体验🎯
## ToDo 
- [ ] Handle more exceptions.
- [ ] LOGGER support.
- [ ] Service account support.
- [ ] Update command.

## Deploying

### Deploy on [Heroku](https://heroku.com)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Deploy on [Hugging Face Spaces](https://huggingface.co/spaces)
1. 在 Hugging Face 创建 **Space**，选择 **Python** 模板并关联本仓库（或导入自己的 Fork）。
2. **可选（推荐）**：在仓库根目录添加 `packages.txt`，写入一行 `ffmpeg`，以便 Space 自动安装系统级 ffmpeg。
3. 在 Space 的 **Settings → Variables & secrets** 面板添加下列变量：
   - `ENV=1`
   - `BOT_TOKEN`、`APP_ID`、`API_HASH`
   - `SUPPORT_CHAT_LINK`
   - `G_DRIVE_CLIENT_ID`、`G_DRIVE_CLIENT_SECRET`（Google Cloud OAuth，回调需包含 `http://localhost/`）
   - `SUDO_USERS`（空格分隔 Telegram 用户 ID，至少包含自己的 ID）
   - `DATABASE_URL=sqlite:///data/gdrive.db`（推荐：持久化到 Space 的 `/data` 目录）
   - `DOWNLOAD_DIRECTORY=/data/downloads/`（若省略，将自动回落到 `/data/downloads`）
   - `DATA_DIR=/data`（如需显式控制数据根目录）
4. 在 **Settings → Runtime** 中将 **Start command** 设置为 `python app.py`（或保持默认，Space 会自动寻找 `app` 实例）。
5. 点击 **Restart this Space**。首次启动后，在 Telegram 中向机器人发送 `/authorize`，按照提示完成 Google Drive 授权并确认 Space 日志无报错。

### Deploy on [Render](https://render.com)
1. 在 Render 创建 **New Web Service**，选择连续部署（Continuous Deployment），代码仓库指向本项目或你的 Fork。
2. 环境变量在 Render 的 **Environment → Environment Variables** 中添加：
   - `ENV=1`
   - `BOT_TOKEN`、`APP_ID`、`API_HASH`
   - `SUPPORT_CHAT_LINK`
   - `G_DRIVE_CLIENT_ID`、`G_DRIVE_CLIENT_SECRET`
   - `SUDO_USERS`（至少包含你的 Telegram 用户 ID）
   - `DATABASE_URL=sqlite:////var/data/gdrive.db`（Render 的 `/var/data` 为持久磁盘）
   - `DOWNLOAD_DIRECTORY=/var/data/downloads/`
   - **可选**：`DATA_DIR=/var/data`
3. 在 **Build Command** 填写 `pip install -r requirements.txt`；**Start Command** 使用 `python app.py`。
4. 至少为该服务启用一个持久磁盘（Persistent Disk）挂载到 `/var/data`，保证数据库和临时文件不丢失。
5. 部署完成后在 Telegram 中执行 `/authorize`，确认 OAuth 授权与上传流程正常。

### Deploy on Replit
1. 在 Replit 上选择 **Create Repl → Import from GitHub**，填写本仓库地址并创建实例。
2. 等待 Replit 根据 `replit.nix` 构建基础环境（已包含 Python 3.11 与 `ffmpeg` 二进制）。
3. 在 Shell 中运行 `pip install -r requirements.txt` 安装 Python 依赖。
4. 通过 Replit 的 **Secrets** 面板添加配置（至少包括 `ENV=1`、`BOT_TOKEN`、`APP_ID`、`API_HASH`、`SUPPORT_CHAT_LINK`、可选的 `DATABASE_URL`、`G_DRIVE_CLIENT_ID`、`G_DRIVE_CLIENT_SECRET` 等）。`SUDO_USERS` 可留空，若需要请填写以空格分隔的 Telegram 用户 ID。
5. 点击 **Run** 或在 Shell 中执行 `python3 -m bot` 即可启动，日志会输出到 Replit 控制台。

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

## Replit 部署常见问题及解决方案
- **缺少运行入口**：Replit 默认无法识别 Heroku 的 `Procfile`。仓库提供的 `.replit` 文件会将运行命令设置为 `python3 -m bot`，确保点击 **Run** 后可以直接启动。
- **未设置 `SUDO_USERS` 导致启动报错**：如果未提供该环境变量，旧版本会在解析时崩溃。现在即使留空也能正常启动，若需要自定义请填写以空格分隔的数字 ID。
- **缺少 `ffmpeg` 可执行文件**：YouTube-DL 与部分下载流程依赖 `ffmpeg`，Replit 会根据 `replit.nix` 自动安装该二进制。如依旧提示缺少命令，可在 Shell 中执行 `ffmpeg -version` 验证。
## Credits
- [Dan](https://github.com/delivrance) for creating [PyroGram](https://pyrogram.org)
- [Spechide](https://github.com/Spechide) for [gDriveDB.py](./bot/helpers/sql_helper/gDriveDB.py)
- [Shivam Jha](https://github.com/lzzy12) for [Clone Feature](./bot/helpers/gdrive_utils/gDrive.py) from [python-aria-mirror-bot](https://github.com/lzzy12/python-aria-mirror-bot)

## Copyright & License
- Copyright (©) 2020 by [Adnan Ahmad](https://github.com/viperadnan-git)
- Licensed under the terms of the [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](./LICENSE)
