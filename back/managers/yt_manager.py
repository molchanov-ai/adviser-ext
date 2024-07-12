from googleapiclient.discovery import build

import os

class YtManager:
  api_key = os.environ['YT_API_KEY']
  youtube = build('youtube', 'v3', developerKey=api_key)
