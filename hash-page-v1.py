from concurrent.futures import ThreadPoolExecutor
import requests
from timer import timer
import hashlib

with open(r'domain-url.txt', 'r') as file:
    DOMAINS = file.read().splitlines()
    
# URL = 'https://en.wikipedia.org/wiki/Special:Random'

verify_hash = '36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4'

def HashPageSHA512 (response, url):
    PageToSHA512 = hashlib.sha512(response.content).hexdigest()
    if verify_hash == str(PageToSHA512):
        print('SHA512: YES | ', url)
        exit()  
    # Comment the below lines if you don't want any output until the HASH is found
    else:
        print('====================')
        print('SHA512: NO | ', url)
    # We remove the last URL it checked so the list will decrease.
    # Unsure if this actually decreases the time taken
    DOMAINS.remove(url)
    return


timeoutDelay = 2
def fetch (session, url):
    with session.get(url, timeout=timeoutDelay) as response:
        HashPageSHA512 (response, response.url)

# Once finished this will tell us how long it took to complete the whole list so you can calculate how long it would take for future attempts
# Using the second function below you can visit the random wiki page 5000 times using 10 workers. 
# This only takes approx 16seconds to complete. 
@timer(1, 1)
randomWikiHashAttempts = 5000
threadWorkers = 10
def main():
        with ThreadPoolExecutor(max_workers=threadWorkers) as executor:
            with requests.Session() as session:
                    # this will send each URL in the DOMAINS array to be hashed
                    executor.map(fetch, [session] * len(DOMAINS), [DOMAINS][0])
                    
                    # Use this one if you want to just check a how long it would take to visit random wiki pages and hash the page contents
                    # executor.map(fetch, [session] * randomWikiHashAttempts, [URL] * randomWikiHashAttempts)
                    executor.shutdown(wait=True)
