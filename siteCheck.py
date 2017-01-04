import sys
from urllib2 import Request, urlopen
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM

# ANSI escape sequences
HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# Print string formatted with escape sequence
def print_f(string, seq):
    print seq + string + ENDC

# This function checks for open ports
def portScan(url, limit):
    try:
        print_f("[*] Attempting To Scan %s Ports on %s..." %(limit,url), HEADER)

        url = url.replace("http://www.", "")
        url = url.split("/")

        openports = 0

        for port in range(1, limit+1):

            sock = socket(AF_INET, SOCK_STREAM)

            sock.settimeout(0.5)
            test = sock.connect_ex((url[0],port))

            sys.stdout.write("\r[+] Scanning Port: %s" %port)
            sys.stdout.flush()

            if test == 0:
                print "\n[+] Port: %s" %port
                openports += 1

            sock.close()
        print_f("\n[*] Finished Scanning %s Ports, %s Open Port(s) Found" %(limit, openports), GREEN)
    except:
        print_f("\n[*] Error - No Port Scan available", FAIL)

# This function tests for an open ftp port which makes it vunerable
def ftpTest(url):
    try:
        print_f("[*] Attempting To Test For FTP Vulnerability on %s..." %url, HEADER)

        url = url.replace("http://www.", "")
        url = url.split("/")

        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.5)

        test = sock.connect_ex((url[0],21))

        if test == 0:
            print_f("[+] Port 21 is Open. Site May Be Vulnerable to FTP Attacks", GREEN)

        else:
            print_f("[+] Port 21 is Close. Site Not Vulnerable to FTP Attacks", BLUE)

        sock.close()

    except:
        print_f("[*] Unable to Test for FTP Attack", FAIL)

# This tests a php webpage for any possibility of an SQL injection attack
def sqlTest(url):
    try:
        print_f("[*] Attempting To Test For SQL Vunerability on %s..." %url, HEADER)

        if "http://www." not in url:
            url.strip("www.") #if www. is at the beginning
            url = "http://www."+url

        req = Request(url+"?id=1'")

        response = urlopen(req)
        page = response.read()

        if ("Error" in page) and ("SQL" in page):
            print_f("[+] Site May be Vulnerable to SQL injection Attacks", GREEN)

            url = url.replace("http://www.", "")
            url = url.split("/")
            print "[+] ip address: %s" %gethostbyname(url[0])

        else:
            print_f("[+] No SQL Vulnerabilities Detected", BLUE)

    except:
        print_f("[-] Some Error Occured While Testing", FAIL)
        print_f("[-] Make sure the site is in the format: http://www.example.com/page.php", WARNING)

def help():
    print "[*] '-h' or '--help' [For help]"
    print "[*] '-s' <name of site> [To check for sql injection attack]"
    print "[*] '-f' <name of site> [To check for ftp vulnerability]"
    print "[*] '-p' <name of site> [To scan for open ports up to default]"
    print "[*] '-p' <name of site> -l <# of ports to check> [To scan for open ports up to specified]"

def main():

    if len(sys.argv) < 2:
        print_f("[*] No System Arguments Supplied\n", FAIL)
        help()

    elif sys.argv[1] == '-s':
        sqlTest(sys.argv[2])

    elif sys.argv[1] == '-f':
        ftpTest(sys.argv[2])

    elif sys.argv[1] == '-p' and len(sys.argv) <=3:
        portScan(sys.argv[2], 1024)

    elif sys.argv[1] == '-p' and sys.argv[3] == '-l':
        portScan(sys.argv[2], int(sys.argv[4]))

    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        help()

    else:
        print_f("[-] Error - Check Your Command", FAIL)
        help()

    print "" # leave some space

if __name__ == "__main__":
    main()
