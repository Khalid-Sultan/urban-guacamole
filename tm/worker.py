import threading
import requests
import re

class Worker(threading.Thread):
    def __init__(self, guac):
        threading.Thread.__init__(self)
        self.guac = guac
        
    def run(self):
        while True:
            url = self.guac.queue.get()
            headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html"}
            try:
                print("[✓] Scraping emails from: {}".format(url))

                response = requests.get(url, headers=headers, verify=False, timeout=self.guac.url_timeout)

                if response.status_code == 200:
                    response_text = response.text
                    for badchar in {"<", ">", ":", "=",  "/", "\\", ";", "&", "%3A", "%3D", "%3C"}:
                        response_text = response_text.replace(badchar, " ")

                    emails = re.findall(r"[a-zA-Z0-9.-_]*@(?:[a-z0-9.-]*\.)?" + self.guac.domain, response_text, re.I)
                    self.guac.all_emails += emails

            except Exception as e:
                print("[✗] Exception: {}".format(e))

            guac.queue.task_done()