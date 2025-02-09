# This is the main agent !! 

import asyncio 
import openai 
import os, json, time 
from typing import List, Optional
from models.gemini_model import GenericModel
from assets.prompts import Prompts
from assets.response_format import HighLevelStepsOutput
from assets.utils import getJsonFromStr




# Create a Step set 
steps = GenericModel(
    system_prompt=Prompts.GENERATE_HIGH_LEVEL_STEP_WISE_PROCESS , 
    user_prompt="Search the OpenAI on Google and get the first link" , 
    response_format=HighLevelStepsOutput
    )

# Get the List of Steps in the string need to parse in json 
steps = getJsonFromStr(steps) # COnvert 

