import asyncio

from youtube_transcript_api import YouTubeTranscriptApi

class ContentManager:
  @classmethod
  async def content(cls, video_id: str):
    transcripts = await asyncio.to_thread(YouTubeTranscriptApi.list_transcripts, video_id=video_id)
    for t in transcripts:
      srt = await asyncio.to_thread(t.fetch)
      text = ' '.join([x['text'] for x in srt])
      break
    return text