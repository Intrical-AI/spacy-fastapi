import spacy

spacy.prefer_gpu()

nlp_models = {
    # Add here your models to support all the languages you need
    'en': spacy.load("en_core_web_trf"),
    'nl': spacy.load("nl_core_news_sm"),
}
