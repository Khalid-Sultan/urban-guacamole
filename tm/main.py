from harvester import harvest


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
domain = input()

print("\n\n How many emails do you want? \
            \n\tDefault: 100")
limit = int(input())
limit = limit if limit else 100

delay = 7
url_timeout = 60
threads = 12

guac = harvest(domain, limit, delay, url_timeout, threads)
guac.go(guac)

print("\n You're welcome. Come back again for more exploration :)")