from managers.comments_manager import CommentsManager
from managers.content_manager import ContentManager
from managers.video_info_manager import VideoInfoManager

import json
import logging
import os

from together import AsyncTogether
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

llamas = [AsyncTogether(api_key=os.environ['LLAMA_API_KEY']), AsyncTogether(
    api_key=os.environ['LLAMA_API_KEY2'])]

app = FastAPI()

origins = [
    "https://www.youtube.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get('/video-info')
async def video_info(videoId: str):
    video_id = videoId

    clickbait_rating, video_summary, comments_summary, justification = await fetch_data_from_llama(
        video_id)

    return PlainTextResponse(
        content=json.dumps({
            'clickbaitRating': clickbait_rating,
            'videoSummary': video_summary,
            'commentsSummary': comments_summary,
            'justification': justification
        }))


async def fetch_data_from_llama(video_id):
    # TODO: case no words or transcriptions or Exception
    # so we need comments here to make content summary from it
    content = ContentManager.content(video_id)
    comments = CommentsManager.comments(video_id)
    video_info = VideoInfoManager.video_info(video_id)

    if not video_info:
      return ['', '', '', 'Error occured. Please try again']
    
    title = video_info['title']
    desc = video_info['description']

    batches = []
    last_word = 0
    tokens_words = 2/3
    max_tokens = 7600
    batch_size = int(tokens_words*max_tokens)
    while last_word < len(content):
      batches.append(content[last_word: last_word + batch_size])
      last_word += batch_size

    # NOTE: 5 sec requirements don't give us an opportunity to load more sentences.
    # But we could to load from different pieces of text
    # But the main of the video is going at first max sentences
    content_text = batches[0]
    response = await llamas[0].chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[
            {
                "content": "You are an ideal video summarizator. You create summaries in one sentence from video text. In result you write only summary without any other sentences. Write result in json format",
                "role": "system"
            },
            {
                "content": f'Please, create a one-sentence summary of this video text: {content_text}',
                "role": "user"
            },
        ],
    )

    content_summary = response.choices[0].message.content
    try:
      content_summary: str = json.loads(content_summary)['summary']
    except:
        try:
          first_bracet = content_summary.index('{')
          content_summary = content_summary[first_bracet:]
          content_summary = json.loads(content_summary)['summary']
        except:
           logging.error(f'Could not json with processing summary: {content_summary}')
        logging.error(f'Could not json summary: {content_summary}')

    comments = comments[:int(max_tokens*tokens_words)]
    if comments is None:
      comments_summary = 'Not enough comments'
    else:
      ret_format = '{"summary": "<your summary>"}'
      response = await llamas[0].chat.completions.create(
          model="meta-llama/Llama-3-8b-chat-hf",
          messages=[
              {
                  "content": "You are an ideal video comments summarizator. You create one sentence summary of the comments. You must return only one sentence summary for all comments!! Otherwise you will be killed!! Pay more attention to emotions and reactions of people. You should understand do they like the video or not and why. Write result in json format",
                  "role": "system"
              },
              {
                  "content": f'Please, create a one-sentence summary of this video comments. Return format: {ret_format}. Comments:\n{comments}',
                  "role": "user"
              },
          ],
      )

      comments_summary = response.choices[0].message.content
      try:
        comments_summary: str = json.loads(comments_summary)['summary']
      except:
          try:
            first_bracet = comments_summary.index('{')
            last_bracet = comments_summary.rindex('}')
            comments_summary = comments_summary[first_bracet:last_bracet+1]
            comments_summary = json.loads(comments_summary)['summary']
          except:
            logging.error(
                f'Could not json with processing summary: {comments_summary}')
          logging.error(f'Could not json summary: {comments_summary}')

    ### rater
    ret_format = '{"rating": <your rating from 0 to 100>, "justification": <your justification about rating>}'
    response = await llamas[1].chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[
             {
                  "content": "You are an ideal video rater. You must give a rating for the video based on its properties given by user. Also you must give a justification about it just in one sentence!!! If there will be more sentences you will be killed. Write result in json format",
                  "role": "system"
              },
             {
                  "content": f'''Please, rate the video by properties:
                  title: {title},
                  description: {desc},
                  content summary: {content_summary},
                  comments summary: {comments_summary}.

                  Return format: {ret_format}''',
                  "role": "user"
              },
             ],
        )

    rating_text: str = response.choices[0].message.content
    try:
      json_text = rating_text[rating_text.index('{'): rating_text.rindex('}')+1]
      jsoned = json.loads(json_text)
      rating: int = jsoned['rating']
      justification: str = jsoned['justification']
    except:
      logging.error(f'_Could_not_json_rating_: {rating_text}')
      rating = rating_text[:int(len(rating_text)/2)]
      justification = rating_text[int(len(rating_text)/2):]

    return [str(rating), content_summary, comments_summary, justification]
