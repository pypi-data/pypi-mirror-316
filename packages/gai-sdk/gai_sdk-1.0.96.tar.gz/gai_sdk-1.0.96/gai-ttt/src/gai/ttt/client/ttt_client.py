from gai.lib.common.generators_utils import chat_string_to_list
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)

import os
from gai.lib.config.config_utils import get_client_config
from gai.lib.config.pydantic.gai_config import ClientLLMConfig
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from gai.ttt.client.completions import Completions
from typing import get_args,Union, Optional
from openai.types.chat_model import ChatModel
from pydantic import BaseModel

class TTTClient:

    # config is either a string path or a component config
    def __init__(self, config_or_path:Optional[Union[str|dict]]=None):
        self.url=None
        
        # Load from default config file
        self.config:ClientLLMConfig = get_client_config("ttt")
        
        if isinstance(config_or_path, dict):
            # If config is provided, update config            
            for key, value in config_or_path.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)            
        elif isinstance(config_or_path, str):
            # If path is provided, load config from path
            self.config:ClientLLMConfig = get_client_config("ttt",config_or_path)
        elif isinstance(config_or_path, ClientLLMConfig):
            self.config:ClientLLMConfig= config_or_path
        else:
            raise ValueError("Invalid config or path provided")
                    
        self.url = self.config.url
        
        # Handle API Key
        if self.config.engine=="openai":
            if self.config.model in get_args(ChatModel):
                from dotenv import load_dotenv
                load_dotenv()
                import os
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    api_key = self.config.env.get("OPENAI_API_KEY", "")
                if api_key is None:
                    raise ValueError("OPENAI_API_KEY not found in config")
                client = OpenAI(api_key=api_key)
            else:
                raise ValueError(f"Invalid openai model {self.config.model}")
        else:
            client = OpenAI(api_key="")
    
        self.client = Completions.PatchOpenAI(client, override_url=self.url)

    def __call__(self, 
                 messages:str|list, 
                 stream:bool=True, 
                 max_tokens:int=None, 
                 temperature:float=None, 
                 top_p:float=None, 
                 top_k:float=None,
                 json_schema:dict=None,
                 tools:list=None,
                 tool_choice:str=None,
                 stop:list=None,
                 timeout:float=None,
                 response_format:dict=None
                 ):

        if isinstance(messages, str):
            messages = chat_string_to_list(messages)
            
        response=None
        if self.config.engine=="openai":
            if isinstance(response_format, type) and issubclass(response_format, BaseModel):

                # response_format is supported under client.beta.chat.completions.parse
                response = self.client.beta.chat.completions.parse(model=self.config.model,
                            messages=messages,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            top_p=top_p,
                            stop=stop,
                            timeout=timeout,
                            response_format=response_format
                            )
            else:
                # Non response_format call                
                response = self.client.chat.completions.create(model=self.config.model,
                            messages=messages,
                            stream=stream,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            top_p=top_p,
                            tools=tools,
                            tool_choice=tool_choice,
                            stop=stop,
                            timeout=timeout,
                            response_format=response_format
                            )
        else:
            if isinstance(response_format, type) and issubclass(response_format, BaseModel):
                # convert response format to json_schema
                json_schema=response_format.schema()
            
            response = self.client.chat.completions.create(model=self.config.model,
                        messages=messages,
                        stream=stream,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        top_k=top_k,
                        json_schema=json_schema,
                        tools=tools,
                        tool_choice=tool_choice,
                        stop=stop,
                        timeout=timeout,
                        response_format=response_format
                        )
        if stream:
            def streamer():
                for chunk in response:
                    yield chunk
            return streamer()
        return response

