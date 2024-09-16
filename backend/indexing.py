import re
import nltk
import pickle
from nltk.corpus import stopwords as sw
from nltk.stem import PorterStemmer

class Indexing:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        # nltk.download('wordnet')

        self.inverted_index = {} # key: word, value: list of tuples (docno, count)
        self.document_vectors = {} # key: docno, value: dictionary of word frequency
        self.document_frequency = {} # key: word, value: document frequency
        self.avg_doc_length = 0
        self.corpus_size = 0
        self.total_documents = 0

        self.token_pattern = re.compile(r"\b\w{2,}\b")
        self.stopwords = set(sw.words('english'))
        self.stemmer = PorterStemmer()

    def save_object(self, filename):
        obj = {
            "inverted_index": self.inverted_index,
            "document_vectors": self.document_vectors,
            "document_frequency": self.document_frequency,
            "avg_doc_length": self.avg_doc_length,
            "corpus_size": self.corpus_size,
            "total_documents": self.total_documents
        }

        with open(filename, "wb") as f:
            pickle.dump(obj, f)

    def load_object(self, filename):
        with open(filename, "rb") as f:
            obj = pickle.load(f)
            self.inverted_index = obj["inverted_index"]
            self.document_vectors = obj["document_vectors"]
            self.document_frequency = obj["document_frequency"]
            self.avg_doc_length = obj["avg_doc_length"]
            self.corpus_size = obj["corpus_size"]
            self.total_documents = obj["total_documents"]

    def process_text(self, text): 
        # Creating tokens from the text  
        temp = self.token_pattern.findall(text.lower())    

        # Removing stopwords  
        temp = [x for x in temp if x not in self.stopwords]

        # Performing stemming operation
        temp = [self.stemmer.stem(x) for x in temp]
        return temp

    def build_index(self, data: list):
        self.total_documents = len(data)

        for i, doc in enumerate(data):
            # Selecting the text to be indexed
            document_fields = []
            document_fields.append(doc['group'])
            document_fields.append(doc['label'])
            document_fields.append(doc['caption'])
            for x in doc['cv']:
                document_fields.append(x['label'])

            tokens = self.process_text(" ".join(document_fields))

            # Calculating the word frequency for each document
            word_vector = {}
            for word in tokens:
                word_vector[word] = word_vector.get(word, 0) + 1

            # Creating the inverted index and document frequency
            for word, freq in word_vector.items():
                if self.inverted_index.get(word) is None:
                    self.inverted_index[word] = []
                self.inverted_index[word].append((doc["docno"], freq))

                # Calculating the document frequency for each word
                self.document_frequency[word] = self.document_frequency.get(word, 0) + 1

                self.corpus_size += freq

            self.document_vectors[doc["docno"]] = word_vector
        
            print(f"Indexing... ({i + 1} / {len(data)})", end="\r")

        # Calculating some stats
        self.avg_doc_length = self.corpus_size / self.total_documents
        print("\nIndexing completed.")

    def get_document_list(self, query_terms):
        """
        Get the list of documents from inverted_index for the given query terms
        """
        document_list = set()
        for term in query_terms:
            if term in self.inverted_index:
                document_list.update([x[0] for x in self.inverted_index[term]])
        return document_list
