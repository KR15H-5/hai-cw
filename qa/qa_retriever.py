import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import SIMILARITY_THRESHOLD

class QARetriever:
    def __init__(self, qa_pairs):
        self.qa_pairs = qa_pairs
        self.questions = list(qa_pairs.keys())
        
        if self.questions:
            self.vectorizer = TfidfVectorizer()
            self.question_vectors = self.vectorizer.fit_transform(self.questions)
        else:
            self.vectorizer = None
            self.question_vectors = None
    
    def retrieve(self, query):
        if not query or not query.strip() or not self.vectorizer:
            return None, 0.0
        
        try:
            query_vec = self.vectorizer.transform([query.lower()])
            similarities = cosine_similarity(query_vec, self.question_vectors)[0]
            
            best_idx = similarities.argmax()
            best_score = similarities[best_idx]
            
            if best_score > SIMILARITY_THRESHOLD:
                best_question = self.questions[best_idx]
                return self.qa_pairs[best_question], best_score
            
            return None, best_score
        except:
            return None, 0.0

if __name__ == "__main__":
    print("QARetriever module loaded successfully!")