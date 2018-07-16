import sys, getopt, os, urllib2
from threading import Thread
import threading
from os import listdir
from os.path import isfile, join
from colors import *
import xmltodict

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
|_|    |___/                                          0.3

Web fuzzer in Python

Author: Johannes Schroeter - www.devwerks.net

[!] legal disclaimer: Usage of pyFilebuster for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program

"""

def printRed(string, error):
    errorstring = RED + "%s" % string + " (error: %s)\n" % error + RESET
    sys.stdout.write(errorstring)


def listWordlists():
    onlyfiles = [f for f in listdir(BASE_DIR + "/wordlists/") if isfile(join(BASE_DIR + "/wordlists/", f))]
    sys.stdout.write("%s\n" % onlyfiles)


def request(newurl, timeout, s3):
    try:
        req = urllib2.Request(newurl)
        if s3 == False:
            req.get_method = lambda: "HEAD"
        req.add_header("User-agent", useragent)
        response = urllib2.urlopen(req, timeout=timeout)
        data = response.read()
        content = ""
        if s3:
            objects = xmltodict.parse(data)
            Keys = []
            try:
                for child in objects['ListBucketResult']['Contents']:
                    Keys.append(child['Key'])
            except:
                pass
            for words in Keys:
                content += "%s\n" % words
        output = GREEN + "%s (size: %s)\n" % (newurl, len(data)) + content + RESET
        sys.stdout.write(output)
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


def start(url, wordlist, timeout, s3):
    threads = []
    if wordlist != 0:
        with open(wordlist) as f:
            for line in f:
                newurl = createurl(url.rstrip(), line.rstrip())
                at = threading.activeCount()
                if at <= 10:
                    thread = Thread(target=request, args=(newurl, timeout, s3,))
                    threads.append(thread)
                    thread.start()
                else:
                    request(newurl, timeout, s3)


def scan():
    version()

    wordlist = 0
    timeout  = 600
    url = ''
    s3 = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:u:w:s", ["help", "timeout=", "url=", "word=", "s3"])
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

        elif opt in ("-s", "--s3"):
            url = "http://{fuzz}.s3.amazonaws.com"
            s3 = True

    start(url, wordlist, timeout, s3)


def version():
    sys.stdout.write(banner)


def help():
    sys.stdout.write("filebuster.py -w/--word WORDLIST -t/--timeout -u/--url URL/{fuzz} -s/--s3\n")
    sys.stdout.write("Example: filebuster.py -w fast.txt -u http://test.net/\n")
    sys.stdout.write("Example: filebuster.py -w wordlist.txt -t 30 -u http://test.net/{fuzz}.html\n")
    sys.stdout.write(RED)
    sys.stdout.write("New Feature Enumerate AWS S3 buckets\n")
    sys.stdout.write(RESET)
    sys.stdout.write("Example: filebuster.py -w bucket.txt -s\n\n")

def main():
    scan()
    sys.exit()


if __name__ == "__main__":
    main()
