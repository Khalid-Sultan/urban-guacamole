import re

class Parser:
    def __init__(self):
        self.temp = []
        
    def extract(self, results, word):
        self.results = results
        self.word = word
        
    def emails(self):
        words = '\.'.join(self.word.split('.'))
        return re.findall(r'[\w\.-]+@' + words ,self.results)