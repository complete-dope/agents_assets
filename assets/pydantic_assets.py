
'''
This is useful for the models that dont support Response format as a key word arg so we need to define the json in the prompt along with the requesting / begging the LLM model to follow our request and format the response in the way we want it to be.

So this is a function that converts pydantic model to a string that can be used in the prompt.
'''

from pydantic import BaseModel
from typing import Any, get_origin, get_args, Union, List, Dict, Type, Optional

def describe_type(tp: Any) -> str:
    """
    Recursively generates a human-readable description of the type `tp`.
    """
    origin = get_origin(tp)
    args = get_args(tp)
    
    if origin in (list, List):
        # Handle list types (e.g., list[str] or list[list[int]])
        if args:
            inner_desc = describe_type(args[0])
            return f"a list of {inner_desc}"
        else:
            return "a list"
    elif origin in (dict, Dict):
        # Handle dictionary types (e.g., dict[str, int])
        if len(args) == 2:
            key_desc = describe_type(args[0])
            value_desc = describe_type(args[1])
            return f"a dictionary with keys as {key_desc} and values as {value_desc}"
        else:
            return "a dictionary"
    elif origin is Union:
        # Handle Union types; this also covers Optional (which is Union[X, NoneType])
        non_none_types = [arg for arg in args if arg is not type(None)]
        if len(args) == 2 and len(non_none_types) == 1:
            # It’s an Optional type
            inner_desc = describe_type(non_none_types[0])
            # Remove any leading article from the inner description
            if inner_desc.startswith("a "):
                inner_desc = inner_desc[2:]
            elif inner_desc.startswith("an "):
                inner_desc = inner_desc[3:]
            return f"an optional {inner_desc}"
        else:
            # For a general union, join the descriptions with " or "
            union_parts = [describe_type(arg) for arg in args]
            return " or ".join(union_parts)
    else:
        # For non-generic types, map basic types to a friendly description.
        if tp is str:
            return "a string"
        elif tp is int:
            return "an integer"
        elif tp is float:
            return "a float"
        elif tp is bool:
            return "a boolean"
        # If it's a subclass of BaseModel, you can reference its schema.
        elif isinstance(tp, type) and issubclass(tp, BaseModel):
            return f"an object conforming to the {tp.__name__} schema and {tp.__name__} schema is : <schema_start> {describe_pydantic_model(tp)} <schema_end>"
        elif hasattr(tp, '__name__'):
            return f"a {tp.__name__}"
        else:
            return str(tp)

def describe_pydantic_model(model: Type[BaseModel]) -> str:
    """
    Generates a descriptive string for the provided Pydantic model.
    """
    # Get the field annotations
    hints = model.__annotations__
    description = "The output should contain "
    
    fields = []
    for field, field_type in hints.items():
        type_description = describe_type(field_type)
        fields.append(f'a key named "{field}" that will be {type_description}')
    
    return description + ", ".join(fields) + "." + ".You have to be extremely careful with the upper and lower character case and you need to follow it exactly as it is."
