# Using the cerebras model 

from cerebras.cloud.sdk import Cerebras, AsyncCerebras
from utils.func_utils import GetJSONStringFromUnstructuredData
from assets.pydantic_assets import describe_pydantic_model
from dotenv import dotenv_values

config = dotenv_values(".env")


def  GenericModel(*args , **kwargs): 
    '''This is the generic model that is used to call the cerebras model'''

    CEBERAS_API_KEY = config.get("CEBERAS_API_KEY")

    system_prompt = kwargs.get("system_prompt")
    user_prompt = kwargs.get("user_prompt")
    assistant_prompt = kwargs.get('assistant_prompt', None)
    model_name = 'llama-3.3-70b'
    response_format = kwargs.get('response_format', None)

    if system_prompt is None or user_prompt is None:
        raise ValueError("system_prompt and user_prompt are required")


    client = Cerebras(
        api_key=CEBERAS_API_KEY,  # This is the default and can be omitted
    )

    history = [
        {"role": "system", "content": system_prompt},
    ]

    if response_format: 
        response_format_string = describe_pydantic_model(response_format)
        history.append({"role": "user", "content": f"{user_prompt}. \nThe response format should be {response_format_string} \n\nOutput as JSON."})
        history.append({"role": "assistant", "content": "Based on the response format provided and the system prompt, this is the structured response."})

    else: 
        history.append({"role": "user", "content": user_prompt})

    model_args = {
        "model": model_name,
        "messages": history,
        "temperature": 0, #fixed 
        "top_p": 0.95
    }

    if response_format:
        model_args["response_format"] = {"type": "json_object"} # This is to tell cerebras that output the response in a json format ..  

    chat_completion = client.chat.completions.create(**model_args)

    output = chat_completion.choices[0].message.content
    try: 
        if response_format: 
            output = GetJSONStringFromUnstructuredData(output)
            return str(output) # if got a dict convert that to a string 
    except: 
        return output
    


async def AsyncGenericModel(*args , **kwargs): 
    '''This is the generic model that is used to call the cerebras model'''

    CEBERAS_API_KEY = config.get("CEBERAS_API_KEY")

    system_prompt = kwargs.get("system_prompt")
    user_prompt = kwargs.get("user_prompt")
    assistant_prompt = kwargs.get('assistant_prompt', None)
    model_name = 'llama-3.3-70b'
    response_format = kwargs.get('response_format', 'json')

    if response_format: 
        response_format = ""

    client = AsyncCerebras(
        api_key=CEBERAS_API_KEY,  # This is the default and can be omitted
    )


    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt + "\n\nOutput as JSON."},
        {"role": "assistant", "content" : "Here is the required answer in JSON format : "}    
    ]
    if assistant_prompt:
        history.append({"role": "assistant", "content": assistant_prompt})

    model_args = {
        "model": model_name,
        "messages": history,
        "temperature": 0,
        "top_p": 0.95
    }

    if response_format:
        model_args["response_format"] = {"type": "json_object"} 


    chat_completion = client.chat.completions.create(**model_args)

    return chat_completion.choices[0].message.content


