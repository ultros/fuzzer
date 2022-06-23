import requests
import re
from typing import TextIO


def format_url(url: str, keyword: str) -> str:
    """Returns a formatted URL to fuzz."""
    try:
        if re.search("FUZZ", url):
            url = url.replace("FUZZ", keyword.strip())
        else:
            print("[!] Could not find the \"FUZZ\" string. E.g. \"https://www.google.com/q?=FUZZ\"")
            return None
    except Exception as e:
        print(e)

    return url


def prepare_wordlist(url: str, wordlist: TextIO) -> None:
    """Returns valid URLs and a list of unsupported values discovered in the wordlist."""
    urls = []
    badwords = []

    try:
        file = open(wordlist, 'r')
    except Exception as e:
        print(e)

    try:
        for word in file:
            urls.append(format_url(url, word))
    except Exception as e:
        badwords.append(word)

    print(f"Total URLs to fuzz: {len(urls)}")
    print(f"Total invalid words in wordlist: {len(badwords)}")

    return urls, badwords

def fuzz(url: str, wordlist: TextIO) -> None:
    """Prints valid URLs from queries that resolve."""
    urls = prepare_wordlist(url, wordlist)
    try:
        for url in urls[0]:
            req = requests.get(url, timeout=1)
            if req.status_code == 200:
                print(f"Discovered: {url}")
            else:
                print(req.status_code)
    except Exception as e:
        print(f"***\n{e}\n***")


def main() -> None:
    wordlist = "/usr/share/wordlists/rockyou.txt"
    url = 'http://google.com/?q=FUZsZ'

    fuzz(url, wordlist)


if __name__ == '__main__':
    main()
