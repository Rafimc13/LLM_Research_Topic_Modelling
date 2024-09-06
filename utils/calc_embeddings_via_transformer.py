from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F


def mean_pooling(model_output, attention_mask):
    """
    Mean Pooling - Take attention mask into account for correct averaging
    """
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def calc_embeddings(sentences):
    """
    Calculates embeddings with a transformer model

    Args:
        sentences (np.array): Sentences to be transformed as embeddings.

    Returns:
        embeddings (np.array): calculated embeddings.
    """

    # Load model from HuggingFace Hub
    # tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    # model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')
    model = AutoModel.from_pretrained('sentence-transformers/paraphrase-mpnet-base-v2')

    # Set up the correct device for the transformer
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Available device for the model is: '{device}'")
    model.to(device)
    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    encoded_input.to(device)
    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    transform_data_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    transform_data_embeddings = F.normalize(transform_data_embeddings, p=2, dim=1)

    transform_data_embeddings = transform_data_embeddings.cpu().detach().numpy().tolist()
    print('Calculation of embeddings completed succesfully')
    return transform_data_embeddings
