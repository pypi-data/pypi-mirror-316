import re
import time
from typing import Any, overload
import requests
import logging

# Base exception for all GroqAgent exceptions
class GroqAgentException(Exception):
    pass

# Throw this error when the rate limit is exceeded
class GroqAgentRateLimitExceededError(GroqAgentException):
    pass

#Throw this error when the context length is exceeded
class GroqAgentContectLengthError(GroqAgentException):
    pass

class GroqAgent():
    '''
    Create a GroqAgent object to interact with the Groq API.
    Automatically handles chat for the agent.
    '''
    def __init__(self,
        *,
        api_key: str | list[str],
        model: str | None = None,
        frequency_penalty: float | None = None,
        function_call: str | dict | None = None,
        functions: list | None = None,
        logit_bias: dict | None = None,
        logprobs: bool | None = None,
        max_tokens: int | None = None,
        n: int | None = None,
        parallel_tool_calls: bool | None = None,
        presence_penalty: float | None = None,
        response_format: dict | None = None,
        seed: int | None = None,
        stop: str | list | None = None,
        stream: bool | None = None,
        stream_options: dict | None = None,
        temperature: float | None = None,
        tool_choice: str | dict | None = None,
        tools: list | None = None,
        top_logprobs: int | None = None,
        top_p: float | None = None,
        user: str | None = None,
        # Custom parameters
        max_attempts: int = 3,
        max_wait_time_s: int = -1,
        # Development parameters
        DEBUG: bool = False,
    ):
        '''
        Initialize the GroqAgent object with the settings.
        
        Args:
            Groq: API Parameters detailed in the OpenAI API documentation. https://console.groq.com/docs/api-reference#chat
            max_attempts (int): The maximum number of attempts to make the request.-1 for infinite attempts. 
        '''
        self.Set_Agent_Settings(api_key=api_key, model=model, frequency_penalty=frequency_penalty, function_call=function_call,
            functions=functions, logit_bias=logit_bias, logprobs=logprobs, max_tokens=max_tokens, n=n,
            parallel_tool_calls=parallel_tool_calls, presence_penalty=presence_penalty, response_format=response_format,
            seed=seed, stop=stop, stream=stream, stream_options=stream_options, temperature=temperature,
            tool_choice=tool_choice, tools=tools, top_logprobs=top_logprobs, top_p=top_p, user=user,
            
            # Custom parameters
            max_attempts=max_attempts, max_wait_time_s=max_wait_time_s)
        self.chat_history: list = []
        self.DEBUG = DEBUG

    def Set_Agent_Settings(self,
        *,
        api_key: str | list[str] | None = None,
        model: str | None = None,
        frequency_penalty: float | None = None,
        function_call: str | dict | None = None,
        functions: list | None = None,
        logit_bias: dict | None = None,
        logprobs: bool | None = None,
        max_tokens: int | None = None,
        n: int | None = None,
        parallel_tool_calls: bool | None = None,
        presence_penalty: float | None = None,
        response_format: dict | None = None,
        seed: int | None = None,
        stop: str | list | None = None,
        stream: bool | None = None,
        stream_options: dict | None = None,
        temperature: float | None = None,
        tool_choice: str | dict | None = None,
        tools: list | None = None,
        top_logprobs: int | None = None,
        top_p: float | None = None,
        user: str | None = None,
        # Custom parameters
        max_attempts: int | None = None,
        max_wait_time_s: int | None = None,
    ):
        '''
        Set the agent settings for the Groq API.
        
        Args:
            Groq: API Parameters detailed in the OpenAI API documentation. https://console.groq.com/docs/api-reference#chat
            max_attempts (int): The maximum number of attempts to make the request. -1 for infinite attempts. 
        '''
        if api_key is not None:
            self.api_key = api_key or getattr(self, 'api_key', None)
            if isinstance(self.api_key, list):
                # list to dict
                api_dict = {}
                for key in self.api_key:
                    api_dict[key] = 0
                self.api_key = api_dict
            elif isinstance(self.api_key, str):
                self.api_key = {self.api_key: 0}
            else:
                self.api_key = None

        self.model = model or getattr(self, 'model', None)
        self.frequency_penalty = frequency_penalty or getattr(self, 'frequency_penalty', None)
        self.function_call = function_call or getattr(self, 'function_call', None)
        self.functions = functions or getattr(self, 'functions', None)
        self.logit_bias = logit_bias or getattr(self, 'logit_bias', None)
        self.logprobs = logprobs or getattr(self, 'logprobs', None)
        self.max_tokens = max_tokens or getattr(self, 'max_tokens', None)
        self.n = n or getattr(self, 'n', None)
        self.parallel_tool_calls = parallel_tool_calls or getattr(self, 'parallel_tool_calls', None)
        self.presence_penalty = presence_penalty or getattr(self, 'presence_penalty', None)
        self.response_format = response_format or getattr(self, 'response_format', None)
        self.seed = seed or getattr(self, 'seed', None)
        self.stop = stop or getattr(self, 'stop', None)
        self.stream = stream or getattr(self, 'stream', None)
        self.stream_options = stream_options or getattr(self, 'stream_options', None)
        self.temperature = temperature or getattr(self, 'temperature', None)
        self.tool_choice = tool_choice or getattr(self, 'tool_choice', None)
        self.tools = tools or getattr(self, 'tools', None)
        self.top_logprobs = top_logprobs or getattr(self, 'top_logprobs', None)
        self.top_p = top_p or getattr(self, 'top_p', None)
        self.user = user or getattr(self, 'user', None)

        # Custom parameters
        self.max_attempts = max_attempts or getattr(self, 'max_attempts', None)
        self.max_wait_time_s = max_wait_time_s or getattr(self, 'max_wait_time', None)

    def SystemPrompt(self, prompt: str):
        '''
        Use this method to add a system prompt to the chat history altering how the agent responds.
        example: 'Respond as a personal assistant.' or 'Respond as a customer service agent.'
        '''
        self.chat_history.append({
            "role": "system",
            "content": prompt
        })

    def Chat(self, message: str, *, remember: bool = True, verbose: bool = False) -> str | dict:
        '''
        Chat with the agent. The agent will respond to the message.

        Args:
            message (str): The message to send to the agent.
            remember (bool): Whether to remember the chat history. Default is True.
            verbose (bool): Whether to return the full response. Default is False.

        Returns:
            str | dict: The response message from the agent.
                str: If verbose is False, only the response message is returned.
                dict: If verbose is True, the full response is returned.
        '''
        response = self._post(messages=[*self.chat_history, {"role": "user", "content": message}])
        response_message = response['choices'][0]['message']
        if remember:
            self.chat_history.append({"role": "user", "content": message})
            self.chat_history.append(response_message)
        
        if verbose:
            return response
        return response_message['content']

    def _post(self, *, messages: list = None) -> dict:
        '''
        POST request to the Groq API.
        '''
        # get dict key with the lowest value
        self.api_key = dict(sorted(self.api_key.items(), key=lambda item: item[1]))
        print(self.api_key)
        # get the first key
        bearer_api_key = list(self.api_key.keys())[0]

        # Reduce all value be lowers value if not zero
        _v_ = self.api_key[bearer_api_key]
        if _v_ > 0:
            for key in self.api_key.keys():
                self.api_key[key] -= _v_

        URL = 'https://api.groq.com/openai/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {bearer_api_key}',
            'Content-Type': 'application/json',
        }

        if self.function_call:
            logging.warning('\'function_call\' is Deprecated')
        if self.functions:
            logging.warning('\'functions\' is Deprecated')
        if self.logit_bias:
            logging.warning('\'logit_bias\' is not yet supported')
        if self.logprobs:
            logging.warning('\'logprobs\' is not yet supported')
        if self.n:
            logging.warning('\'n\' only supports n=1')
        if self.tool_choice:
            logging.warning('\'tool_choice\' disabled')
        if self.tools:
            logging.warning('\'tools\' disabled')
        if self.top_logprobs:
            logging.warning('\'top_logprobs\' is not yet supported')

        body = {
            'messages': messages,
            'model': self.model,
            'frequency_penalty': self.frequency_penalty,
            # 'function_call': self.function_call, # Deprecated on API
            # 'functions': self.functions, # Deprecated on API
            # 'logit_bias': self.logit_bias, # not yet supported on API
            # 'logprobs': self.logprobs, # not yet supported on API
            'max_tokens': self.max_tokens,
            # 'n': self.n, # only support n=1 on API
            'parallel_tool_calls': self.parallel_tool_calls,
            'presence_penalty': self.presence_penalty,
            'response_format': self.response_format,
            'seed': self.seed,
            'stop': self.stop,
            'stream': self.stream,
            'stream_options': self.stream_options,
            'temperature': self.temperature,
            # 'tool_choice': self.tool_choice, # not working
            # 'tools': self.tools, # not working
            # 'top_logprobs': self.top_logprobs,# not yet supported on API
            'top_p': self.top_p,
            'user': self.user,
        }

        # NOTE: This 'while' loop should not be broken using 'break' keyword.
        # NOTE: Must 'return' or 'raise' to exit the loop and a 'continue' keyword must be used for looping.
        attempt = 0
        # NOTE: If max_attempts is -1, it will loop infinitely.
        do_attempt_loop = attempt < self.max_attempts
        while self.max_attempts == -1 or do_attempt_loop:
            attempt += 1
            do_attempt_loop = attempt < self.max_attempts

            response = requests.post(URL, headers=headers, json=body)

            # Handle HTTP errors separately
            try:
                response.raise_for_status()
            
            # HTTP error handling
            except requests.exceptions.HTTPError as e:
                content: dict

                content = response.json()
                logging.warning(f'HTTP Error: {content}')
                content_error = content.get('error', None)
                error_message = content_error.get('message', None)
                error_type = content_error.get('type', None)
                error_code = content_error.get('code', None)

                logging.warning(f'Attempt {attempt} - {content_error}')

                # Rate limit exceeded error
                if error_code == 'rate_limit_exceeded':
                    groq_api_rate_limit_exceeded_error_handle(error_message, error_type, error_code, self=self)
                elif error_code == 'context_length_exceeded':
                    raise GroqAgentContectLengthError(f'Context length exceeded.\n{error_message}')
                else:
                    if not do_attempt_loop: raise GroqAgentException(f'HTTP Error: {content_error}')
                continue
                
            # Other exceptions
            except Exception as e:
                logging.error(str(e), exc_info=True)
                if not do_attempt_loop: raise e
                continue
            
            # Rate limit info
            rate_limit_info = {
                'max_requests': response.headers.get('x-ratelimit-limit-requests'),
                'max_tokens': response.headers.get('x-ratelimit-limit-tokens'),
                'remaining_requests': response.headers.get('x-ratelimit-remaining-requests'),
                'remaining_tokens': response.headers.get('x-ratelimit-remaining-tokens'),
                'reset_requests': response.headers.get('x-ratelimit-reset-requests'),
                'reset_tokens': response.headers.get('x-ratelimit-reset-tokens'),
            }

            return_response = response.json()
            return_response['rate_limit'] = rate_limit_info
            prompt_token_count = return_response['usage']['prompt_tokens']
            self.api_key[bearer_api_key] += prompt_token_count
            return return_response
        
            # NOTE: NEVER REMOVE THIS ERROR CHECK EVEN IF THE CODE IS UNREACHABLE
            raise GroqAgentException('Loop auto looped. \'continue\' must be used to loop.')
        
        if attempt == self.max_attempts: # If the loop reaches the max attempts
            raise GroqAgentException('Max attempts reached. Unable to get valid response from API.')
        raise GroqAgentException('Loop exited. \'return\' or \'raise\' must be used to exit the loop.')

