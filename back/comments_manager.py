from back.yt_manager import YtManager

class CommentsManager:

  @classmethod
  def comments(cls, video_id: str):
    comments_request = YtManager.youtube.commentThreads().list(part='snippet,replies',
                                                    maxResults=100, videoId=video_id)
    response = comments_request.execute()
    print(response)

    return response
