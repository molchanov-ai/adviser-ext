from youtube_transcript_api import YouTubeTranscriptApi

class ContentManager:
  @classmethod
  def content(cls):
    transcripts = YouTubeTranscriptApi.list_transcripts('LegCx9q_I8s')
    # TODO: check if no transcript available
    for t in transcripts:
      srt = t.fetch()
      text = ' '.join([x['text'] for x in srt])
      break
    return text