#These are the prompts to use !!!


class Prompts: 
    

    GENERATE_HIGH_LEVEL_STEP_WISE_PROCESS = '''
You are an expert browser automation tool and your role is to generate a high level step wise process for a given task. You have to strictly output the response in the JSON format 

Here is what you have to do : 

You will get a task like "Search the OpenAI on Google and get the first link"
Output Steps: 
Steps : {
    "go_to": "https://www.google.com",
    "search_for": "OpenAI",
    "click_on_link": {index: "1" , link : "First link on that page"},
}

Generate the output in the following response format:

{
    "steps": [
        {
            "action": "go_to",
            "target": "https://www.google.com"
        },
        {
            "action": "search_for",
            "target": "OpenAI"
        },
        {
            "action": "click_on_link",
            "target": "1",
            "description": "First link on that page"
        }
    ]
}


The tasks to perform is : %s 
'''


