import openai
from .cache import redis_cache

from chatgpt_lsp.settings import OPENAI_KEY


class OpenAI:
    """
    OpenAI API client
    """
    def __init__(self):
        self.openai = openai
        self.openai.api_key = OPENAI_KEY

    def answer(self, question):
        response = self.openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.5,
            max_tokens=2048,
            stop=None,
        )
        return response.get("choices")[0].get("text")


def set_answer(cache_id, question):
    """
    查询并缓存openapi返回的答案
    """
    openai_api = OpenAI()
    answer = openai_api.answer(question).strip()
    redis_cache.push(cache_id, answer)
    print(f'查询答案是: {answer}')
