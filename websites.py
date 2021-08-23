from collections import deque
class Websites:
    def __init__(self, harvester, host, visited):
        self.harvester = harvester
        self.host = host
        self.websites = {
            'Google': {
                'Google': 'https://www.google.com/search?num=25&start=0&hl=en&q="%40{word}"'
            },
            'Bing': {
                'Bing': 'http://www.bing.com/search?q="%40{word}"&count=25&first=0'
            },
            'Yahoo': {
                'Yahoo': 'http://search.yahoo.com/search?p="%40{word}"&n=25&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b=0'
            },
            'Github': {
                'Google' : 'https://www.google.com/search?num=25&start=0&hl=en&q=site%3Agithub.com+"%40{word}"',
                'Yahoo': 'http://search.yahoo.com/search?p=site%3Agithub.com+"%40{word}"&n=25&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b=0',
                'Bing': 'http://www.bing.com/search?q=site%3Agithub.com+"%40{word}"&count=25&first=0',
            },
            'LinkedIn': {
                'Google': 'https://www.google.com/search?num=25&start=0&hl=en&q=site%3Alinkedin.com+"%40{word}"',
                'Yahoo': 'http://search.yahoo.com/search?p=site%3Alinkedin.com+"%40{word}"&n=25&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b=0',
                'Bing': 'http://www.bing.com/search?q=site%3Alinkedin.com+"%40{word}"&count=25&first=0'
            },
            'Twitter': {
                'Google': 'https://www.google.com/search?num=25&start=0&hl=en&q=site%3Atwitter.com+intitle:"on Twitter"+"%40{word}"',
                'Yahoo': 'http://search.yahoo.com/search?p=site%3Atwitter.com+"%40{word}"&n=25&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b=0',
                'Bing': 'http://www.bing.com/search?q=site%3Atwitter.com+"%40{word}"&count=25&first=0'
            }
        }
        self.urls = deque()
        self.visited = visited
        for url in self.websites[host]:
            self.urls.append((self.websites[host][url], 0))
    
    def search(self, domain):
        all_emails = []
        self.harvester.show_message("[+] Searching for websites in "+ self.host)

        while self.urls:
            url,depth = self.urls.popleft()   
            if url in self.visited:
                continue
            if depth>1:
                continue
            self.visited.add(url)     
            self.harvester.init_search(url, depth, domain, url, self.urls)
            self.harvester.process()
            all_emails += self.harvester.get_emails()
        return all_emails

AvailableWebsites = {
    '1': 'Bing',
    '2': 'Github',
    '3': 'Google',
    '4': 'LinkedIn',
    '5': 'Twitter',
    '6': 'Yahoo'
}