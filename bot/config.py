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
    START_MSG = "**你好 {}。**\n__我是 Google Drive 上传机器人。你可以使用我将直链或 Telegram 文件上传到 Google Drive。__\n__了解更多功能请发送 /help。__"

    HELP_MSG = [
        ".",
        "**Google Drive Uploader**\n__我可以把直链或 Telegram 文件上传到你的 Google Drive。只需授权我访问你的账号，然后把直链或文件发给我即可。__\n\n我还有更多功能！想要了解吗？请按照下面的教程并仔细阅读每条提示。",

        f"**Google Drive 授权**\n__发送 /{BotCommands.Authorize[0]} 命令获取授权链接，打开并按提示操作，然后把最终得到的代码发给我。使用 /{BotCommands.Revoke[0]} 可以撤销当前登录的 Google Drive 账号。__\n\n**注意：在完成授权之前，我只会响应 /{BotCommands.Authorize[0]} 命令，因此必须先完成授权！**",

        f"**直链下载**\n__把可直接下载的链接发给我，我会在服务器下载并上传到你的 Google Drive。你可以在链接后使用 ' | ' 与新文件名分隔，以便在上传前重命名。__\n\n**__示例：__**\n```https://example.com/AFileWithDirectDownloadLink.mkv | 新文件名.mkv```\n\n**Telegram 文件**\n__发送 Telegram 文件给我即可上传到你的 Google Drive。注意：Telegram 下载速度较慢，大文件可能需要更长时间。__\n\n**YouTube-DL 支持**\n__使用 youtube-dl 下载。\n命令：/{BotCommands.YtDl[0]} (YouTube 链接或任意 youtube-dl 支持的链接)__",

        f"**自定义上传文件夹**\n__想将文件保存到自定义文件夹或 TeamDrive？\n使用 /{BotCommands.SetFolder[0]} (文件夹链接) 设置自定义上传目录。\n之后的所有文件都会保存到你提供的文件夹中。__",

        f"**删除 Google Drive 文件**\n__使用 /{BotCommands.Delete[0]} (文件或文件夹链接) 删除文件，或在我的消息下回复 /{BotCommands.Delete[0]}。\n你也可以使用 /{BotCommands.EmptyTrash[0]} 清空垃圾桶。\n注意：文件会被永久删除，此操作无法撤销。\n\n**复制 Google Drive 文件**\n__是的，可以克隆或复制 Google Drive 文件。\n使用 /{BotCommands.Clone[0]} (文件/文件夹 ID 或链接) 将其复制到你的 Google Drive。__",

        "**规则与注意事项**\n__1. 请勿复制体积巨大的 Google Drive 文件/文件夹，可能导致机器人卡住或文件损坏。\n2. 请一次只发送一个请求，否则机器人会终止所有任务。\n3. 不要发送极慢的直链，建议先使用转存服务。\n4. 请勿滥用或过度使用该免费服务。__",

        # Dont remove this ↓ if you respect developer.
        "**Developed by @viperadnan**"
        ]

    RATE_LIMIT_EXCEEDED_MESSAGE = "❗ **超出速率限制。**\n__用户调用次数已达上限，请 24 小时后再试。__"

    FILE_NOT_FOUND_MESSAGE = "❗ **未找到文件/文件夹。**\n__文件 ID - {} 不存在或当前账号无法访问。__"

    INVALID_GDRIVE_URL = "❗ **无效的 Google Drive 链接**\n请确认链接格式正确。"

    COPIED_SUCCESSFULLY = "✅ **复制成功。**\n[{}]({}) __({})__"

    NOT_AUTH = f"🔑 **你还没有授权任何 Google Drive 账号。**\n__发送 /{BotCommands.Authorize[0]} 进行授权。__"

    DOWNLOADED_SUCCESSFULLY = "📤 **开始上传文件...**\n**文件名：** ```{}```\n**大小：** ```{}```"

    UPLOADED_SUCCESSFULLY = "✅ **上传成功。**\n[{}]({}) __({})__"

    DOWNLOAD_ERROR = "❗**下载失败**\n{}\n__链接 - {}__"

    DOWNLOADING = "📥 **正在下载文件...**\n链接： ```{}```"

    ALREADY_AUTH = "🔒 **当前 Google Drive 账号已授权。**\n__使用 /revoke 撤销当前账号。\n向我发送直链或文件即可上传到 Google Drive。__"

    FLOW_IS_NONE = f"❗ **无效的代码**\n__请先执行 {BotCommands.Authorize[0]}。__"

    AUTH_SUCCESSFULLY = '🔐 **已成功授权 Google Drive 账号。**'

    INVALID_AUTH_CODE = '❗ **无效的代码**\n__你提供的代码无效或已被使用，请通过授权链接重新生成。__'

    PROVIDE_AUTH_CODE = f"❗ **请提供 /{BotCommands.Authorize[0]} 获得的授权链接或代码。**\n__发送 /{BotCommands.Authorize[0]} 以重新获取链接，打开并把最终跳转的完整地址发给我。__"

    AUTH_TEXT = "⛓️ **要授权你的 Google Drive 账号，请访问这个 [链接]({}) 并复制类似 http://localhost/?code= 的完整地址。**\n__打开链接 > 授权 > 复制最终地址 > 发给我__"

    DOWNLOAD_TG_FILE = "📥 **正在下载文件...**\n**文件名：** ```{}```\n**大小：** ```{}```\n**MimeType：** ```{}```"

    PARENT_SET_SUCCESS = '🆔✅ **已成功设置自定义文件夹链接。**\n__你的自定义文件夹 ID - {}\n使用__ ```/{} clear``` __可以清除设置。__'

    PARENT_CLEAR_SUCCESS = f'🆔🚮 **已清除自定义文件夹 ID。**\n__使用__ ```/{BotCommands.SetFolder[0]} (文件夹链接)``` __重新设置。__'

    CURRENT_PARENT = "🆔 **当前的自定义文件夹 ID - {}**\n__使用__ ```/{} (文件夹链接)``` __进行修改。__"

    REVOKED = f"🔓 **已成功撤销当前登录的账号。**\n__使用 /{BotCommands.Authorize[0]} 重新授权以继续使用机器人。__"

    NOT_FOLDER_LINK = "❗ **无效的文件夹链接。**\n__该链接不属于文件夹。__"

    CLONING = "🗂️ **正在复制到 Google Drive...**\n__链接 - {}__"

    PROVIDE_GDRIVE_URL = "**❗ 请提供有效的 Google Drive 链接并附带命令。**\n__用法 - /{} (Google Drive 链接)__"

    INSUFFICIENT_PERMISSONS = "❗ **你没有该文件的足够权限。**\n__文件 ID - {}__"

    DELETED_SUCCESSFULLY = "🗑️✅ **文件删除成功。**\n__文件已被永久删除！\n文件 ID - {}__"

    WENT_WRONG = "⁉️ **错误：发生未知问题**\n__请稍后重试。__"

    EMPTY_TRASH = "🗑️🚮**垃圾桶已清空！**"

    PROVIDE_YTDL_LINK = "❗**请提供有效的 YouTube-DL 支持链接。**"

    PROVIDE_DIRECT_LINK = (
        "❗**Please provide a direct download link.**\n__Usage - /{} (Link | Optional File Name)__"
        "\n🇨🇳 **提示：请发送直接下载链接。**\n__用法 - /{} (链接 | 可选文件名)__"
    )
