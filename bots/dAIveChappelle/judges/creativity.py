from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

MODEL: str = 'sentence-transformers/all-MiniLM-L6-v2'


class CreativityJudge:
    '''
    This class is used to judge the Creativity score of a joke
    '''

    def __init__(self):
        # get a list of jokes that were already generated
        # # read the /utils/history.txt file and get the jokes history (each line is a joke)
        with open('bots/dAIveChappelle/utils/history.txt', 'r') as f:
            self.jokes_history = f.readlines()
        # get a semantic similarity model
        # # Load model from HuggingFace Hub
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL)
        self.similarity_model = AutoModel.from_pretrained(
            MODEL)

    def score(self, joke):
        '''
        Returns the Creativity score of the joke
        '''
        # get the semantic similarity score between the joke and the jokes history, if one of them is similar to the joke then the comedian is not creative
        for old_joke in self.jokes_history:
            # get the semantic similarity score between the joke and the joke history
            similarity = self._get_semantic_similarity(joke, old_joke)
            if similarity > 0.9:
                print(old_joke)
                score = 0
                return score
        # add the joke to the jokes history
        with open('bots/dAIveChappelle/utils/history.txt', 'a') as f:
            # replace the newlines with spaces
            joke = joke.replace('\n', ' ')
            # remove starting and trailing whitespace
            joke = joke.strip()
            # write the joke in a new line
            f.write(f'{joke}\n')
        # if the joke is not similar to any of the jokes in the jokes history then return 10
        score = 10
        return score

    def _get_semantic_similarity(self, sentence_1, sentence_2):
        # Sentences we want sentence embeddings for
        sentences = [sentence_1, sentence_2]

        # Load model from HuggingFace Hub
        tokenizer = AutoTokenizer.from_pretrained(
            'sentence-transformers/all-MiniLM-L6-v2')
        model = AutoModel.from_pretrained(
            'sentence-transformers/all-MiniLM-L6-v2')

        # Tokenize sentences
        encoded_input = tokenizer(
            sentences, padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = model(**encoded_input)

        # Perform pooling
        sentence_embeddings = self._mean_pooling(
            model_output, encoded_input['attention_mask'])

        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

        # Compute cosine similarity between the two
        cos_sim = F.cosine_similarity(
            sentence_embeddings[0], sentence_embeddings[1], dim=0)

        return cos_sim

    def _mean_pooling(self, model_output, attention_mask):
        '''
        Class function used to compute mean pooling - Take attention mask into account for correct averaging
        '''
        # First element of model_output contains all token embeddings
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(
            -1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
