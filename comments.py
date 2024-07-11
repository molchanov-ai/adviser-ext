from apiclient.discovery import build

with open('creds.env', 'r') as f:
  api_key = f.read()
  youtube = build('youtube', 'v3', developerKey=api_key)

comments_request = youtube.commentThreads().list(part='snippet,replies',
                                                 maxResults=100, videoId='m9DhJiPtC4Q')
response = comments_request.execute()
print(response)
