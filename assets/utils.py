# These are the utils function 

import ast 

def getJsonFromStr(data):
     
    try: 
        output = ast.literal_eval(data) 
        return output
    except Exception as e:
        print(e)
        return None


