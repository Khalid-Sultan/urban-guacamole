# Standard Python libraries.
import argparse
import queue
import re
import sys
import threading
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from worker import Worker

class harvest:
    def __init__(self, domain, search_max, delay, url_timeout, num_threads):
        self.domain = domain
        self.search_max = search_max
        self.num_max = min(search_max, 100)
        self.delay = delay
        self.url_timeout = url_timeout
        self.all_emails = []
        self.queue = queue.Queue()
        self.num_threads = num_threads
        self.guac = None

    def go(self, guac):
        self.guac = guac

        for i in range(self.num_threads):
            thread = Worker(self.guac)
            thread.daemon = True
            thread.start()

        self.google_search()

        self.display_emails()

        if self.all_emails:
            inp = input("Hi, It's me again, do you want these emails saved to a file? y/n")
            if inp and (inp=='y' or inp=='Y'):
                now = time.localtime()
                timestamp = time.strftime("%Y%m%d_%H%M%S", now)
                with open("{}_{}.txt".format(self.domain, timestamp), "a") as fh:
                    for email in self.parsed_emails:
                        fh.write("{}\n".format(email))

    def google_search(self):
        query = "{} -site:{}".format(self.domain, self.domain)
        print("[*] (PASSIVE) Searching for emails NOT within the domain's site: {}".format(query))

        for url in googlesearch.search(
            query,
            start=0,
            stop=self.search_max,
            num=self.num_max,
            pause=self.delay,
            extra_params={"filter": "0"},
            tbs="li:1",
        ):
            self.queue.put(url)

        query = "site:{}".format(self.domain)

        print("[*] (ACTIVE) Searching for emails within the domain's sites: {}".format(self.domain))
        for url in googlesearch.search(
            query,
            start=0,
            stop=self.search_max,
            num=self.num_max,
            pause=self.delay,
            extra_params={"filter": "0"},
            tbs="li:1",  
        ):
            self.queue.put(url)

        self.guac.queue.join()

    def display_emails(self):
        if not self.all_emails:
            print("[-] No emails found. :(")
        else:
            self.parsed_emails = list(sorted(set([element.lower() for element in self.all_emails])))
            print("\n[+] {} unique emails found: ".format(len(self.parsed_emails)))
            print("---------------------------")
            for i, email in enumerate(self.parsed_emails):
                print(i, '.', email)
