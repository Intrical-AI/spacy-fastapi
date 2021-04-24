
from fastapi import FastAPI

from model_wrapper import ModelWrapper
from models import Batch, ResponseModel


app = FastAPI()


@app.post("/predict", response_model=ResponseModel)
def predict(batch: Batch):
    # Remove empty texts
    batch.texts = list(filter(lambda x: len(x) > 0, batch.texts))
    model = ModelWrapper()
    res = model(batch)

    return {"documents": res}
