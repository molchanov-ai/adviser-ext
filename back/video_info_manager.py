from yt_manager import YtManager


class VideoInfoManager:

  # TODO: async
  @classmethod
  def video_info(cls, video_id: str):
    video_request = YtManager.youtube.videos().list(part='snippet', id=video_id)
    response = video_request.execute()

    if 'items' not in response or len(response['items']) == 0:
      return None

    video = response['items'][0]

    return video['snippet']
