import requests
import re

wl = "/usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt"
url = ''

file = open(wl, 'r')

for parameter in file:
    fuzz = re.findall(">.*?<", url)
    param1 = re.sub('[><]', '', parameter.strip())
    url2 = url.replace(fuzz[0], parameter.strip())

    try:
        req = requests.get(url2, timeout=1)
        if req.status_code == 200:
            print(f"Found parameter: {param1}")
    except Exception as e:
        print(f"***\n{e}\n***")