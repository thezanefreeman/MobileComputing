from torch.nn.functional import cosine_similarity
import ModelLoader
import Constants as Const
import DataLoader
from EmbeddingCalculation import textToBertEmbedding

TOKENIZER = ModelLoader.get_distil_bert_tokenizer()
BERT_MODEL = ModelLoader.get_distil_bert_model()
SPACY_MDOEL = ModelLoader.get_spacy_model()


def calculate_distance(v1, v2):
    return cosine_similarity(v1, v2, dim=0)

def get_nearest_issues(text, embeddings, n=10):
    text_embedding = textToBertEmbedding(
        text, TOKENIZER, BERT_MODEL, SPACY_MDOEL)
    
    distances = []

    for issue_id, issue_embedding in embeddings.items():
        distance = calculate_distance(text_embedding, issue_embedding)
        distances.append((issue_id, distance))

    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    return distances[:n]


if __name__ == "__main__":
    embeddings = DataLoader.load_embeddings(
        Const.SIGNAL_EMBEDDINGS)
    issues = DataLoader.load_df_compressed(Const.SIGNAL_ISSUES)

    app_review_text = 'cannot send image messages'

    distances = get_nearest_issues(app_review_text, embeddings)


    print(f'App review: {app_review_text}')
    print()

    
    for issue_id, distance in distances[:10]:
        issue_summary = issues.loc[issues['id'] == issue_id]['title'].values[0]
        print(f"{distance:>.2f}: {issue_summary}")
