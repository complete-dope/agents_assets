import re 
import json 


def GetJSONStringFromUnstructuredData(data: str):
    '''
    This data might contain json in the form of  ```json <data> ``` and this function extracts the json from it...
    Returns a json object / python dict  
    '''

    match = re.search(r'```json\n(.*?)\n```', data, re.DOTALL)
    json_str = match.group(1)
    output_json = json.loads(json_str)

    return output_json


