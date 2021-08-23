import validators
from websites import AvailableWebsites
from urllib.parse import urlparse
  
def checkProxyUrl(url):
    try:
        if not url:
            return None, None
        url_checked = urlparse(url)
        if (url_checked.scheme not in ('http', 'https')) | (url_checked.netloc == ''):
            return None, 'Invalid {} Proxy URL (example: http://127.0.0.1:8080).'.format(url)
        return url_checked, None
    except:
        return None, 'Invalid {} Proxy URL (example: http://127.0.0.1:8080).'.format(url)


def timeout_limit(x):
    try:
        if not x:
            return 2, None
        x = int(x)
        if x > 0:
            return x, None
        return None, "Minimum results timeout is 1."
    except:
        return None, "Invalid timeout provided {}".format(x)

def checkDomain(value):
    try:
        domain_checked = validators.domain(value)
        if not domain_checked:
            return None, 'Invalid {} domain.'.format(value)
        return value, None
    except:
        return None, "Invalid domain provided {}".format(value)

def cleanEngines(chosen):
    try:
        chosen = chosen.strip()
        res = []
        if not chosen or chosen == '':
            return list(AvailableWebsites.values()), None
        chosen = chosen.split()
        for i in chosen:
            if i!='' and str(i) in AvailableWebsites:
                res.append(AvailableWebsites[i])
            else:
                return None, 'Invalid choice selected {}'.format(i)
        if not res:
            return list(AvailableWebsites.values()), None
        return res, None
    except:
        return None, 'Invalid choices selected'
