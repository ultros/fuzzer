# fuzzer
Multithreaded URL fuzzer, directory buster, and exploit suggester (i.e. subdomains, queries, directories)

fuzzer -u http://google.com/?q=FUZZ -w /usr/share/wordlists/dirb/common.txt  


$ python3 fuzzer.py -u https://FUZZ.google.com/ -w /usr/share/wordlists/dirb/common.txt  
Total URLs to fuzz: 4615  
Total invalid words in wordlist: 0  
Forbidden: http://127.0.0.1/.htpasswd  
Forbidden: http://127.0.0.1/.htaccess  
Forbidden: http://10.129.88.84/cgi-bin/  
└─[¿shellshock?] -> Scan for scripts in /cgi-bin/ (e.g. http://127.0.0.1/cgi-bin/FUZZ.sh).  
...  
Temporary redirect: https://127.0.0.1/  
...  
Temporary redirect: https://about.google.com/  
Permanent redirect: https://accounts.google.com/  
Temporary redirect: https://About.google.com/  
...  
