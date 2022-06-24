import requests
import re
from typing import TextIO, Tuple


def format_url(url: str, keyword: str) -> str:
    """Returns a formatted URL to fuzz."""
    try:
        if re.search("FUZZ", url):
            url = url.replace("FUZZ", keyword.strip())
        else:
            print("[!] Could not find the \"FUZZ\" string. E.g. \"https://www.google.com/q?=FUZZ\"")
            return 0

    except Exception as e:
        print(e)

    return url


def prepare_wordlist(url: str, wordlist: TextIO) -> Tuple[str, str]:
    """Returns valid URLs and a list of invalid entries discovered in the wordlist."""
    urls = []
    badwords = []

    try:
        file = open(wordlist, 'r')
    except Exception as e:
        print(e)

    try:
        for word in file:
            temp_url = format_url(url, word)
            if temp_url == 0:
                exit()
            urls.append(temp_url)
    except Exception as e:
        badwords.append(word)

    total_urls = len(urls)
    print(f"Total URLs to fuzz: {total_urls}")
    print(f"Total invalid words in wordlist: {len(badwords)}")

    return urls, badwords, total_urls

def pp():
    print("Processing...", end="\r")


def fuzz(url: str, wordlist: TextIO) -> None:
    """Prints valid URLs from queries that resolve."""
    urls = prepare_wordlist(url, wordlist)
    i = 0
    try:
        i += 1
        for url in urls[0]:
            req = requests.get(url, timeout=1)
            match req.status_code:
                case 200:
                    print(f"Discovered: {url}")
                case 301:
                    print(f"Permanent redirect: {url}")
                case 302:
                    print(f"Temporary redirect: {url}")
                case _:
                    continue
            print(f"{i} of {urls[2]}")
        print(f"Did not process: {urls[1]}")
    except Exception as e:
        print(f"***\n{e}\n***")


def main() -> None:
    wordlist = "/usr/share/wordlists/rockyou.txt" #dirbuster/directory-list-2.3-small.txt"
    url = 'http://bing.com/FUZZ'

    fuzz(url, wordlist)


if __name__ == '__main__':
    main()
