# About SiteTest
Application written in Python.
The GUI uses the Kivy open source library that tests websites for vunerabilities. 
This was written using python 2.7

# Current Features
* Potential for SQL Injection Attack Test
* Potential for FTP Attack Test 
* Port Scanner

# Use
* To view the help menu <code>python siteCheck.py -h</code>
* To test for SQL vunerability <code>python siteCheck.py -s http://www.example.com/page.php</code>
* To test for FTP vunerability <code>python siteCheck.py -f http://www.example.com</code>
* To run a port scan <code>python siteCheck.py -p http://www.example.com</code>
* To run a port scan and specify how many to scan <code>python siteCheck.py -p http://www.example.com -l 1025</code>

# Issues
