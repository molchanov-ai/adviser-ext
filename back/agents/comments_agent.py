from .balancer import Balancer

import json
import logging


class CommentsAgent:
  @classmethod
  async def summary(cls, comments: str):
    llama = Balancer.get_llama()

    tokens_words = 2/3
    max_tokens = 7600

    comments = comments[:int(max_tokens*tokens_words)]
    if comments is None:
      comments_summary = 'Not enough comments'
    else:
      ret_format = '{"summary": "<your summary>"}'
      response = await llama.chat.completions.create(
          model="meta-llama/Llama-3-8b-chat-hf",
          messages=[
              {
                  "content": "You are an ideal video comments summarizator. You create one sentence summary of the comments. You must return only one sentence summary for all comments!! Otherwise you will be killed!! Pay more attention to emotions and reactions of people. You should understand do they like the video or not and why. You must use smiles for better text reading or you will be killed!! Write result in correct json format that can be compiled in python",
                  "role": "system"
              },
              {
                  "content": f'Please, create a one-sentence summary of this video comments. Return format: {ret_format}. Use escaping for quotes in text because you are returning json!! Comments:\n{comments}',
                  "role": "user"
              },
          ],
      )

      comments_summary = response.choices[0].message.content
      try:
        first_bracet = comments_summary.index('{')
        last_bracet = comments_summary.rindex('}')
        json_comments_str = comments_summary[first_bracet: last_bracet+1]
        value_index = json_comments_str.index(':')
        value = json_comments_str[value_index+1:].lstrip()[1:-2]
        value = value.replace('"', "'")
        key = json_comments_str[:value_index]
        closing = '}'
        prepared_str = f'{key}: "{value}"{closing}'

        logging.error(f'_prepared_str_: {prepared_str}')
        comments_summary: str = json.loads(prepared_str)['summary']
      except:
          logging.error(f'Could not json summary: {comments_summary}')

    return comments_summary

