import requests
import re
import argparse
import os
from typing import TextIO, Tuple


def random_user_agent():


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


def prepare_wordlist(url: str, wordlist: TextIO) -> Tuple[str, str, str]:
    """Returns valid URLs, a total of all words, and a list of invalid words discovered in the wordlist."""
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

    for url in urls[0]:
        try:
            req = requests.get(url, timeout=10)
            match req.status_code:
                case 200:
                    print(f"Discovered: {url}")
                case 301:
                    print(f"Permanent redirect: {url}")
                case 302:
                    print(f"Temporary redirect: {url}")
                case _:
                    continue
        except Exception as e:
            print(f"***\n{e}\n***")

    print(f"Did not process: {urls[1]}")


def main() -> None:
    parser = argparse.ArgumentParser(description='URL Fuzzer (E.g. ')
    parser.add_argument('-u', '--url', required=True, type=str,
                        default=None, dest="url",
                        help="Specify URL to fuzz (e.g. www.google.com?q=FUZZ")
    parser.add_argument('-w', '--wordlist', required=True, type=str,
                        default=None,
                        help='Specify wordlist to use (e.g. /usr/share/wordlists/rockyou.txt)')

    args = parser.parse_args()

    if args.url is not None:
        url = args.url
    if (args.wordlist is not None) and (os.path.isfile(args.wordlist)):
        wordlist = args.wordlist
    else:
        print(f"[!] Invalid wordlist")
        exit(0)

    fuzz(url, wordlist)


if __name__ == '__main__':
    main()
