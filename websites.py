class Websites:
    def __init__(self, harvester, host):
        self.harvester = harvester
        self.host = host
        self.websites = {
            'Github': 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Agithub.com+"%40{word}"',
            'Google': 'https://www.google.com/search?num=100&start={counter}&hl=en&q="%40{word}"',
            'Instagram': 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Ainstagram.com+"%40{word}"',
            'LinkedIn': 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Alinkedin.com+"%40{word}"',
            'Reddit': 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Areddit.com+"%40{word}"',
            'Twitter': 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Atwitter.com+intitle:"on Twitter"+"%40{word}"',
            'Youtube': 'https://www.google.com/search?num=100&start={counter}&hl=en&q=site%3Ayoutube.com+"%40{word}"'
        }
        self.url = self.websites[host]

    def search(self, domain, limit):
        all_emails = []
        self.harvester.show_message("[+] Searching for websites in "+ self.host)
        
        #Google is used to filter the host
        self.harvester.init_search(self.url, domain, limit, 0, 100, 'Google + ' + self.host)
        self.harvester.process()

        all_emails += self.harvester.get_emails()
        return all_emails

AvailableWebsites = {
    '1': 'Github',
    '2': 'Google',
    '3': 'Instagram',
    '4': 'LinkedIn',
    '5': 'Reddit',
    '6': 'Twitter',
    '7': 'Youtube'
}