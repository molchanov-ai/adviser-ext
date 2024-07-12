from .balancer import Balancer

import json
import logging

class ContentAgent:
  @classmethod
  async def summary(cls, text):
    llama = Balancer.get_llama()

    tokens_words = 2/3
    max_tokens = 7600

    # NOTE: 5 sec requirements don't give us an opportunity to load more sentences.
    # But we could to load from different pieces of text
    # But the main of the video is going at first max sentences
    content_text = text[:int(max_tokens*tokens_words)]
    ret_format = '{"summary": "<your summary>"}'
    response = await llama.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[
            {
                "content": "You are an ideal video summarizator. You create summaries in one sentence from video text. In result you write only summary without any other sentences. Write result in json format",
                "role": "system"
            },
            {
                "content": f'Please, create a one-sentence summary of this video text. Return format: {ret_format}. Video text:\n{content_text}',
                "role": "user"
            },
        ],
    )

    content_summary = response.choices[0].message.content
    try:
      first_bracet = content_summary.index('{')
      last_bracet = content_summary.rindex('}')
      json_comments_str = content_summary[first_bracet: last_bracet+1]
      content_summary: str = json.loads(json_comments_str)['summary']
    except:
        logging.error(f'Could not json summary: {content_summary}')

    return content_summary