class config:
    BOT_TOKEN = ""
    APP_ID = ""
    API_HASH = ""
    DATABASE_URL = ""
    SUDO_USERS = "" # Sepearted by space.
    SUPPORT_CHAT_LINK = ""
    DOWNLOAD_DIRECTORY = "./downloads/"
    G_DRIVE_CLIENT_ID = ""
    G_DRIVE_CLIENT_SECRET = ""


class BotCommands:
  Download = ['download', 'dl']
  Authorize = ['auth', 'authorize']
  SetFolder = ['setfolder', 'setfl']
  Revoke = ['revoke']
  Clone = ['copy', 'clone']
  Delete = ['delete', 'del']
  EmptyTrash = ['emptyTrash']
  YtDl = ['ytdl']


class Messages:
    START_MSG = "**你好，{}。**\n__我是 Google Drive 上传机器人。你可以使用我把任何直接链接或 Telegram 文件上传到 Google Drive。__\n__想了解更多，请发送 /help。__"

    HELP_MSG = [
        ".",
        "**Google Drive 上传器**\n__我可以把直接下载链接或 Telegram 文件上传到你的 Google Drive。你只需授权我访问账号，然后发送直接下载链接或 Telegram 文件即可。__\n\n我还有更多功能！想了解吗？请按照本教程仔细阅读每条消息。",

        f"**Google Drive 授权**\n__发送 /{BotCommands.Authorize[0]} 命令，你会收到一个链接。打开链接并按照步骤操作，然后把获得的代码发送到这里。使用 /{BotCommands.Revoke[0]} 可以撤销当前登录的 Google Drive 账号。__\n\n**注意：在完成授权之前，我不会响应任何命令或消息（/{BotCommands.Authorize[0]} 命令除外），因此必须先完成授权！**",

        f"**直接链接**\n__把文件的直接下载链接发给我，我会在服务器上下载并上传到你的 Google Drive。你可以在上传前重命名文件，只需发送“链接 | 新文件名”。__\n\n**__示例：__**\n```https://example.com/AFileWithDirectDownloadLink.mkv | 新文件名.mkv```\n\n**Telegram 文件**\n__要将 Telegram 文件上传到 Google Drive，只需把文件发给我。我会下载并上传。注意：下载 Telegram 文件较慢，大文件可能需要更长时间。__\n\n**YouTube-DL 支持**\n__通过 youtube-dl 下载文件。\n使用 /{BotCommands.YtDl[0]} (YouTube 链接/YouTube-DL 支持的站点链接)__",

        f"**自定义上传文件夹**\n__想把文件上传到自定义文件夹或__ **TeamDrive** __中？\n使用 /{BotCommands.SetFolder[0]} (文件夹链接) 设置自定义上传文件夹。所有文件都会上传到你提供的文件夹中。__",

        f"**删除 Google Drive 文件**\n__删除 Google Drive 文件。使用 /{BotCommands.Delete[0]} (文件/文件夹链接) 删除，或回复机器人的消息并发送 /{BotCommands.Delete[0]}。\n你也可以使用 /{BotCommands.EmptyTrash[0]} 清空垃圾桶。\n注意：文件会被永久删除，此操作无法撤销。\n\n**复制 Google Drive 文件**\n__是的，可以克隆或复制 Google Drive 文件。\n__使用 /{BotCommands.Clone[0]} (文件 ID/文件夹 ID 或链接) 将文件复制到你的 Google Drive。__",

        "**规则与注意事项**\n__1. 不要复制非常大的 Google Drive 文件或文件夹，可能会导致机器人卡死或损坏你的文件。\n2. 请一次只发送一个请求，否则机器人会停止所有进程。\n3. 不要发送速度很慢的链接，请先自行中转。\n4. 请不要滥用、过载或恶意使用此免费服务。__",

        # Dont remove this ↓ if you respect developer.
        "**由 @viperadnan 开发**"
        ]

    RATE_LIMIT_EXCEEDED_MESSAGE = "❗ **超出速率限制。**\n__用户速率限制已达上限，请 24 小时后再试。__"

    FILE_NOT_FOUND_MESSAGE = "❗ **未找到文件/文件夹。**\n__未找到文件 ID - {}。请确认它存在并且当前账号可访问。__"

    INVALID_GDRIVE_URL = "❗ **无效的 Google Drive 链接**\n请确保链接格式正确。"

    COPIED_SUCCESSFULLY = "✅ **复制成功。**\n[{}]({}) __({})__"

    NOT_AUTH = f"🔑 **你还没有授权我上传到任何账号。**\n__发送 /{BotCommands.Authorize[0]} 进行授权。__"

    DOWNLOADED_SUCCESSFULLY = "📤 **正在上传文件...**\n**文件名：** ```{}```\n**大小：** ```{}```"

    UPLOADED_SUCCESSFULLY = "✅ **上传成功。**\n[{}]({}) __({})__"

    DOWNLOAD_ERROR = "❗**下载失败**\n{}\n__链接 - {}__"

    DOWNLOADING = "📥 **正在下载文件...**\n**链接：** ```{}```"

    ALREADY_AUTH = f"🔒 **此 Google Drive 账号已授权。**\n__使用 /{BotCommands.Revoke[0]} 撤销当前账号。__\n__请发送直接链接或文件进行上传__"

    FLOW_IS_NONE = f"❗ **无效的代码**\n__请先运行 {BotCommands.Authorize[0]}。__"

    AUTH_SUCCESSFULLY = '🔐 **已成功授权 Google Drive 账号。**'

    INVALID_AUTH_CODE = '❗ **无效的代码**\n__你发送的代码无效或已被使用。请通过授权链接重新生成。__'

    PROVIDE_AUTH_CODE = f"❗ **请提供 /{BotCommands.Authorize[0]} 返回的授权链接或代码。**\n__发送 /{BotCommands.Authorize[0]} 重新获取链接，打开后把最终跳转的链接发给我。__"

    AUTH_TEXT = "⛓️ **要授权你的 Google Drive 账号，请访问这个 [链接]({}) 并复制类似 http://localhost/?code= 的最终网址。**\n__打开链接 > 授权 > 复制完整网址 > 发到这里__"

    DOWNLOAD_TG_FILE = "📥 **正在下载文件...**\n**文件名：** ```{}```\n**大小：** ```{}```\n**MIME 类型：** ```{}```"

    PARENT_SET_SUCCESS = '🆔✅ **自定义文件夹链接设置成功。**\n__你的自定义文件夹 ID - {}\n使用__ ```/{} clear``` __来清除。__'

    PARENT_CLEAR_SUCCESS = f'🆔🚮 **已清除自定义文件夹 ID。**\n__使用__ ```/{BotCommands.SetFolder[0]} (文件夹链接)``` __重新设置。__'

    CURRENT_PARENT = "🆔 **你当前的自定义文件夹 ID - {}**\n__使用__ ```/{} (文件夹链接)``` __进行更改。__"

    REVOKED = f"🔓 **已成功撤销当前账号。**\n__发送 /{BotCommands.Authorize[0]} 重新授权后继续使用本机器人。__"

    NOT_FOLDER_LINK = "❗ **无效的文件夹链接。**\n__你发送的链接不属于文件夹。__"

    CLONING = "🗂️ **正在复制到 Google Drive...**\n__Google Drive 链接 - {}__"

    PROVIDE_GDRIVE_URL = "❗ **请提供有效的 Google Drive 链接和命令。**\n__用法 - /{} (Google Drive 链接)__"

    INSUFFICIENT_PERMISSONS = "❗ **你没有该文件的足够权限。**\n__文件 ID - {}__"

    DELETED_SUCCESSFULLY = "🗑️✅ **文件已成功删除。**\n__文件已被永久删除！\n文件 ID - {}__"

    WENT_WRONG = "⁉️ **错误：出现问题**\n__请稍后再试。__"

    EMPTY_TRASH = "🗑️🚮**垃圾桶已清空！**"

    PROVIDE_YTDL_LINK = "❗**请提供受 YouTube-DL 支持的有效链接。**"

    PROVIDE_DIRECT_LINK = "❗**请提供直接下载链接。**\n__用法 - /{} (链接 | 可选文件名)__"
