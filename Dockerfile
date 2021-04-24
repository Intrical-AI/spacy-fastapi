FROM cupy/cupy:v9.0.0 as base


RUN pip install --upgrade pip
RUN pip install --no-cache-dir "uvicorn[standard]" gunicorn
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

RUN python3 -m spacy download en_core_web_trf


WORKDIR  /app
COPY . /app/

ENV PYTHONPATH=/app


EXPOSE 80

ENV WEB_CONCURRENCY 1
ENV WORKERS_PER_CORE 8

CMD gunicorn --preload -k uvicorn.workers.UvicornWorker -c /app/gunicorn_conf.py main:app

