import re
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def download_nltk_data():
    datasets = ['punkt', 'punkt_tab', 'stopwords']
    for dataset in datasets:
        try:
            nltk.data.find(f'tokenizers/{dataset}')
        except LookupError:
            try:
                nltk.download(dataset, quiet=True)
            except:
                pass

download_nltk_data()

class TextProcessor:
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text):
        text = text.lower().strip()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return text
    
    def tokenize(self, text):
        text = self.clean_text(text)
        try:
            return word_tokenize(text)
        except LookupError:
            return text.split()
    
    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stop_words]
    
    def stem_tokens(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]
    
    def stem_text(self, text, remove_stops=False):
        tokens = self.tokenize(text)
        if remove_stops:
            tokens = self.remove_stopwords(tokens)
        stemmed = self.stem_tokens(tokens)
        return ' '.join(stemmed)
    
    def extract_name(self, text):
        text_lower = text.lower()
        name = ""
        
        patterns = [
            (r"my name is (\w+)", 1),
            (r"i am (\w+)", 1),
            (r"i'm (\w+)", 1),
            (r"im (\w+)", 1),
            (r"call me (\w+)", 1),
            (r"this is (\w+)", 1),
        ]
        
        for pattern, group in patterns:
            match = re.search(pattern, text_lower)
            if match:
                name = match.group(group)
                break
        
        if not name:
            tokens = text.split()
            if tokens:
                name = tokens[0]
        
        name = re.sub(r"[^a-zA-Z]", "", name)
        return name.capitalize() if name else None
    
    def extract_number(self, text):
        for word in text.split():
            if word.isdigit():
                return int(word)
        
  
        word_to_num = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        
        text_lower = text.lower()
        for word, num in word_to_num.items():
            if word in text_lower:
                return num
        
        return None
    
    def parse_seats(self, text):
        pattern = r'([A-E])(\d+)'
        matches = re.findall(pattern, text.upper())
        return [(row, int(num)) for row, num in matches]

if __name__ == "__main__":
    print("TextProcessor module loaded successfully!")