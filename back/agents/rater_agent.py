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
                "content": "You are an ideal video rater. You must give a rating for the video based on its properties given by user. Also you must give a justification about it just in one sentence!!! If there will be more sentences you will be killed. Write result in json format",
                "role": "system"
            },
            {
                "content": f'''Please, rate the video by properties:
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
      rating = rating_text[:int(len(rating_text)/2)]
      justification = rating_text[int(len(rating_text)/2):]

    return f'{rating}/100', justification
