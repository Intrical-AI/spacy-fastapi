from typing import Dict, List, Optional

from pydantic_choices import choice
from pydantic import BaseModel

from spacy_models import nlp_models


class Batch(BaseModel):

    texts: List[str]
    # The options for the language as the models that are loaded
    language: choice(nlp_models.keys())
    split_sentences: Optional[bool] = True


class EntityModel(BaseModel):

    name: str
    start: int
    end: int
    label: str
    syntactic_pos: str
    syntactic_dep: str
    tense: str
    morph: Dict[str, str]


class SentenceModel(BaseModel):

    text: str
    tense: str
    entities: List[EntityModel]


class ResponseModel(BaseModel):

    documents: List[List[SentenceModel]]
