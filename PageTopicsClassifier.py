from utils.Context import context
import logging
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

logging.basicConfig(level=context.log_level, filename='PageTopicsClassifier')


class PageTopicsClassifier:
    def __init__(self, page_url: str, page_html: str, page_topics: list, page_text: str):
        self.page_url = page_url
        self.page_html = page_html
        self.page_text = page_text
        self.page_topics = page_topics
        self.all_tags = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "VB", "VBZ",
                                "VBP", "VBD", "VBN", "VBG", "IN", "PRP", "PRP$", "UH", "CC", "DT", "WDT",
                                "WP", "WP$", "WRB"]
        self.tage_map = {
            "JJ": "adjective",
            "JJR": "adjective",
            "JJS": "adjective",
            "NN": "noun",
            "NNS": "noun",
            "NNP": "topic",
            "NNPS": "topic",
            "RB": "adverb",
            "RBR": "adverb",
            "RBS": "adverb",
            "VB": "verb",
            "VBZ": "verb",
            "VBP": "verb",
            "VBD": "verb",
            "VBN": "verb",
            "VBG": "verb",
            "IN": "preposition",
            "PRP": "pronoun",
            "PRP$": "pronoun",
            "UH": "interjection",
            "CC": "conjunction",
            "DT": "determiner",
            "WDT": "determiner",
            "WP": "pronoun",
            "WP$": "pronoun",
            "WRB": "adverb",
        }

    async def classify_topics(self):
        for each_topic in self.page_topics:
            tokens = nltk.word_tokenize(each_topic)
            tagged = nltk.pos_tag(tokens)
            cleaned_tagged_list = []
            for each_value, each_tag in tagged:
                if each_tag and each_tag in self.all_tags:
                    cleaned_tagged_list.append(tuple((each_value, each_tag)))
            entities = nltk.chunk.ne_chunk(cleaned_tagged_list)
            for elem in entities:
                if isinstance(elem, nltk.Tree):
                    pass
                else:
                    pass

    async def classify_text_topics(self):
        en_stopwords = stopwords.words('english')
        lmr = WordNetLemmatizer()
        page_doc = []
        for t in word_tokenize(self.page_text):
            if t.isalpha():
                t = lmr.lemmatize(t.lower())
                if t not in en_stopwords:
                    page_doc.append(t)
