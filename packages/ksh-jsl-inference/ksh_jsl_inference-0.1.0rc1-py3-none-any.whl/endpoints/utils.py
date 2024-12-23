from typing import List, Union

from enum import Enum


class Recipe(str, Enum):
    HEALTHCARE_NLP = "healthcare_nlp"
    VISUAL_NLP = "visual_nlp"
    LLM = "llm"


class Platform(str, Enum):
    SAGEMAKER = "sagemaker"
    SNOWFLAKE = "snowflake"


def append_string_or_list_of_string(text: Union[str, List], texts: List) -> List[str]:
    if isinstance(text, str):
        texts.append(text)
    elif isinstance(text, list):
        texts.extend(text)
    return texts


def get_attr_or_key(item, key):
    """Fetches an attribute or dictionary key from an item."""
    return getattr(item, key, None) if hasattr(item, key) else item.get(key, None)
