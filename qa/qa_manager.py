import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .qa_retriever import QARetriever
from .qa_knowledge import QAKnowledge

class QAManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.knowledge = QAKnowledge()
        self.general_qa = self.knowledge.get_general_qa()
        self.retriever = QARetriever(self.general_qa)
    
    def find_answer(self, query):
        answer, score = self.retriever.retrieve(query)
        return answer
    
    def get_movie_answer(self, query, movie):
        query_lower = query.lower()
        patterns = self.knowledge.get_movie_specific_patterns()
        
        if any(word in query_lower for word in ['genre', 'type', 'kind', 'category']):
            return f"{movie['title']} {patterns['genre'].format(genre=movie['genre'])}"
        
        if any(word in query_lower for word in ['director', 'directed', 'who made', 'filmmaker']):
            return f"{movie['title']} {patterns['director'].format(director=movie['director'])}"
        
        if any(word in query_lower for word in ['star', 'cast', 'actor', 'actress', 'who is in']):
            cast_str = ', '.join(movie['cast'])
            return f"{movie['title']} {patterns['cast'].format(cast=cast_str)}"
        
        if any(word in query_lower for word in ['time', 'when', 'showtime', 'screening']):
            times_str = ', '.join(movie['times'])
            return f"{movie['title']} {patterns['time'].format(times=times_str)}"
        
        if any(word in query_lower for word in ['price', 'cost', 'much', 'expensive']):
            return f"Tickets for {movie['title']} {patterns['price'].format(price=movie['price'])}"
        
        if any(word in query_lower for word in ['rating', 'rated', 'age', 'certificate']):
            return f"{movie['title']} {patterns['rating'].format(rating=movie['rating'])}"
        
        if any(word in query_lower for word in ['long', 'duration', 'runtime', 'length']):
            return f"{movie['title']} {patterns['duration'].format(duration=movie['duration'])}"
        
        if any(word in query_lower for word in ['about', 'plot', 'story', 'synopsis']):
            return f"{movie['title']}: {patterns['plot'].format(description=movie['description'])}"
        
        return None

if __name__ == "__main__":
    print("QAManager module loaded successfully!")