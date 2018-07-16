# pyFileBuster [![Build Status](https://travis-ci.org/devwerks/pyfilebuster.svg?branch=master)](https://travis-ci.org/devwerks/pyfilebuster)
A fast web fuzzer written in Python. With support for AWS S3 buckets.

### Why?:
The Idea behind this is from [Filebuster](https://github.com/henshin/filebuster). But i hate PERL and i want to have the
same tool written in Python. So here is it. So far not all features are implemented.

### Wordlists:
Copy new wordlists into the wordlists directory. Now you can load them with out path specification.

### Usage:
```
filebuster.py -w/--word WORDLIST -t/--timeout -u/--url URL/{fuzz} -s/--s3

Example: filebuster.py -w fast.txt -u http://test.net/

Example: filebuster.py -w wordlist.txt -t 30 -u http://test.net/{fuzz}.html

Example: filebuster.py -w bucket.txt -s\n\n")
```

### Contact:
If you run into issues, feel free to get on touch on Twitter, check the current issues or create a new one. Patches are also welcome.

http://devwerks.net 

```
            ______ _ _     ______           _
            |  ___(_) |    | ___ \         | |
 _ __  _   _| |_   _| | ___| |_/ /_   _ ___| |_ ___ _ __
| '_ \| | | |  _| | | |/ _ \ ___ \ | | / __| __/ _ \ '__|
| |_) | |_| | |   | | |  __/ |_/ / |_| \__ \ ||  __/ |
| .__/ \__, \_|   |_|_|\___\____/ \__,_|___/\__\___|_|
| |     __/ |
|_|    |___/                                          0.3

Web fuzzer in Python

Author: Johannes Schroeter - www.devwerks.net

[!] legal disclaimer: Usage of pyFilebuster for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program

filebuster.py -w/--word WORDLIST -t/--timeout -u/--url URL/{fuzz} -s/--s3
Example: filebuster.py -w fast.txt -u http://test.net/
Example: filebuster.py -w wordlist.txt -t 30 -u http://test.net/{fuzz}.html
New Feature Enumerate AWS S3 buckets
Example: filebuster.py -w bucket.txt -s
```

### TODO:
- add more Features
