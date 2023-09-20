from nltk.corpus import wordnet as wn

class LanguageUtils:
    """
    Utility class for language-related operations.

    Attributes:
        None
    """

    def __init__(self):
        pass

    def get_max_similarity(self, word1, word2):
        """
        Returns the maximum similarity score between two words.

        Args:
            word1 (str): First word.
            word2 (str): Second word.

        Returns:
            float: Maximum similarity score.
        """
        synsets_word1 = wn.synsets(word1)
        synsets_word2 = wn.synsets(word2)
        
        max_sim = 0

        for synset1 in synsets_word1:
            for synset2 in synsets_word2:
                sim = synset1.path_similarity(synset2) or 0
                if sim > max_sim:
                    max_sim = sim
                    
        return max_sim

    def get_most_similar_word(self, word_a, list_e):
        """
        Returns the word in list E that is most similar to word A.

        Args:
            word_a (str): Word to compare.
            list_e (list): List of possible words.

        Returns:
            str: Most similar word.
        """
        # Map each word in list E to its maximum similarity score with word A
        similarity_scores = [(word, self.get_max_similarity(word_a, word)) for word in list_e]

        # Get the word with the maximum similarity score
        max_sim_word, max_sim_score = max(similarity_scores, key=lambda item:item[1])

        return max_sim_word