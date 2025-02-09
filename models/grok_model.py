# Use the OpenAI Model 
from openai import OpenAI , AsyncOpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")

def GenericModel(**kwargs): 
    ''' This is a gemini model and I am keeping the naming same so that it becomes easy'''

    GROQ_API_KEY =  config.get("GROQ_API_KEY", None)
    if GROQ_API_KEY is None: 
        raise ValueError("GROQ_API_KEY is not set. Please set it in the .env file")

    system_prompt = kwargs.get('system_prompt', None) 
    user_prompt = kwargs.get('user_prompt' , None)
    assistant_prompt = kwargs.get("assistant_prompt" , None)
    model_name = kwargs.get("model_name", "gpt-4o")
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
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )

    completion = client.beta.chat.completions.parse(**model_args)

    try: 
        return completion.choices[0].message.content
    except Exception as e:
        print(e)
        return "None"






async def AsyncGenericModel(**kwargs): 
    ''' This is a gemini model and I am keeping the naming same so that it becomes easy'''

    GROQ_API_KEY =  config.get("GROQ_API_KEY", None)
    if GROQ_API_KEY is None: 
        raise ValueError("GROQ_API_KEY is not set. Please set it in the .env file")

    system_prompt = kwargs.get('system_prompt', None) 
    user_prompt = kwargs.get('user_prompt' , None)
    assistant_prompt = kwargs.get("assistant_prompt" , None)
    model_name = kwargs.get("model_name", "llama-3.3-70b")
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

    
    client = AsyncOpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )

    completion = await client.beta.chat.completions.parse(**model_args)

    try: 
        return completion.choices[0].message.content
    except Exception as e:
        print(e)
        return "None"

