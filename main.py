import sys
import time
import utils
from harvest import Harvester
from websites import Websites

if __name__ == '__main__':
    print("\
        █████████████████████████████████████████████████████████████\n\
        █░░░░░░░░░░░░░░█░░░░░░██░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█\n\
        █░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█\n\
        █░░▄▀░░░░░░░░░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░░░█\n\
        █░░▄▀░░█████████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░█████████\n\
        █░░▄▀░░█████████░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░█████████\n\
        █░░▄▀░░██░░░░░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░█████████\n\
        █░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░█████████\n\
        █░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░█████████\n\
        █░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█\n\
        █░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█\n\
        █░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░██░░░░░░█░░░░░░░░░░░░░░█\n\
        █████████████████████████████████████████████████████████████")
    print("Hi, I am Guac")
    print("I am your friendly email harvester for 'educational' purposes and nothing more ;) ")
    print("\n\n What's the domain you want to harvest emails for? \
                \n\tExample: Giving 'gmail.com' will make the script search for gmail domain having emails")
    domain,err = utils.checkDomain(input())
    if err:
        print(err)
        sys.exit(1)

    print('\n Okay the agents(Using Google, Yahoo and Bing) I have at the moment are the following: \
                \n\t 1 - Bing\
                \n\t 2 - Github\
                \n\t 3 - Google\
                \n\t 4 - LinkedIn\
                \n\t 5 - Twitter\
                \n\t 6 - Yahoo\
                \n Skip with Clicking enter if you want to search through all \
                \n Or type out with space inbetween, which ones you want to search for like "1 2 4"')
    engine = None
    engine,err = utils.cleanEngines(input())
    if err:
        print(err)
        sys.exit(1)

    print('\n Do you want a custom user agent header? Click enter if you want to continue with the default')
    header = input()
    header = header if header else "Chrome"

    print('\n Do you want a custom proxy to check with? Click enter if you want to continue with the default')
    proxy, err = utils.checkProxyUrl(input())
    if err:
        print(err)
        sys.exit(1)

    print('\n Last but not least, the program runs on a 2 second break between each request \
        \n\t to avoid being locked out from most companies TOS violation \
        \n\t Do you want to set a custom timer check (In seconds)? \
        \n\t Default: 2')
    timeout, err = utils.timeout_limit(input())
    if err:
        print(err)
        sys.exit(1)

    print(header, proxy, domain)
    app = Harvester(header, proxy, timeout)
    all_emails = []
    visited = set()
    for e in engine:
        w = Websites(app, e, visited)
        all_emails += w.search(domain)

    all_emails = list(set(all_emails))
    
    if not all_emails:
        print("[-] No emails found")
        sys.exit(1)

    print("[+] Emails found: ")
    for emails in all_emails:
        print(emails)
    
    print("Hi, It's me again, do you want these emails saved to a file? y/n")
    inp = input()
    if inp and (inp=='y' or inp=='Y'):
        try:
            now = time.localtime()
            timestamp = time.strftime("%Y%m%d_%H%M%S", now)
            filename = "{}_{}.txt".format(domain, timestamp)
            with open(filename, 'w') as out_file:
                for email in all_emails:
                    try:
                        out_file.write(email + "\n")
                    except:
                        print("Couldn't add this email to a file: " + email)
        except Exception as e:
            print("Error occured while saving to a file: " + e)
