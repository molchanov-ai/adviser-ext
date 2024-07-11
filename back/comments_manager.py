from yt_manager import YtManager

class CommentsManager:

  @classmethod
  def comments(cls, video_id: str):
    comments_request = YtManager.youtube.commentThreads().list(part='snippet,replies',
                                                    maxResults=100, videoId=video_id)
    response = comments_request.execute()
    # print(response)

    if 'items' not in response:
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


    # response['items'][0]['snippet']['topLevelComment']['snippet']['textDisplay']
    # response['items'][3]['replies']['comments'][0]['snippet']['textDisplay']

    return comments
