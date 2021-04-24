FROM cupy/cupy:v9.0.0

WORKDIR  /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en_core_web_trf

COPY . /app/
CMD uvicorn main:app --port 80 --host 0.0.0.0