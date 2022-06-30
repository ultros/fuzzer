import requests
import re
import argparse
import os
import concurrent.futures
from typing import TextIO, Tuple, Union

def random_user_agent():
    pass

def format_url(url: str, keyword: str) -> int | str:
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


def prepare_wordlist(url: str, wordlist: TextIO) -> Tuple[list, list, int]:
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


def process_url(url: str) -> str:
    """Performs a GET request for the URL and returns a page status string."""
    res = requests.get(url, timeout=10)
    match res.status_code:
        case 200:
            return f"Discovered: {url}"
        case 301:
            return f"Permanent redirect: {url}"
        case 302:
            return f"Temporary redirect: {url}"
        case _:
            pass

def fuzz(url: str, wordlist: TextIO) -> None:
    """Prints valid URLs from queries that resolve."""
    urls = prepare_wordlist(url, wordlist)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for url in urls[0]:
                futures.append(executor.submit(process_url, url=url))

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            print(res)

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