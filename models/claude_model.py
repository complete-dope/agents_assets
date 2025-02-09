# Not tested for claude

from openai import OpenAI   
from dotenv import dotenv_values

config = dotenv_values(".env")

def GenericModel(**kwargs): 
    ''' This is a gemini model and I am keeping the naming same so that it becomes easy'''

    CLAUDE_API_KEY =  config.get("CLAUDE_API_KEY", None)
    if CLAUDE_API_KEY is None: 
        raise ValueError("CLAUDE_API_KEY is not set. Please set it in the .env file")

    system_prompt = kwargs.get('system_prompt', None) 
    user_prompt = kwargs.get('user_prompt' , None)
    assistant_prompt = kwargs.get("assistant_prompt" , None)
    model_name = kwargs.get("model_name", "claude-3.5-sonnet")
    response_format = kwargs.get("response_format", None)

    if system_prompt is None or user_prompt is None:
        raise ValueError("system_prompt and user_prompt are required")

    history = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    if assistant_prompt is not None:
        history.append({
            "role": "assistant",
            "content": assistant_prompt
        })
    
    model_args = { 
        "model": model_name,
        "temperature": 0,
        "max_tokens": 1000,
        "top_p": 0.95,
        "messages": history
    }

    if response_format is not None:
        model_args["response_format"] = response_format 

    
    client = OpenAI(
        api_key=CLAUDE_API_KEY, 
        base_url="https://api.anthropic.com/v1/messages"
    )

    completion = client.beta.chat.completions.parse(**model_args)

    try: 
        return completion.choices[0].message.content
    except Exception as e:
        print(e)
        return "None"





