from .balancer import Balancer

import json
import logging


class RaterAgent:
  @classmethod
  async def rate(cls, video_props: dict):
    llama = Balancer.get_llama()

    ret_format = '{"rating": <your rating from 0 to 100>, "justification": <your justification about rating>}'
    response = await llama.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[
            {
                "content": """You are an ideal video clickbate rater. 
You must give a clickbait rating for the video based 
on its properties given by user. So you should understand 
how video's properties attract attention and encourage people. 
The most weight must have a video title. Examples of 100/100 clickbait: 
"These two zodiac signs will be swimming in money in 2021",
"To get rid of fungus, rub in a penny Soviet ...",
"This guy from your city became a millionaire thanks to...",
"Nightmares of 21st century",
"This is what kills you every day",
"Naked girl is dancing"

Example of 0/100 clickbait: "Description how software works?"

Clickbait conditions with rating points:
1) contains sensation information, that can surprise a user - 40 points
2) contains mystery - 30 points
3) claims a problem common for people something like human routine, love problems, criminal, etc - 70 points
4) evokes primitive emotions: curiosity, anger, sexuality, envy, thirst for easy money - 30 points
5) contains wow effect - 80 points
6) tells about something epic - 50 points
7) info about someone famous – 30 points

Sum these points above to get a rating otherwise you will be killed!! If the sum is > 100, the rating is 100.
Think yourself!

Also you must give a justification about it just in one sentence!!!
If there will be more sentences you will be killed.
Write result in json format""",
                "role": "system"
            },
            {
                "content": f'''Please, rate the clickbait of the video by properties:
                  {video_props}.

                  Return format: {ret_format}''',
                "role": "user"
            },
        ],
    )

    rating_text: str = response.choices[0].message.content
    try:
      json_text = rating_text[rating_text.index(
          '{'): rating_text.rindex('}')+1]
      jsoned = json.loads(json_text)
      rating: int = jsoned['rating']
      justification: str = jsoned['justification']
    except:
      logging.error(f'_Could_not_json_rating_: {rating_text}')
      rating = 0
      justification = rating_text

    return f'{rating}/100', justification
