from apiclient.discovery import build

class YtManager:
  with open('creds.env', 'r') as f:
    api_key = f.read()
    youtube = build('youtube', 'v3', developerKey=api_key)
