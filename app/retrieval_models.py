from indexing import Indexing
from typing import List
import math

class BaseModel():
    def query_on_index(self, query: str):
        raise NotImplementedError("Method not implemented")


class VectorSpaceModel(BaseModel):
    def __init__(self, indexing: Indexing, tf_variation = 5, idf_variation = 5, double_normalization_k = 0.2):
        self.indexing = indexing
        self.tf_idf = {}
        # self.tf_variation = tf_variation
        # self.idf_variation = idf_variation
        self.double_normalization_k = double_normalization_k
        self.max_document_freq = max(self.indexing.document_frequency.values())

        print("Calculating TF-IDF for each document...")
        for docno, word_vector in self.indexing.document_vectors.items():
            self.tf_idf[docno] = self.get_tf_idf(word_vector)
        
        print("Vector Space Model initialized.")

    def get_tf_idf(self, word_vector):
        tf_idf = {}

        for word, freq in word_vector.items():
            # tf = 0
            # idf = 0

            # if self.tf_variation == 1:
            #     # Binary
            #     tf = 1
            # elif self.tf_variation == 2:
            #     # Raw frequency
            #     tf = freq
            # elif self.tf_variation == 3:
            #     # Log normalization
            tf = 1 + math.log(freq)
            # elif self.tf_variation == 4:
            #     # Double normalization 0.5
            #     tf = 0.5 + (0.5 * freq / max(word_vector.values()))
            # elif self.tf_variation == 5:
            #     # Double normalization K [0.1 - 0.9]
            # tf = self.double_normalization_k + ((1 - self.double_normalization_k) * freq / max(word_vector.values()))


            # if self.idf_variation == 1:
            #     # Unary
            #     idf = 1
            # elif self.idf_variation == 2:
            #     # Inverse frequency
            #     idf = self.indexing.total_documents / self.indexing.document_frequency.get(word, 0)
            # elif self.idf_variation == 3:
            #     # Inverse frequency with log
            idf = math.log(self.indexing.total_documents / self.indexing.document_frequency.get(word, 0))
            # elif self.idf_variation == 4:
            #     # Inverse frequency smooth
            #     idf = math.log(1 + (self.indexing.total_documents / self.indexing.document_frequency.get(word, 0)))
            # elif self.idf_variation == 5:
            #     # Inverse frequency max
            # idf = math.log( 1 + (self.max_document_freq / self.indexing.document_frequency.get(word, 0)))
            # elif self.idf_variation == 6:
            #     # Probabilistic inverse frequency
            #     idf = math.log((self.indexing.total_documents - self.indexing.document_frequency.get(word, 0)) / self.indexing.document_frequency.get(word, 0))
                
            tf_idf[word] = tf * idf

        return tf_idf

    
    def calculate_scores(self, query_tokens: List):
        query_terms = set(query_tokens)

        similarity = {}

        # Get list of possible documents from the inverted index
        possible_docs = self.indexing.get_document_list(query_terms)

        # Calculating the tf-idf of query term
        query_dict = {}
        for q in query_tokens:
            if q in self.indexing.document_frequency:
                if q in query_dict:
                    query_dict[q] += 1
                else:
                    query_dict[q] = 1
        query_tfidf = self.get_tf_idf(query_dict)

        # Calculate the similarity score for each document and the query
        for docno in possible_docs:
            document_tf_idf = self.tf_idf[docno]
            word_set = set(document_tf_idf)
            common_pairs = set.intersection(query_terms, word_set)

            score = 0
            for term in common_pairs:
                score += document_tf_idf[term] * query_tfidf[term]

            if score > 0:
                similarity[docno] = score

        return similarity

    def query_on_index(self, query: str):
        # Tokenize the query
        query_tokens = self.indexing.process_text(query)
        
        return self.calculate_scores(query_tokens)
    

class BM25Model():

    def __init__(self, indexing: Indexing, k: float = 2.2, b: float = 0.75):
        self.indexing = indexing
        self.k = k # 1.2 - 2.0
        self.b = b # 0.5 - 0.8

        print("BM25 Model initialized.")

    def calc_w_rjs(self, total_docs, docs_with_term):
        return math.log((total_docs - docs_with_term + 0.5) / (docs_with_term + 0.5))
    
    def calc_normalization_factor(self, doc_len, avg_doc_len):
        return (1 - self.b) + (self.b * (doc_len / avg_doc_len))
    
    def calc_w_bm25(self, tf, total_docs, docs_with_term, doc_len, avg_doc_len):
        w_rjs = self.calc_w_rjs(total_docs, docs_with_term)
        denominator = (self.k * self.calc_normalization_factor(doc_len, avg_doc_len)) + tf
        return (tf / denominator) * w_rjs
    
    def query_on_index(self, query):
        # Tokenize the query
        query_tokens = self.indexing.process_text(query)
        query_tokens = set(query_tokens)

        score_dict = {}

        # Get list of possible documents from the inverted index
        possible_docs = self.indexing.get_document_list(query_tokens)

        for docno in possible_docs:
            doc_len = sum(self.indexing.document_vectors[docno].values())
            doc_score = 0

            for term in query_tokens:
                if term in self.indexing.inverted_index:
                    docs_with_term = self.indexing.document_frequency[term]
                    tf = self.indexing.document_vectors[docno].get(term, 0)
                    w_bm25 = self.calc_w_bm25(tf, self.indexing.total_documents, docs_with_term, doc_len, self.indexing.avg_doc_length)
                    doc_score += w_bm25
            
            score_dict[docno] = doc_score

        return score_dict

# Query Likelyhood Model with Dirichlet Smoothing
class QueryLikelyhoodDPSModel():
    def __init__(self, indexing: Indexing, mu: int = 130):
        self.indexing = indexing
        self.mu = mu
        self.overall_term_probability = {}
        
        for term, doc_freq in indexing.document_frequency.items():
           self.overall_term_probability[term] = doc_freq / indexing.total_documents

        print("Query Likelyhood Model Initialized.")

    def calculate_score(self, query_tokens):
        score_dict = {}

        # Get list of possible documents from the inverted index
        possible_docs = self.indexing.get_document_list(query_tokens)

        for docno in possible_docs:
            word_vector = self.indexing.document_vectors[docno]
            document_size = sum(word_vector.values())

            doc_score = 0
            for word in set(query_tokens):
                # Applying Drichlet Prior Smoothing
                prob = word_vector.get(word, 0) + (self.mu * self.overall_term_probability.get(word, 0)) / (document_size + self.mu)
                if prob > 0:
                    doc_score += math.log(prob)
            
            score_dict[docno] = doc_score

        return score_dict
    
    def query_on_index(self, query):
        # Tokenize the query
        query_tokens = self.indexing.process_text(query)
        return self.calculate_score(query_tokens)