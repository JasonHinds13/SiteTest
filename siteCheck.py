import sys
from urllib2 import Request, urlopen
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM

#This function checks for open ports
def portScan(url, limit):
    try:
        url = url.replace("http://www.", "")
        url = url.split("/")

        for port in range(1, limit+1):

            sock = socket(AF_INET, SOCK_STREAM)

            sock.settimeout(0.5)
            test = sock.connect_ex((url[0],port))

            if test == 0:
                print "[+] Port: %s" %port

            sock.close()
    except:
        print "[*] Error - No Port Scan available"

#This function tests for an open ftp port which makes it vunerable
def ftpTest(url):
    try:
        url = url.replace("http://www.", "")
        url = url.split("/")

        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.5)
        
        test = sock.connect_ex((url[0],21))

        if test == 0:
            print "[+] Port 21 is Open. Site May Be Vunerable to FTP Attacks"

        else:
            print "[+] Port 21 is Close. Site Not Vunerable to FTP Attacks"

        sock.close()

    except:
        print "[*] Unable to Test for FTP Attack"

#This tests a php webpage for any possibility of an SQL injection attack
def sqlTest(url):
    try:
        if "http://www." not in url:
            url.strip("www.") #if www. is at the beginning
            url = "http://www."+url

        req = Request(url+"?id=1'")

        response = urlopen(req)
        page = response.read()

        if ("Error" in page) and ("SQL" in page):
            print "[+] Site May be Vunerable to SQL injection Attacks"

            url = url.replace("http://www.", "")
            url = url.split("/")
            print "[+] ip address: %s" %gethostbyname(url[0])

        else:
            print "[+] No SQL Vunrabilities Detected"

    except:
        print "[-] Some Error Occured While Testing"
        print "[-] Make sure the site is in the format: http://www.example.com/page.php"

def help():
    print "[*] '-h' [For help]"
    print "[*] '-s' <name of site> [To check for sql injection attack]"
    print "[*] '-f' <name of site> [To check for ftp vunerability]"
    print "[*] '-p' <name of site> [To scan for open ports up to default]"
    print "[*] '-p' <name of site> -l <# of ports to check> [To scan for open ports up to specified]"

def main():
    try:
        if sys.argv[1] == '-s':
            sqlTest(sys.argv[2])

        elif sys.argv[1] == '-f':
            ftpTest(sys.argv[2])

        elif sys.argv[1] == '-p' and len(sys.argv) <=3:
            portScan(sys.argv[2], 1024)

        elif sys.argv[1] == '-p' and sys.argv[3] == '-l':
            portScan(sys.argv[2], int(sys.argv[4]))

        elif sys.argv[1] == '-h':
            help()

        print "" #leave some space

    except:
        print "[-] Error - Check Your Command"
        help()

if __name__ == "__main__":
    main()
