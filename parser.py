import re

class Parser:
    def __init__(self):
        self.temp = []
        
    def extract(self, results, word):
        self.results = results
        self.word = word

    def cleanInput(self):
        pass
        # keywords = {'<KW>', '</KW>', '</a>', '<b>', '</b>', '</div>', '<em>', '</em>', '<p>', '</span>',
        #             '<strong>', '<title>', '<wbr>', '</wbr>'}
        # tags = {'%2f', '%3a', '%3A', '%3C', '%3D', '&', '/', ':', ';', '<', '=','>','\\'}
        # for e in keywords | tags:
        #     self.results = self.results.replace(e, '')
        
    def emails(self):
        self.cleanInput()
        # reg_emails = re.compile(
        #     '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' +
        #     '@' +
        #     self.word)
        words = '\.'.join(self.word.split('.'))
        self.temp = re.findall(r'[\w\.-]+@' + words ,self.results)
        emails = self.unique()
        return emails
    
    def unique(self):
        return list(set(self.temp))