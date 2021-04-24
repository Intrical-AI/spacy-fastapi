import spacy

from typing import Dict, List, Optional

from pydantic_choices import choice
from pydantic import BaseModel, Field

from spacy_models import nlp_models


"""
"""
nlp = spacy.load("en_core_web_trf")
pos_labels = '\n'.join([
    f"{label}--{spacy.explain(label)}" for label in nlp.get_pipe("tagger").labels])
dp_labels = '\n'.join([
    f"{label}--{spacy.explain(label)}" for label in nlp.get_pipe("parser").labels])


class Batch(BaseModel):

    texts: List[str]
    # The options for the language as the models that are loaded
    language: choice(nlp_models.keys())
    split_sentences: Optional[bool] = True


class EntityModel(BaseModel):

    name: str
    start: int
    end: int
    label: str = Field(
        title='Label of the entity',
        description=f'Available tags: {pos_labels}'
    )
    syntactic_pos: str = Field(
        title='Syntactic pos of the entity',
        description="Tag from this list https://universaldependencies.org/docs/u/pos/"
    )
    # Tag from this list https://universaldependencies.org/u/dep/
    syntactic_dep: str
    # This can be used to asses if the verb is present of past tense
    tense: str
    # https://spacy.io/usage/linguistic-features#morphology
    morph: Dict[str, str]


class SentenceModel(BaseModel):

    text: str
    tense: str
    entities: List[EntityModel]


class ResponseModel(BaseModel):

    documents: List[List[SentenceModel]]
