from .yt_manager import YtManager

import asyncio

class CommentsManager:

  @classmethod
  async def comments(cls, video_id: str):
    comments_request = YtManager.youtube.commentThreads().list(part='snippet,replies',
                                                    maxResults=100, videoId=video_id)
    try:
      response = await asyncio.to_thread(comments_request.execute)
    except Exception as e:
      response = None

    if response is None or 'items' not in response or len(response['items']) == 0:
      return None

    comments = ''

    for comment in response['items']:
      text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
      replies = ''
      if 'replies' in comment:
        replies = 'Replies:\n'
        for reply in comment['replies']['comments']:
          reply_text = reply['snippet']['textDisplay']
          replies += f'{reply_text}\n'
      comments += f'Comment: {text}\n{replies}'

    return comments
