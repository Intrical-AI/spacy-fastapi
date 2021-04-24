import os
import threading

from typing import List
from segtok.segmenter import split_single

from spacy_models import nlp_models
from models import Batch, SentenceModel

model_lock = threading.Lock()


class ModelWrapper(object):

    def __call__(self, batch: Batch) -> List[List[SentenceModel]]:
        """
        Given a batch of texts and the language of them, it passes through 
        spacy language model and return the corresponding serialized version

        Args:
            batch (Batch): The batch of documents

        Returns:
            [type]: [description]
        """

        model = nlp_models[batch.language]

        if batch.split_sentences:
            documents = [
                [sent for sent in split_single(text)]
                for text in batch.texts]
            sentences_flat = [
                item for sublist in documents for item in sublist]
        else:
            sentences_flat = batch.texts

        # Model forward pass
            """
        If the webserver is running in a multithreading settings, we must
        ensure the model is not called in parallel on the same thread so
        we wrap it in Semaphore. In case you are running it using Gunicorn
        with a single thread per worker, it does not require thread lock
        since it runs on separate processes.
        """
        if os.getenv("MULTITHREADING", True):
            with model_lock:
                pos_res = list(model.pipe(sentences_flat))
        else:
            pos_res = list(model.pipe(sentences_flat))

        if batch.split_sentences:
            """
            Inflate the results from the nlp model, as outcome a list of lists
            where each inner list represents a document
            """
            pos_res_inflate = []
            last_id = 0
            for s in documents:
                pos_res_inflate.append(pos_res[last_id:last_id+len(s)])
                last_id += len(s)
        else:
            # Keep all documents list as it is if sentences have not been splitted
            pos_res_inflate = pos_res

        res = []
        for doc in pos_res_inflate:
            doc_ent = []
            for sentence in doc:
                tmp = []
                for entity in sentence.ents:
                    # Reconstruct the sentence tokens of the entity
                    tokens = sentence[entity.start:entity.end]
                    # Get the total length
                    length = sum(map(lambda x: len(x), tokens))
                    # Append the Entity
                    tmp.append({
                        "name": entity.text,
                        "start": tokens[0].idx,
                        "end":  tokens[0].idx+length,
                        "label": entity.label_,
                        "syntactic_pos": tokens[0].pos_,
                        "syntactic_dep": tokens[0].dep_,
                        "tense": entity.root.tag_,
                        "morph": tokens[0].morph.to_dict(),
                    })
                doc_ent.append({
                    "text": sentence.text,
                    "tense": list(sentence.sents)[0].root.tag_,
                    "entities": tmp,
                })
            res.append(doc_ent)
        return res
