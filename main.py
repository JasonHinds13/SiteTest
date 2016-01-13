#If on Windows to avoid fullscreen, use the following two lines of code
#from kivy.config import Config
#Config.set('graphics', 'fullscreen', '0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget

from urllib2 import Request, urlopen
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM

Builder.load_string('''
<TestSite>:
    
    TextInput:
        id: website
        pos: 0,root.top-50
        size: root.width-200,50
    Button:
        text: 'Test'
        size: 200,50
        background_color: 0,.5,1,1
        pos: root.width-200, root.top-50
        on_press:
            status.text = "Testing For Vunrabilities..."
            status.color = (1, .5, 0, 1)
        
        on_release: root.test()
        
    GridLayout:
        cols: 1
        pos: root.center

        Label:
            id: status
            text: "Test Websites for SQL Vunrabilities"
        
        Label:
            id: addr
            text: ""
        Label:
            id: ftp
            text: ""

''')

class TestSite(Widget):

    #This function tests port 21 for an open ftp port
    #If it is open an ftp attack is likely
    
    def ftest(self):
        try:
            url = self.ids.website.text
            url = url.replace("http://www.", "")
            url = url.split("/")
            
            sock = socket(AF_INET, SOCK_STREAM)
            test = sock.connect_ex((url[0],21))
            
            if test == 0:
                self.ids.ftp.text  = "Port 21 is Open. Site May Be Vunerable to FTP Attacks"
                self.ids.ftp.color = (0, 1, 0, 1)
                
            else:
                self.ids.ftp.text  = "Port 21 is Close. Site Not Vunerable to FTP Attacks"
                self.ids.ftp.color = (1, 0, 0, 1)
                    
            sock.close()
            
        except:
            self.ids.ftp.text  = "Unable to Test for FTP Attack"
            self.ids.ftp.color = (1, 0, 0, 1)

    #This tests a php webpage for any possibility of an SQL injection attack
    #If it is vunerable it will give the user the ip address of the website
            
    def stest(self):
        
        try:
            url = self.ids.website.text
            req = Request(url+"?id=1'")

            response = urlopen(req)
            page = response.read()

            if ("Error" in page) and ("SQL" in page):
                self.ids.status.text = "Site May be Vunerable to SQL injection Attacks"
                self.ids.status.color = (0, 1, 0, 1)
                
                url = url.replace("http://www.", "")
                url = url.split("/")
                self.ids.addr.text = "ip address: %s" %gethostbyname(url[0])

            else:
                self.ids.addr.text = ""
                self.ids.status.text = "No SQL Vunrabilities Detected"
                self.ids.status.color = (1, 0, 0, 1)
                
        except:
            self.ids.status.text = """
            Make sure the site is in the format:
               http://www.example.com/page.php
            If you are testing for an SQL Vunrability
            
            (Also Check Your Internet Connection)"""
            self.ids.status.color = (1, .5, 0, 1)

    #This will call both test functions when the 'Test' button is pressed
            
    def test(self):
        self.stest()
        self.ftest()
    
class TestSiteApp(App):
    
    def build(self):
        return TestSite()
        
    def on_pause(self):
        return True
        
    def on_resume(self):
        pass
        
if __name__ == "__main__":
    TestSiteApp().run()
