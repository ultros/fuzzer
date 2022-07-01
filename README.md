# fuzzer
Multithreaded URL fuzzer (i.e. subdomains, queries, directories)

fuzzer -u http://google.com/?q=FUZZ -w /usr/share/wordlists/dirb/common.txt  


$ python3 fuzzer.py -u https://FUZZ.google.com/ -w /usr/share/wordlists/dirb/common.txt  
Total URLs to fuzz: 4615  
Total invalid words in wordlist: 0  
Temporary redirect: https://1.google.com/  
Temporary redirect: https://about.google.com/  
Permanent redirect: https://accounts.google.com/  
Temporary redirect: https://About.google.com/  
...  
