from content_manager import ContentManager
import requests
from fastapi import FastAPI, Query, File, UploadFile, Form
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from together import AsyncTogether
import os

llama = AsyncTogether(api_key=os.environ['LLAMA_API_KEY'])

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

    clickbait_rating, video_summary, comments_summary = await fetch_data_from_llama(
        video_id)

    return PlainTextResponse(
        content=json.dumps({
            'clickbaitRating': clickbait_rating,
            'videoSummary': video_summary,
            'commentsSummary': comments_summary
        }))


async def fetch_data_from_llama(video_id):
    content = ContentManager.content(video_id)
    response = await llama.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[
            {
                "content": "You are an ideal video summarizator. You create summaries in one sentence from video text",
                "role": "assistant"
            },
            {
                "content": f'Please, create a one-sentence summary of this video text: {content}',
                "role": "user"
            },
        ],
    )

    text = response.choices[0].message.content
    # return "45/100", "This video explains the basics of AI and its applications.", "This video is very informative and well-explained."
    return ["45/100", text, "Cool Video"]
