import requests
from flask import Flask, jsonify, request
from fastapi import FastAPI, Query, File, UploadFile, Form
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import json

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
def read_root():
    return {"Hello": "World"}

@app.get('/video-info')
def video_info(videoId: str):
    video_id = videoId
    if not video_id:
        return jsonify({'error': 'No video ID provided'}), 400

    # Call Llama3-8b API or any other provider to get video data
    clickbait_rating, video_summary, comments_summary = fetch_data_from_llama(
        video_id)

    return PlainTextResponse(content=json.dumps({
        'clickbaitRating': clickbait_rating,
        'videoSummary': video_summary,
        'commentsSummary': comments_summary
    }))


def fetch_data_from_llama(video_id):
    # Dummy data for now; replace with actual API calls
    return "45/100", "This video explains the basics of AI and its applications.", "This video is very informative and well-explained."