def groq_api_rate_limit_exceeded_error_handle(error_message: str, error_type: str, error_code: str, *, self: GroqAgent):
    pass
    # Check for rate limit exceeded error
    t_regex = r'Limit (?P<limit>\d*).*?Used (?P<used>\d*).*?Requested (?P<requested>\d*).*?Please try again in ((?P<ms>\d*\.?\d*?)ms)?((?P<m>\d*)m)?((?P<s>\d*\.?\d*?)s)?'
    match = re.search(t_regex, error_message)

    if not match:
        logging.error(f'Rate limit exceeded error message not found:\n{error_message}')
        raise GroqAgentRateLimitExceededError(f'Maximum token limit exceeded.\n{error_message}')
    
    # rate limit info
    limit = match.group('limit')
    # used = match.group('used')
    requested = match.group('requested')
    limit_wait_m = match.group('m') or 0 # minutes
    limit_wait_m_in_s = int(limit_wait_m) * 60 # minutes in seconds
    limit_wait_s = float(match.group('s') or 0) # seconds
    limit_wait_ms = match.group('ms') or 0 # milliseconds
    limit_wait_ms_in_s = float(limit_wait_ms) / 1000 # milliseconds in seconds
    waiting_time_seconds = limit_wait_m_in_s + limit_wait_s + limit_wait_ms_in_s

    if self.max_wait_time_s != -1 and waiting_time_seconds > self.max_wait_time_s:
        raise GroqAgentException(f'Maximum wait time exceeded.\n{error_message}')

    if int(requested) > int(limit):
        print(f'=== {requested} > {limit} ===')
        raise GroqAgentRateLimitExceededError(f'Maximum token limit exceeded.\n{error_message}')

    print(f'Wait time: {waiting_time_seconds} seconds')
    if self.DEBUG:
        __timer__ = 0
        while __timer__ <= waiting_time_seconds:
            print(f' Waiting for {__timer__} seconds...   ', end='\r')
            time.sleep(1)
            __timer__ += 1
        return
    else:
        time.sleep(waiting_time_seconds)
        return