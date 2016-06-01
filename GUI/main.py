#If on Windows, to avoid fullscreen use the following two lines of code
#from kivy.config import Config
#Config.set('graphics', 'fullscreen', '0')

#------ Notes ------#
# Port Scan May Be Slow

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown

from urllib2 import Request, urlopen
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM

Builder.load_string('''
<TestsMenu>:

    Button:
        id: sqlbtn
        text: 'SQL Test'
        size_hint_y: None
        height: 50
        background_color: 0,.5,1,1

    Button:
        id: ftpbtn
        text: 'FTP Test'
        size_hint_y: None
        height: 50
        background_color: 0,.5,1,1

    Button:
        id: portbtn
        text: 'Port Scan'
        size_hint_y: None
        height: 50
        background_color: 0,.5,1,1

<TestSite>:

    TextInput:
        id: website
        pos: 0,root.top-50
        size: root.width-200,50

    Button:
        text: 'Tests'
        size: 200,50
        background_color: 0,.5,1,1
        pos: root.width-200, root.top-50
        on_release: root.menu.open(self)

    GridLayout:
        cols: 1
        pos: root.center

        Label:
            id: status
            text: "Test Websites for SQL Vunrabilities"
        Label:
            id: info
            text: ""

''')

class TestsMenu(DropDown):
    pass

class TestSite(Widget):

    menu = TestsMenu() #The dropdown menu for each test

    #This function checks for open ports

    def portScan(self, btn):
        try:
            url = self.ids.website.text
            url = url.replace("http://www.", "")
            url = url.split("/")

            sock = socket(AF_INET, SOCK_STREAM)

            self.ids.status.text = "Open Ports: "
            self.ids.status.color = (0, 1, 0, 1)

            for port in range(1, 1025):
                test = sock.connect_ex((url[0],port))

                #If port is open - port number is concatinated to string
                if test == 0:
                    s = str(port) + ", "
                    self.ids.status.text  += s

            sock.close()

        except:
            self.ids.status.text = "Error - No Port Scan available"
            self.ids.status.color = (1, 0, 0, 1)

    #This function tests port 21 for an open ftp port
    #If it is open an ftp attack is likely

    def ftpTest(self, btn):
        try:
            url = self.ids.website.text
            url = url.replace("http://www.", "")
            url = url.split("/")

            sock = socket(AF_INET, SOCK_STREAM)
            test = sock.connect_ex((url[0],21))

            if test == 0:
                self.ids.status.text  = "Port 21 is Open. Site May Be Vunerable to FTP Attacks"
                self.ids.status.color = (0, 1, 0, 1)

            else:
                self.ids.status.text  = "Port 21 is Close. Site Not Vunerable to FTP Attacks"
                self.ids.status.color = (1, 0, 0, 1)

            sock.close()

        except:
            self.ids.status.text  = "Unable to Test for FTP Attack"
            self.ids.status.color = (1, 0, 0, 1)

    #This tests a php webpage for any possibility of an SQL injection attack
    #If it is vunerable it will give the user the ip address of the website

    def sqlTest(self, btn):

        try:
            url = self.ids.website.text

            if "http://www." not in url:
                url.strip("www.") #if www. is at the beginning
                url = "http://www."+url

            req = Request(url+"?id=1'")

            response = urlopen(req)
            page = response.read()

            if ("Error" in page) and ("SQL" in page):
                self.ids.status.text = "Site May be Vunerable to SQL injection Attacks"
                self.ids.status.color = (0, 1, 0, 1)

                url = url.replace("http://www.", "")
                url = url.split("/")
                self.ids.info.text = "ip address: %s" %gethostbyname(url[0])

            else:
                self.ids.status.text = "No SQL Vunrabilities Detected"
                self.ids.status.color = (1, 0, 0, 1)

        except:
            self.ids.status.text = "Make sure the site is in the format: http://www.example.com/page.php"
            self.ids.status.color = (1, .5, 0, 1)

    #This will link the buttons from the dropdown menu to functions

    def bindButtons(self):

        def process(mes):
            self.ids.status.text = mes
            self.ids.info = ""
            self.ids.status.color = (1, .5, 0, 1)

        self.menu.ids.sqlbtn.bind(on_press=process("Testing For SQL Vunrabilities..."))
        self.menu.ids.ftpbtn.bind(on_press=process("Testing For FTP Vunrabilities..."))
        self.menu.ids.portbtn.bind(on_press=process("Scanning For Open Ports..."))

        self.menu.ids.sqlbtn.bind(on_release=self.sqlTest)
        self.menu.ids.ftpbtn.bind(on_release=self.ftpTest)
        self.menu.ids.portbtn.bind(on_release=self.portScan)

        if self.ids.website.text == "":
            self.ids.status.text = "Test Websites for SQL Vunrabilities"
            self.ids.status.color = (1,1,1,1)

class TestSiteApp(App):

    def build(self):
        testSite = TestSite()
        testSite.bindButtons()
        return testSite

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == "__main__":
    TestSiteApp().run()