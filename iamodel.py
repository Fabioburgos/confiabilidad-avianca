#IA model to compare report text mainly for Amos.
# Importing spacy and fuzzy wuzzy
import fuzzywuzzy

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class IAmodel:

    def report_comparation(self, sentence_1, sentence_2):
        ratio = fuzz.ratio(sentence_1.lower(), sentence_2.lower())
        return ratio