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
                \n\tExample: Giving 'aait' will make the script search for aait domain having emails")
    domain,err = utils.checkDomain(input())
    if err:
        print(err)
        sys.exit(1)

    print('\n\n Okay the agents I have at the moment are the following: \
                \n\t 1 - Github\
                \n\t 2 - Google\
                \n\t 3 - Instagram\
                \n\t 4 - LinkedIn\
                \n\t 5 - Reddit\
                \n\t 6 - Twitter\
                \n\t 7 - Youtube\
                \n Skip with Clicking enter if you want to search through all \
                \n Or type out with space inbetween, which ones you want to search for like "1 2 4 7"')
    engine = None
    engine,err = utils.cleanEngines(input())
    if err:
        print(err)
        sys.exit(1)
    
    print("\n\n How many emails do you want? \
            \n\tDefault: 100")
    limit,err = utils.limit_type(input())
    if err:
        print(err)
        sys.exit(1)
    limit = min(limit,100)

    print('\n\n Do you want a custom user agent header? Click enter if you want to continue with the default')
    header = input()
    header = header if header else "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"

    print('\n\n Do you want a custom proxy to check with? Click enter if you want to continue with the default')
    proxy, err = utils.checkProxyUrl(input())
    if err:
        print(err)
        sys.exit(1)

    print(header, proxy, domain, limit)
    app = Harvester(header, proxy)
    all_emails = []

    for e in engine:
        w = Websites(app, e)
        all_emails += w.search(domain, limit)

    all_emails = list(set(all_emails))
    
    if not all_emails:
        print("[-] No emails found")
        sys.exit(1)

    print("[+] Emails found: ")
    for emails in all_emails:
        print(emails)
    
    inp = input("Hi, It's me again, do you want these emails saved to a file? y/n")
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
