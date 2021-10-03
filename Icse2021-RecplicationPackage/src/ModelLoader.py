import spacy
from transformers import DistilBertModel, DistilBertTokenizer


def get_spacy_model():
    return spacy.load("en_core_web_sm")


def get_distil_bert_tokenizer():
    return DistilBertTokenizer.from_pretrained('distilbert-base-uncased')


def get_distil_bert_model():
    return DistilBertModel.from_pretrained('distilbert-base-uncased')
