import re
import json
from httplib2 import Http
from bot import LOGGER, G_DRIVE_CLIENT_ID, G_DRIVE_CLIENT_SECRET
from bot.config import Messages
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bot.helpers.sql_helper import gDriveDB
from bot.config import BotCommands
from bot.helpers.utils import CustomFilters


OAUTH_SCOPE = "https://www.googleapis.com/auth/drive"
REDIRECT_URI = "http://localhost/"

flows = {}

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Authorize))
async def _auth(client, message):
  user_id = message.from_user.id
  creds = gDriveDB.search(user_id)
  if creds is not None:
    creds.refresh(Http())
    gDriveDB._set(user_id, creds)
    await message.reply_text(Messages.ALREADY_AUTH, quote=True)
  else:
    try:
      flow = OAuth2WebServerFlow(
              G_DRIVE_CLIENT_ID,
              G_DRIVE_CLIENT_SECRET,
              OAUTH_SCOPE,
              redirect_uri=REDIRECT_URI,
              response_type='code',
              access_type='offline',
              prompt='consent'
      )
      flows[user_id] = flow
      auth_url = flow.step1_get_authorize_url()
      LOGGER.info(f'AuthURL:{user_id}')
      await message.reply_text(
        text=Messages.AUTH_TEXT.format(auth_url),
        quote=True,
        reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("授权链接", url=auth_url)]]
              )
        )
    except Exception as e:
      await message.reply_text(f"**ERROR:** ```{e}```", quote=True)

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Revoke) & CustomFilters.auth_users)
def _revoke(client, message):
  user_id = message.from_user.id
  try:
    gDriveDB._clear(user_id)
    LOGGER.info(f'Revoked:{user_id}')
    message.reply_text(Messages.REVOKED, quote=True)
  except Exception as e:
    message.reply_text(f"**ERROR:** ```{e}```", quote=True)


@Client.on_message(filters.private & filters.incoming & filters.text & ~CustomFilters.auth_users)
async def _token(client, message):
  text = (message.text or "").strip()
  code = None

  if "?code=" in text:
    try:
      code = text.split("?code=", 1)[1].split("&", 1)[0]
    except IndexError:
      code = None
  elif text:
    code = text.split()[-1]

  if not code:
    await message.reply_text(Messages.PROVIDE_AUTH_CODE, quote=True)
    return

  token = code.strip().split()[-1]
  allowed_prefixes = ("4/", "1/")

  if token and token.startswith(allowed_prefixes):
    creds = None
    user_id = message.from_user.id
    flow = flows.pop(user_id, None)
    if flow:
      sent_message = await message.reply_text("🕵️**正在验证授权代码...**", quote=True)
      try:
        creds = flow.step2_exchange(token)
        gDriveDB._set(user_id, creds)
        LOGGER.info(f'AuthSuccess: {user_id}')
        await sent_message.edit(Messages.AUTH_SUCCESSFULLY)
      except FlowExchangeError:
        await sent_message.edit(Messages.INVALID_AUTH_CODE)
      except Exception as e:
        await sent_message.edit(f"**ERROR:** ```{e}```")
    else:
      await message.reply_text(Messages.FLOW_IS_NONE, quote=True)
  else:
    await message.reply_text(Messages.INVALID_AUTH_CODE, quote=True)
