from .balancer import Balancer

import json
import logging

class ContentAgent:
  @classmethod
  async def summary(cls, text):
    llama = Balancer.get_llama()

    batches = []
    last_word = 0
    tokens_words = 2/3
    max_tokens = 7600
    batch_size = int(tokens_words*max_tokens)
    while last_word < len(text):
      batches.append(text[last_word: last_word + batch_size])
      last_word += batch_size

    # NOTE: 5 sec requirements don't give us an opportunity to load more sentences.
    # But we could to load from different pieces of text
    # But the main of the video is going at first max sentences
    content_text = batches[0]
    response = await llama.chat.completions.create(
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
           logging.error(
               f'Could not json with processing summary: {content_summary}')
        logging.error(f'Could not json summary: {content_summary}')

    return content_summary