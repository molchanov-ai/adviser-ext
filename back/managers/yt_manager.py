from googleapiclient.discovery import build

import os

'''
Here we potentially can have
RateLimit errors
but its very easy to make a balancer
like agents balancer
'''
class YtManager:
  api_key = os.environ['YT_API_KEY']
  youtube = build('youtube', 'v3', developerKey=api_key)
