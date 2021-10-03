import logging

import tokenizations
from tqdm import tqdm

import Constants as Const
import DataLoader
import ModelLoader

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


def textToBertEmbedding(text: str, bert_tokenizer, bert_model, spacy_model):
    text = str(text)
    bert_tokens = bert_tokenizer.tokenize(text)
    doc = spacy_model(text)
    spacy_tokens = [token.text for token in doc]
    s2b, _ = tokenizations.get_alignments(spacy_tokens, bert_tokens)

    index_noun_tokens = []

    for ent, token_mapping in zip(doc, s2b):
        if ent.pos_ == 'NOUN':
            index_noun_tokens += token_mapping

    inputs = bert_tokenizer(text, return_tensors="pt", padding=True)
    outputs = bert_model(**inputs)
    last_hidden_states = outputs[0]
    vectors = last_hidden_states[0]
    vectors_without_special_tokens = vectors[1:-1]

    if index_noun_tokens:
        vectors = vectors_without_special_tokens[index_noun_tokens]
    else:
        vectors = vectors_without_special_tokens

    return vectors.mean(axis=0)


def embed(file, texts, ids, tokenizer, model, spacy_model, limit):
    number_texts = len(texts)
    embeddings = DataLoader.load_embeddings(file)

    if limit:
        texts = texts[:limit]
        ids = ids[:limit]

    new_embeddings = 0

    for ids, texts in tqdm(zip(ids, texts), total=number_texts):
        if ids not in embeddings:
            issue_embedding = textToBertEmbedding(
                texts, tokenizer, model, spacy_model)
            embeddings[ids] = issue_embedding
            new_embeddings += 1

    if new_embeddings > 0:
        DataLoader.save_embeddings(file, embeddings)
    else:
        logger.info(f'no new embedding for {file}')


def embed_firefox_android_issues(file, tokenizer, model, spacy_model, limit):
    logger.info('Embedding firefox android issues...')
    firefox_android = DataLoader.load_df_compressed(
        Const.FIREFOX_ISSUES_ANDROID)
    issue_descriptions = firefox_android['summary'].to_list()
    issue_ids = firefox_android['id'].to_list()

    embed(file, issue_descriptions, issue_ids,
          tokenizer, model, spacy_model, limit)


def embed_firefox_issues(file, tokenizer, model, spacy_model, limit):
    logger.info('Embedding firefox issues...')
    firefox = DataLoader.load_df_compressed(Const.FIREFOX_ISSUES_DESKTOP)
    issue_descriptions = firefox['summary'].to_list()
    issue_ids = firefox['id'].to_list()

    embed(file, issue_descriptions, issue_ids,
          tokenizer, model, spacy_model, limit)


def embed_vlc_issues(file, tokenizer, model, spacy_model, limit):
    logger.info('Embedding vlc issues...')
    vlc = DataLoader.load_df_compressed(Const.VLC_ISSUES)
    issue_descriptions = vlc['summary'].to_list()
    issue_ids = vlc['id'].to_list()

    embed(file, issue_descriptions, issue_ids,
          tokenizer, model, spacy_model, limit)


def embed_signal_issues(file, tokenizer, model, spacy_model, limit):
    logger.info('Embedding signal issues...')
    signal = DataLoader.load_df_compressed(Const.SIGNAL_ISSUES)
    issue_descriptions = signal['title'].to_list()
    issue_ids = signal['id'].to_list()

    embed(file, issue_descriptions, issue_ids,
          tokenizer, model, spacy_model, limit)

def embed_nextcloud_issues(file, tokenizer, model, spacy_model, limit):
    logger.info('Embedding nextcloud issues...')
    nextcloud = DataLoader.load_df_compressed(Const.NEXTCLOUD_ISSUES)
    issue_descriptions = nextcloud['title'].to_list()
    issue_ids = nextcloud['id'].to_list()

    embed(file, issue_descriptions, issue_ids,
          tokenizer, model, spacy_model, limit)


if __name__ == "__main__":

    tokenizer = ModelLoader.get_distil_bert_tokenizer()
    model = ModelLoader.get_distil_bert_model()
    spacy_model = ModelLoader.get_spacy_model()

    # embed_firefox_android_issues(Const.FIREFOX_ANDROID_EMBEDDINGS,
    #                              tokenizer, model, spacy_model, None)

    # embed_firefox_issues(Const.FIREFOX_EMBEDDINGS,
    #                      tokenizer, model, spacy_model,
    #                      None)

    # embed_vlc_issues(Const.VLC_EMBEDDINGS,
    #                  tokenizer, model, spacy_model,
    #                  22_000)

    # embed_signal_issues(Const.SIGNAL_EMBEDDINGS,
    #                  tokenizer, model, spacy_model,
    #                  10_000)

    embed_nextcloud_issues(Const.NEXTCLOUD_EMBEDDINGS,
                     tokenizer, model, spacy_model,
                     10_000)
