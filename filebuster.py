import sys, getopt, os, urllib2
from threading import Thread
from os import listdir
from os.path import isfile, join
from colors import *

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0"

banner = """
            ______ _ _     ______           _
            |  ___(_) |    | ___ \         | |
 _ __  _   _| |_   _| | ___| |_/ /_   _ ___| |_ ___ _ __
| '_ \| | | |  _| | | |/ _ \ ___ \ | | / __| __/ _ \ '__|
| |_) | |_| | |   | | |  __/ |_/ / |_| \__ \ ||  __/ |
| .__/ \__, \_|   |_|_|\___\____/ \__,_|___/\__\___|_|
| |     __/ |
|_|    |___/                                          0.2

Web fuzzer in Python

Author: Johannes Schroeter - www.devwerks.net

[!] legal disclaimer: Usage of pyFilebuster for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program

"""

def printRed(string, error):
    sys.stdout.write(RED)
    sys.stdout.write("%s" % string)
    sys.stdout.write(" (error: %s)\n" % error)
    sys.stdout.write(RESET)


def listWordlists():
    onlyfiles = [f for f in listdir(BASE_DIR + "/wordlists/") if isfile(join(BASE_DIR + "/wordlists/", f))]
    sys.stdout.write("%s\n" % onlyfiles)


def request(newurl, timeout):
    try:
        req = urllib2.Request(newurl)
        req.get_method = lambda: "HEAD"
        req.add_header("User-agent", useragent)
        response = urllib2.urlopen(req, timeout=timeout)
        data = response.read()
        sys.stdout.write(GREEN)
        output = "%s (size: %s)\n" % (newurl, len(data))
        sys.stdout.write(output)
        sys.stdout.write(RESET)
    except urllib2.HTTPError, e:
        printRed(newurl, e.code)
    except urllib2.URLError, e:
        printRed(newurl, e.args)


def createurl(url, word):
    if url.find("{fuzz}") != -1:
        return url.replace("{fuzz}", word)
    else:
        newurl = url + word
        return newurl


def start(url, wordlist, timeout):
    if wordlist != 0:
        with open(wordlist) as f:
            thread = Thread(target=request, args=(url, timeout,))
            thread.start()
            thread.join()
            for line in f:
                newurl = createurl(url.rstrip(), line.rstrip())
                thread = Thread(target=request, args=(newurl, timeout,))
                thread.start()
                thread.join()


def scan():
    version()

    wordlist = 0
    timeout  = 600
    url = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:u:w:", ["help", "timeout=", "url=", "word="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:

        if opt in ("-h", "--help"):
            help()
            sys.exit()

        elif opt in ("-t", "--timeout"):
            timeout = float(arg)

        elif opt in ("-w", "--word"):
            path = BASE_DIR + "/wordlists/" + arg
            if os.path.isfile(path):
                wordlist = path
            else:
                listWordlists()
                sys.exit()

        elif opt in ("-u", "--url"):
            url = arg

    start(url, wordlist, timeout)


def version():
    sys.stdout.write(banner)


def help():
    sys.stdout.write("filebuster.py -w/--word WORDLIST -t/--timeout -u/--url URL/{fuzz}\n")
    sys.stdout.write("Example: filebuster.py -w fast.txt -u http://test.net/\n")
    sys.stdout.write("Example: filebuster.py -w wordlist.txt -t 30 -u http://test.net/{fuzz}.html\n\n")


def main():
    scan()
    sys.exit()


if __name__ == "__main__":
    main()
