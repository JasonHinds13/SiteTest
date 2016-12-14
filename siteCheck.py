
import sys
from urllib2 import Request, urlopen
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM

#This function checks for open ports
def portScan(url, limit):
    try:
        print "[*] Attempting To Scan %s Ports on %s..." %(limit,url)

        url = url.replace("http://www.", "")
        url = url.split("/")

        for port in range(1, limit+1):

            sock = socket(AF_INET, SOCK_STREAM)

            sock.settimeout(0.5)
            test = sock.connect_ex((url[0],port))

            sys.stdout.write("\rScanning Port: %s" %port)
            sys.stdout.flush()

            if test == 0:
                print "\n[+] Port: %s" %port

            sock.close()
        print "\n[*] Finished Scanning %s Ports" %limit
    except:
        print "\n[*] Error - No Port Scan available"

#This function tests for an open ftp port which makes it vunerable
def ftpTest(url):
    try:
        print "[*] Attempting To Test For FTP Vulnerability on %s..." %url

        url = url.replace("http://www.", "")
        url = url.split("/")

        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.5)

        test = sock.connect_ex((url[0],21))

        if test == 0:
            print "[+] Port 21 is Open. Site May Be Vulnerable to FTP Attacks"

        else:
            print "[+] Port 21 is Close. Site Not Vulnerable to FTP Attacks"

        sock.close()

    except:
        print "[*] Unable to Test for FTP Attack"

#This tests a php webpage for any possibility of an SQL injection attack
def sqlTest(url):
    try:
        print "[*] Attempting To Test For SQL Vunerability on %s..." %url

        if "http://www." not in url:
            url.strip("www.") #if www. is at the beginning
            url = "http://www."+url

        req = Request(url+"?id=1'")

        response = urlopen(req)
        page = response.read()

        if ("Error" in page) and ("SQL" in page):
            print "[+] Site May be Vulnerable to SQL injection Attacks"

            url = url.replace("http://www.", "")
            url = url.split("/")
            print "[+] ip address: %s" %gethostbyname(url[0])

        else:
            print "[+] No SQL Vulnerabilities Detected"

    except:
        print "[-] Some Error Occured While Testing"
        print "[-] Make sure the site is in the format: http://www.example.com/page.php"

def help():
    print "[*] '-h' or '--help' [For help]"
    print "[*] '-s' <name of site> [To check for sql injection attack]"
    print "[*] '-f' <name of site> [To check for ftp vulnerability]"
    print "[*] '-p' <name of site> [To scan for open ports up to default]"
    print "[*] '-p' <name of site> -l <# of ports to check> [To scan for open ports up to specified]"

def main():

    if len(sys.argv) < 2:
        print "[*] No System Arguments Supplied\n"
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
        print "[-] Error - Check Your Command"
        help()

    print "" #leave some space

if __name__ == "__main__":
    main()
