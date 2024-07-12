from .yt_manager import YtManager

import asyncio

class VideoInfoManager:

  # TODO: async
  @classmethod
  async def video_info(cls, video_id: str):
    video_request = YtManager.youtube.videos().list(part='snippet', id=video_id)
    response = await asyncio.to_thread(video_request.execute)

    if 'items' not in response or len(response['items']) == 0:
      return None

    video = response['items'][0]

    return video['snippet']
