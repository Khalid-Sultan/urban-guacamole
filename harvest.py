import requests
from requests_html import HTMLSession
import sys
import time
from parser import Parser

class Harvester:

    def __init__(self, userAgent, proxy, timeout):
        self.proxy = proxy
        self.userAgent = userAgent
        self.parser = Parser()
        self.timeout = timeout
        self.session = HTMLSession()

    def init_search(self, url, depth, word, queue):
        self.url = url
        self.wrd = word
        self.depth = depth

        self.queue = queue

        self.results = ""
        self.totalresults = ""

        
    def do_search(self):
        try:
            urly = self.url.format(word=self.wrd)
            headers = {'User-Agent': self.userAgent, "referer":"referer: https://www.google.com/"}
            r = None
            if self.proxy:
                proxies = { self.proxy.scheme: self.proxy.scheme + "://" + self.proxy.netloc}
                r = self.session.get(urly, headers=headers, proxies=proxies)
            else:
                r = self.session.get(urly, headers=headers)
            r.html.render(retries=3,timeout=3)
            for link in r.html.absolute_links:
                self.queue.append((link, self.depth+1))

            self.totalresults += r.html.find('html', first=True).html
        except Exception as err:
            print(err)
            # sys.exit(4)

        
    def process(self):
        self.do_search()
        time.sleep(self.timeout)
        print("[+] Searching in {}".format(self.url.format(word=self.wrd)))

    def get_emails(self):
        self.parser.extract(self.totalresults, self.wrd)
        return self.parser.emails()

    def close_session(self):
        self.session.close()

    def show_message(self, msg):
        print(msg)    

