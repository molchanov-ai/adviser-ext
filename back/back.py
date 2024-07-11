from content_manager import ContentManager
import requests
from fastapi import FastAPI, Query, File, UploadFile, Form
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
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
    # TODO: case no words or transcriptions
    content = ContentManager.content(video_id)
    batches = []
    last_word = 0
    tokens_words = 2/3
    max_tokens = 7600
    batch_size = int(tokens_words*max_tokens)
    while last_word < len(content):
      batches.append(content[last_word: last_word + batch_size])
      last_word += batch_size

    # NOTE: 5 sec requirements don't give us an opportunity to load more sentences. But we could to load from different pieces of text
    text = batches[0]
    response = await llama.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[
            {
                "content": "You are an ideal video summarizator. You create summaries in one sentence from video text. In result you write only summary without any other sentences. Write result in json format. Use only russian language in summarys",
                "role": "assistant"
            },
            {
                "content": f'Please, create a one-sentence summary of this video text: {text}',
                "role": "user"
            },
        ],
    )

    text = response.choices[0].message.content
    try:
      text: str = json.loads(text)['summary']
    except:
        try:
          first_bracet = text.index('{')
          text = text[first_bracet:]
          text = json.loads(text)['summary']
        except:
           logging.error(f'Could not json with processing summary: {text}')
        logging.error(f'Could not json summary: {text}')
    # return "45/100", "This video explains the basics of AI and its applications.", "This video is very informative and well-explained."
    return ["45/100", text, "Cool Video"]
