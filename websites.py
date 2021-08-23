from collections import deque
from harvest import Harvester
import threading
class Websites:
    def __init__(self, host, visited,header, proxy, timeout, domain):
        self.host = host
        self.header = header
        self.proxy = proxy
        self.timeout = timeout

        self.websites = {
            'Google': {
                'Google': 'https://www.google.com/search?num=25&start=0&hl=en&q="@{word}"'
            },
            'Bing': {
                'Bing': 'http://www.bing.com/search?q="@{word}"&count=25&first=0'
            },
            'Yahoo': {
                'Yahoo': 'http://search.yahoo.com/search?p="@{word}"&n=25&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b=0'
            },
            'Github': {
                'Google' : 'https://www.google.com/search?num=25&start=0&hl=en&q=site%3Agithub.com "@{word}"',
                'Yahoo': 'http://search.yahoo.com/search?p=site%3Agithub.com "@{word}"&n=25&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b=0',
                'Bing': 'http://www.bing.com/search?q=site%3Agithub.com "@{word}"&count=25&first=0',
            },
            'LinkedIn': {
                'Google': 'https://www.google.com/search?num=25&start=0&hl=en&q=site%3Alinkedin.com "@{word}"',
                'Yahoo': 'http://search.yahoo.com/search?p=site%3Alinkedin.com "@{word}"&n=25&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b=0',
                'Bing': 'http://www.bing.com/search?q=site%3Alinkedin.com "@{word}"&count=25&first=0'
            },
            'Twitter': {
                'Google': 'https://www.google.com/search?num=25&start=0&hl=en&q=site%3Atwitter.com+intitle:"on Twitter" "@{word}"',
                'Yahoo': 'http://search.yahoo.com/search?p=site%3Atwitter.com "@{word}"&n=25&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b=0',
                'Bing': 'http://www.bing.com/search?q=site%3Atwitter.com "@{word}"&count=25&first=0'
            }
        }
        self.urls = deque()
        self.visited = visited
        for url in self.websites[host]:
            self.urls.append((self.websites[host][url].format(word=domain), 0))
    
    def search(self, domain):
        print("[+] Searching for emails in "+ self.host)
        all_emails = []
        harvester = Harvester(self.header, self.proxy, self.timeout)
        while self.urls:
            url, depth = self.urls.popleft()
            if url in self.visited:
                continue
            if depth>=2:
                continue
            self.visited.add(url)
            harvester.init_search(url, depth, domain, self.urls)
            harvester.process()
            for email in harvester.get_emails():
                all_emails.append(email)
        harvester.close_session()
        return all_emails

AvailableWebsites = {
    '1': 'Bing',
    '2': 'Github',
    '3': 'Google',
    '4': 'LinkedIn',
    '5': 'Twitter',
    '6': 'Yahoo'
}