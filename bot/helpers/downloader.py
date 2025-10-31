import os
import wget
import glob
import yt_dlp
from pySmartDL import SmartDL
from urllib.error import HTTPError
from yt_dlp.utils import DownloadError
from bot import DOWNLOAD_DIRECTORY, LOGGER


def download_file(url, dl_path):
  try:
    dl = SmartDL(url, dl_path, progress_bar=False)
    LOGGER.info(f'Downloading: {url} in {dl_path}')
    dl.start()
    return True, dl.get_dest()
  except HTTPError as error:
    return False, error
  except Exception as error:
    try:
      filename = wget.download(url, dl_path)
      if os.path.isabs(filename):
        return True, filename
      absolute_path = os.path.abspath(filename)
      download_root = os.path.abspath(DOWNLOAD_DIRECTORY)
      if absolute_path.startswith(download_root):
        return True, absolute_path
      return True, os.path.join(download_root, os.path.basename(filename))
    except HTTPError:
      return False, error


def utube_dl(link):
  ytdl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(title)s.%(ext)s'),
    'noplaylist': True,
    'logger': LOGGER,
    'format': 'bestvideo+bestaudio/best',
    'geo_bypass_country': 'IN'
  }
  with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
    try:
      meta = ytdl.extract_info(link, download=True)
    except DownloadError as e:
      return False, str(e)
    for path in glob.glob(os.path.join(DOWNLOAD_DIRECTORY, '*')):
      if path.endswith(('.avi', '.mov', '.flv', '.wmv', '.3gp','.mpeg', '.webm', '.mp4', '.mkv')) and \
          path.startswith(ytdl.prepare_filename(meta)):
        return True, path
    return False, 'Something went wrong! No video file exists on server.'
