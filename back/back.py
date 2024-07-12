from agents.comments_agent import CommentsAgent
from agents.content_agent import ContentAgent
from agents.rater_agent import RaterAgent
from managers.comments_manager import CommentsManager
from managers.content_manager import ContentManager
from managers.video_info_manager import VideoInfoManager

import json
import logging

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

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
    # case no words or transcriptions or Exception
    # so we need comments here to make content summary from it
    comments = CommentsManager.comments(video_id)
    try:
      content = ContentManager.content(video_id)
    except Exception as e:
      logging.error(f'_no_content_: {e}')
      content = f'We can not get video content so you should understand its content by comments. The comments:\n{comments}'
    video_info = VideoInfoManager.video_info(video_id)

    if not video_info:
      return ['', '', '', 'Error occured. Please try again']
    
    title = video_info['title']
    desc = video_info['description']
    
    content_summary = await ContentAgent.summary(content)
    comments_summary = await CommentsAgent.summary(comments)
    rating, justification = await RaterAgent.rate({
        'title': title,
        'description': desc,
        'content_summary': content_summary,
        'comments_summary': comments_summary
    })

    return [str(rating), content_summary, comments_summary, justification]
