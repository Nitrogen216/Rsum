import openai
import backoff
from utils.env import ensure_openai_api_key
api_key = ensure_openai_api_key()
@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def gpt_response_results(prompt):
    openai.api_key = api_key
    completion = completions_with_backoff(
                model='gpt-3.5-turbo',
                messages=[
            {"role": "system",
             "content": "You are an advanced AI language model designed to engage in personality-based conversations."},
            {"role": "user",
             "content": prompt,
             }],
                temperature=0,
            )
    line_m = ' '.join(completion.choices[0]["message"]["content"].split('\n'))
    return line_m

def test():
    m = gpt_response_results("User: How are you?")
    ss = m.split("User:")[0]
    print(ss)
