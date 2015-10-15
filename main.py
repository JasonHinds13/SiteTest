from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from urllib2 import Request, urlopen
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM

Builder.load_string('''
<TestSite>:
    t_ftp: ftp
    t_addr: addr
    t_status: status
    t_website: website
    
    GridLayout:
        cols: 2
        width: 500
        height: 50
        pos: root.a_width-500, root.a_height -50
        
        TextInput:
            id: website
        Button:
            text: 'Test'
            on_press: root.test()
    
    Label:
        id: status
        pos: (root.a_width-50)/2, (root.a_height)/2
        text: 'Test Websites for SQL Vunrabilities'
        
    GridLayout:
        cols: 1
        pos: (root.a_width-50)/2, (root.a_height-100)/2
        
        Label:
            id: addr
            text: ""
        Label:
            id: ftp
            text: ""

''')

class TestSite(Widget):

    a_width = Window.width
    a_height = Window.height
    
    t_ftp = ObjectProperty(None)
    t_addr = ObjectProperty(None)
    t_status = ObjectProperty(None)
    t_website = ObjectProperty(None)

    #This function tests port 21 for an open ftp port
    #If it is open an ftp attack is likely
    def ftest(self):
        try:
            url = self.t_website.text
            url = url.replace("http://www.", "")
            url = url.split("/")
            
            sock = socket(AF_INET, SOCK_STREAM)
            test = sock.connect_ex((url[0],21))
            
            if test == 0:
                self.t_ftp.text  = "Port 21 is Open. Site May Be Vunerable to FTP Attacks"
                self.t_ftp.color = (0, 1, 0, 1)
                
            else:
                self.t_ftp.text  = "Port 21 is Close. Site Not Vunerable to FTP Attacks"
                self.t_ftp.color = (0, 1, 0, 1)
                    
            sock.close()
            
        except:
            self.t_ftp.text  = "Unable to Test for FTP Attack"
            self.t_ftp.color = (1, 0, 0, 1)

    #This tests a php webpage for any possibility of an SQL injection attack
    #If it is vunerable it will give the user the ip address of the website
    def stest(self):
        
        try:
            url = self.t_website.text
            req = Request(url+"?id=1'")

            response = urlopen(req)
            page = response.read()

            if ("Error" in page) and ("SQL" in page):
                self.t_status.text = "Site May be Vunerable to SQL injection Attacks"
                self.t_status.color = (0, 1, 0, 1)
                
                url = url.replace("http://www.", "")
                url = url.split("/")
                self.t_addr.text = "ip address: %s" %gethostbyname(url[0])

            else:
                self.t_status.text = "No SQL Vunrabilities Detected"
                self.t_status.color = (1, 0, 0, 1)
                
        except:
            self.t_status.text = """
            Make sure the site is in the format:
              http://www.example.com/page.php
            If you are testing for an SQL Vunrability
            
            (Also Check Your Internet Connection)"""
            self.t_status.color = (1, .5, 0, 1)

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