import logging
import os

from together import AsyncTogether

'''
With such simple arch we don't need to
check RateLimit errors because
if next llama has RateLimit error
we have no available llama
'''
class Balancer:
  _llamas = [AsyncTogether(api_key=os.environ['LLAMA_API_KEY']), AsyncTogether(
      api_key=os.environ['LLAMA_API_KEY2']), AsyncTogether(
      api_key=os.environ['LLAMA_API_KEY3'])]
  _last_used = None
  
  @classmethod
  def get_llama(cls):
    if Balancer._last_used is None:
      Balancer._last_used = 0
      return Balancer._llamas[0]
    
    Balancer._last_used = (Balancer._last_used + 1) % 3
    return Balancer._llamas[Balancer._last_used]
