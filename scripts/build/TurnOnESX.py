from pyvim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from Tkinter import *
import argparse
import os
import socket
import ssl
import sys

socket.setdefaulttimeout(3)

def Prompt(mayuser=""):

    global usr
    global pwdr
    root = Tk()
    pwdbox = Entry(root , show = '*')
    usrbox = Entry(root , textvariable = StringVar(root , value = mayuser))

    def Collect(evt):
        
        global usr
        global pwdr

        usr = usrbox.get()
        pwdr = pwdbox.get()

        root.destroy()

    Label(root , text= "Username").pack(side = "top")
    usrbox.pack(side="top")
    Label(root , text= "Password").pack(side = "top")
    pwdbox.pack(side="top")

    if mayuser:
        
        pwdbox.focus_set()

    else:

        usrbox.focus_set()

    pwdbox.bind('<Return>', Collect)

    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)

    iconfile = 'VM-Icon.ico'

    root.iconbitmap(default=os.path.join(application_path, iconfile))

    root.title("Enter Crednetials")

    root.geometry("300x100")

    root.mainloop()

    return usr,pwdr

def TurnOnMachinesInFolder(folder):

    VMlist = ""

    Child = folder.childEntity

    for ent in Child:

        if "VirtualMachine" in str(type(ent)):
            ent.PowerOn()
            VMlist = VMlist + ent.name + "\n"

        if "Folder" in str(type(ent)):
            VMlist = VMlist + TurnOnMachinesInFolder(ent)

    return VMlist


parser = argparse.ArgumentParser()

parser.add_argument('-u' , action = "store")
parser.add_argument('-p' , action = "store")
parser.add_argument('-s' , action = "store")

if parser.parse_args().u:

    if parser.parse_args().p:

        usr,pwdr = parser.parse_args().u,parser.parse_args().p

    else:

        usr,pwdr = Prompt(parser.parse_args().u)

else:

    usr,pwdr = Prompt()

USER = usr
PASSWORD = pwdr
FOLDER = usr + "_turnon_folder"
SERVER="X.X.X.X"
PORT=443

if "\\" in FOLDER:

    FOLDER = FOLDER.split("\\")[1]

if parser.parse_args().s:

    SERVER = parser.parse_args().s

roots = Tk()

try:

   Client = SmartConnect(host=SERVER,user=USER,pwd=PASSWORD,port=PORT,sslContext=ssl._create_unverified_context())

except:

    roots.title("Error connecting")

    roots.geometry("300x100")

    Label(roots , text= "Couldn't connect to server").pack(side = "top")

    Label(roots , text= "Please verify credentials and connectivity").pack(side = "top")

    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)

    iconfile = 'VM-Icon.ico'

    roots.iconbitmap(default=os.path.join(application_path, iconfile))

    roots.mainloop()

    sys.exit()

content = Client.content

container = content.viewManager.CreateContainerView( content.rootFolder, [vim.Folder] , True)

for folder in container.view:
    if folder.name == FOLDER:
        LIST = TurnOnMachinesInFolder(folder)
        roots.title("Turned on machines:")
        roots.geometry("300x300")
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        elif __file__:
            application_path = os.path.dirname(__file__)

        iconfile = 'VM-Icon.ico'

        roots.iconbitmap(default=os.path.join(application_path, iconfile))

        Label(roots , text = LIST).pack(side = "top")
        roots.mainloop()
        sys.exit()
