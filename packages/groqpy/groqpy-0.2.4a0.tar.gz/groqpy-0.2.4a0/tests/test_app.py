from groqpy.groq_agent import GroqAgent
import json
import datetime
import os


GROQ_API_KEY = [
    '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',
    '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',
    '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'
    ]
GROQ_MODEL = 'gemma-7b-it'
GROQ_TEMPERATURE = 0

agent = GroqAgent(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=GROQ_TEMPERATURE, max_attempts=3)

time_dict = {}

while True:
    now = datetime.datetime.now()
    current_time = now.replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

    response = agent.Chat(
'''100 prompt token test.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
This sentence is used to get the prompt token count to 100 tokens.
''', verbose=True, remember=False)
    prompt_token_count = response['usage']['prompt_tokens']

    time_dict[current_time] = time_dict.get(current_time, 0) + prompt_token_count

    os.system('cls')
    print(now)
    print(current_time)
    print(time_dict)