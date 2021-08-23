from collections import deque
class Websites:
    def __init__(self, harvester, host, visited):
        self.harvester = harvester
        self.host = host
        self.websites = {
            'Google': {
                'Google': 'https://www.google.com/search?num=100&start={0}&hl=en&q="%40{word}"'
            },
            'Bing': {
                'Bing': 'http://www.bing.com/search?q=%40{word}&count=50&first={0}'
            },
            'Yahoo': {
                'Yahoo': "http://search.yahoo.com/search?p=%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={0}"
            },
            'Github': {
                'Google' : 'https://www.google.com/search?num=100&start={0}&hl=en&q=site%3Agithub.com+"%40{word}"',
                'Yahoo': "http://search.yahoo.com/search?p=site%3Agithub.com+%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={0}",
                'Bing': "http://www.bing.com/search?q=site%3Agithub.com+%40{word}&count=50&first={0}",
            },
            'Instagram': {
                'Google': 'https://www.google.com/search?num=100&start={0}&hl=en&q=site%3Ainstagram.com+"%40{word}"',
                'Yahoo': "http://search.yahoo.com/search?p=site%3Ainstagram.com+%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={0}",
                'Bing': "http://www.bing.com/search?q=site%3Ainstagram.com+%40{word}&count=50&first={0}"
            },
            'LinkedIn': {
                'Google': 'https://www.google.com/search?num=100&start={0}&hl=en&q=site%3Alinkedin.com+"%40{word}"',
                'Yahoo': "http://search.yahoo.com/search?p=site%3Alinkedin.com+%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={0}",
                'Bing': "http://www.bing.com/search?q=site%3Alinkedin.com+%40{word}&count=50&first={0}"
            },
            'Reddit': {
                'Google': 'https://www.google.com/search?num=100&start={0}&hl=en&q=site%3Areddit.com+"%40{word}"',
                'Yahoo': "http://search.yahoo.com/search?p=site%3Areddit.com+%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={0}",
                'Bing': "http://www.bing.com/search?q=site%3Areddit.com+%40{word}&count=50&first={0}"
            },
            'Twitter': {
                'Google': 'https://www.google.com/search?num=100&start={0}&hl=en&q=site%3Atwitter.com+intitle:"on Twitter"+"%40{word}"',
                'Yahoo': "http://search.yahoo.com/search?p=site%3Atwitter.com+%40{word}&n=100&ei=UTF-8&va_vt=any&vo_vt=any&ve_vt=any&vp_vt=any&vd=all&vst=0&vf=all&vm=p&fl=0&fr=yfp-t-152&xargs=0&pstart=1&b={0}",
                'Bing': "http://www.bing.com/search?q=site%3Atwitter.com+%40{word}&count=50&first={0}"
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
            if depth>2:
                continue
            self.visited.add(url)     
            self.harvester.init_search(url, depth, domain, url, self.urls)
            self.harvester.process()
            all_emails += self.harvester.get_emails()
        return all_emails

AvailableWebsites = {
    '1': 'Github',
    '2': 'Google',
    '3': 'Instagram',
    '4': 'LinkedIn',
    '5': 'Reddit',
    '6': 'Twitter'
}