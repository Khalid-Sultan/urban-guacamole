## GUAC
#### Email Harvester written in python

This is a rough implementation in python for the purpose of email harvesting. It first scrapes possible choices based on the engines it has at the moment before going up to 2 levels deep based on the websites it encounters while traversing. 
`Results may come off slow depending on the **internet bandwidth**, **selected engines** and **timeout** parameter provided.

It's an **interactive** script that guides you on filling out necessary parameters needed for running the script.

Features included:
- Input Domain Email Searching
- Engines include Google, Github, Twitter, Bing, Yahoo, LinkedIn
- Custom Header or Proxy Support
- Custom Timeout
- File output

To run the script, use the following steps

1. Install requirements
`pip install -r requirements.txt`
2. Run the following on the terminal
`python main.py`
3. Follow the instructions

**Since the script isn't implemented with threading in mind which can greately improve the speed of the script, Use fewer engines.**

**Status Code of 409 and log messages as Document is Empty or Navigation Timeout Exceeded are signs that either you are locked out from the engines due to Terms of Services or insufficient network connection**


#### In order for this script to work as intended, please input a timeout>=2 seconds as most websites block scraping tasks because they go against their terms of services.


### Collaborators

- Eyosias Samson - ATR/0484/09
- Gemmechu Mohammed - ATR/1432/09
- Khalid Sultan - ATR/8444/09
- Tsedeniya Solomon - ATR/9796/09
