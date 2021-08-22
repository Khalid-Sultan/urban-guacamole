import requests
import sys
import time
from parser import Parser

class Harvester:

    def __init__(self, userAgent, proxy):
        self.proxy = proxy
        self.userAgent = userAgent
        self.parser = Parser()
    
    def show_message(self, msg):
        print(msg)
        
    def init_search(self, url, word, limit, counterInit, counterStep, engineName):
        self.url = url
        self.word = word
        self.limit = int(limit)

        self.ctr = int(counterInit)
        self.step = int(counterStep)

        self.activeEngine = engineName

        self.results = ""
        self.totalresults = ""
        
    def do_search(self):
        try:
            urly = self.url.format(counter=str(self.ctr), word=self.word)
            headers = {'User-Agent': self.userAgent}
            r = None
            if self.proxy:
                proxies = {self.proxy.scheme: "http://" + self.proxy.netloc}
                r=requests.get(urly, headers=headers, proxies=proxies)
            else:
                r=requests.get(urly, headers=headers)

            if r.encoding is None:
                r.encoding = 'UTF-8'
            self.results = r.content.decode(r.encoding)
            self.totalresults += self.results
                
        except Exception as e:
            print(e)
            sys.exit(4)

        
    def process(self):
        while self.ctr < self.limit:
            self.do_search()
            time.sleep(1)
            self.ctr += self.step
            print("[+] Searching in {}: {} results ".format(self.activeEngine, str(self.ctr)))

    def get_emails(self):
        self.parser.extract(self.totalresults, self.word)
        return self.parser.emails()
