# Spacy-fastapi

This project provides REST API interface (thanks to [FastAPI](https://fastapi.tiangolo.com/)) to [Spacy](https://spacy.io/) V3 with GPU support reducing the latecy for a fast, complete and customizable NLP self-contained pipeline part.



## Getting Started


### Docker
If you want to run the Docker image, simply run 

```
docker run -p 8000:80 intrical/spacy-fastapi:latest
```
If you want to enable the GPU support and reduce the inferente time, you first need to install CUDA support for the Docker Runtime.
You can follow a nice guide [here](https://towardsdatascience.com/how-to-properly-use-the-gpu-within-a-docker-container-4c699c78c6d1).

### From source

If you want to run the code from your machine not in docker image, first pull the code

```
git clone https://github.com/Intrical-AI/spacy-fastapi.git
cd spacy-fastapi
```

Create now the virtualenvironment
```
virtualenv --python=/usr/bin/python3.8 env
source ./env/bin/activate
```

Now install Pipenv and consequently all the requirements
```
pip install pipenv
pipenv sync
```

Then, download the language models from spacy that you need, in this case I will download the English model, you can follow the instructions [here](https://spacy.io/usage/models) if you need other languages.
```
python -m spacy download en_core_web_trf
```

Now you are set! You can finally run the web server using uvicorn ([FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/first-steps/))
```
uvicorn main:app --port 8000 --reload
```

To test if everything is up and running, use the `/predict` endpoint. You can do that using Postman or more quickly `CURL`
```
curl --location --request POST 'http://localhost:8100/predict' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=dENUPbzrsmkx1cEVH93cLJhNHKj22AUWEjqE8WOOyy5dqvC0RhzgkUtdJzUiRFCS' \
--data-raw '{
    "texts": [
        "Microsoft is a big company."
    ],
    "language": "en"
}'
```

The answer should be like this
```
{
    "documents": [
        [
            {
                "text": "Microsoft is a big company.",
                "tense": "VBZ",
                "entities": [
                    {
                        "name": "Microsoft",
                        "start": 0,
                        "end": 9,
                        "label": "ORG",
                        "syntactic_pos": "PROPN",
                        "syntactic_dep": "nsubj",
                        "tense": "NNP",
                        "morph": {
                            "NounType": "Prop",
                            "Number": "Sing"
                        }
                    }
                ]
            }
        ]
    ]
}
```



## Running the tests

TODO

## Authors

* **Alvise Sembenico** as Intrical AI - *Initial work* - [Alvise Sembenico](https://github.com/AlviseSembenico)

See also the list of [contributors](https://github.com/Intrical-AI/spacy-fastapi/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

