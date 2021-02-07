import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import threading
import time
from datetime import date
import calendar
import requests
import json
import qrcode
import geocoder
import urllib.parse

def genQR(master):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,
        border=4,
    )
    dictionary = {"u": master.username,"p":master.password,"amt":master.amount}
    json_object = json.dumps(dictionary, indent = 4)   
    qr.add_data(json_object)
    qr.make(fit=True)
    master.qr_img = qr.make_image(fill_color="black", back_color="white")
    master.qr_img.save("QR.png")

def mapRequest(master):
    g = geocoder.ip('me')
    centerSearch = str(g.latlng[0]) + "," + str(g.latlng[1])
    center = "\"" + str(g.latlng[0]) + "," + str(g.latlng[1]) + "\""
    zoom = 12
    size = "400x400"
    key = "AIzaSyC1YvHmJqbzSCpLIJ9dJz-CP5SKnxxeqm4"
    findATM = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=ATM&inputtype=textquery&fields=formatted_address&locationbias=circle:8000@" + centerSearch + "&key=" + key
    response = requests.get(findATM)
    markers = "color:blue%7Clabel:S%7C " + response.json()['candidates'][0]['formatted_address']
    response = requests.get("https://maps.googleapis.com/maps/api/staticmap?center=" + center + "&zoom=" + str(zoom) + "&size=" + size + "&markers=" + markers + "&key=" + key)
    if response.status_code == 200:
        with open("./map.jpg", 'wb') as f:
            f.write(response.content)



class ATM(Tk):
    def __init__(self):
        Tk.__init__(self)
        #self.resizable(False,False)
        self.initImage()
        self.frame = None #Frame shown in window
        self.geometry("450x800")
        self.title("NCR ATMPal")
        self.switch_frame(frameWelcome)
        self.username = ""
        self.password = ""
        self.amount = 0
        self.qr_img = None
    #Switches frame on window
    def switch_frame(self, frameClass):
        newFrame = frameClass(self)
        if self.frame is not None:
            self.frame.pack_forget()
            x = threading.Thread(target=self.frame.destroy, args=())
        self.frame = newFrame
        self.frame.pack(fill=BOTH, expand=True)
    def initImage(self):
        login = Image.open("resources/login.png")
        login = login.resize((250, 60), Image.ANTIALIAS) ## The (250, 250) is (height, width
        im_login = ImageTk.PhotoImage(login)
        self.login_img = im_login
        submit = Image.open("resources/submit.png")
        submit = submit.resize((250, 60), Image.ANTIALIAS) ## The (250, 250) is (height, width
        im_submit = ImageTk.PhotoImage(submit)
        self.submit_img = im_submit

class frameWelcome(Frame):
    def __init__(self, master):
        Frame.__init__(self,master,bg="white")
        Label(self,text="   ", width=300, bg="#51B948",font=('arial', '26', 'bold')).pack()
        Message(self, text="Access your money securely and safely.",width = 250, font=('arial', '30', 'bold'),fg="black",bg="white").pack(pady=100)
        Button(self, image=master.login_img,command=lambda:master.switch_frame(frameLogin),font=('arial', '12'),borderwidth=0,activebackground="white",bg='white').pack(pady=100)

# Frame home
class frameHome(Frame):
    def __init__(self, master):
        Frame.__init__(self,master,bg="white")
        Label(self,text="   ", width=300, bg="#51B948",font=('arial', '26', 'bold')).pack()
        hello = Label(self, text="Hello " + master.username + ".", width=50,font=('arial', '24', 'bold'),bg="white")
        hello.config(anchor=CENTER)
        hello.pack(pady=50)
        Button(self, text="InstaCash",command=lambda:master.switch_frame(frameMap),font=('arial', '12')).pack()
       # Label(self,text="")


# Frame for selecting action to perform at the ATM
class frameMap(Frame):
    def __init__(self,master):
        Frame.__init__(self,master,bg="white")
        prompt = Message(self, text="Search for ATMs", font=('arial', '12', 'bold'),width=200).grid(row=0, column=0)
        search_map = Entry(self,width=30).grid(row=0,column=1)
        Button(self, text="Select ATM",command=lambda:master.switch_frame(frameATMAction),font=('arial', '12')).grid(row=2,column=1)
        self.initMap(master)
        Label(self,image=master.map).grid()
    def initMap(self,master):
        mapRequest(master)
        login = Image.open("map.jpg")
        login = login.resize((400,400), Image.ANTIALIAS) ## The (250, 250) is (height, width
        im_login = ImageTk.PhotoImage(login)
        master.map = im_login

class frameATMAction(Frame):
    def __init__(self, master):
        Frame.__init__(self,master,bg="white")
        Button(self, text="Back", command=lambda:master.switch_frame(frameMap),font=('arial', '12')).grid(row=0,column=0)
        Message(self, text="Select your ATM action below.",width = 350, font=('arial', '18', 'bold')).grid(row=0,column=1)
        Button(self, text="Deposit",command=lambda:master.switch_frame(frameDepositAction),font=('arial', '12')).grid(row=1,column=1)
        Button(self, text="Withdraw",command=lambda:master.switch_frame(frameWithdrawAction),font=('arial', '12')).grid(row=2,column=1)

class frameDepositAction(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        Button(self, text="Back", command=lambda:master.switch_frame(frameATMAction),font=('helvetica', '12')).grid()
        Message(self, text="Enter the amount you would like to deposit.",width = 350, font=('helvetica', '18', 'bold')).grid(row=1,column=1)
        deposit_amount = Entry(self,width=30)
        deposit_amount.grid(row=2,column=1)
        Button(self, text="Submit", command=lambda:self.setAmount(master,deposit_amount)).grid(row=3,column=1)
    def setAmount(self,master,entry):
        master.amount = entry.get()
        master.switch_frame(frameQR)

class frameQR(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.initQR(master)
        Button(self, text="Cancel Transaction", command=lambda:master.switch_frame(frameATMAction),font=('helvetica', '12')).grid(row=0,column=0)
        Message(self, text="Please scan this QR code at the ATM you have selected.",width=200,font=('helvetica', '18', 'bold')).grid(row=1,column=1)
        Label(self,image=master.qr_img).grid()
    def initQR(self,master):
        genQR(master)
        master.qr_img = Image.open("QR.png")
        master.qr_img = master.qr_img.resize((400,400),Image.ANTIALIAS)
        master.qr_img = ImageTk.PhotoImage(master.qr_img)

class frameWithdrawAction(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        Button(self, text="Back", command=lambda:master.switch_frame(frameATMAction),font=('helvetica', '12')).grid()
        Message(self, text="Enter the amount you would like to withdraw.",width = 350, font=('helvetica', '18', 'bold')).grid(row=1,column=1)
        withdraw_amount = Entry(self,width=30)
        withdraw_amount.grid(row=2,column=1)
        Button(self, text="Submit", command=lambda:self.setAmount(master,withdraw_amount)).grid(row=3,column=1)
    def setAmount(self,master,entry):
        master.amount = str(int(entry.get())*-1)
        master.switch_frame(frameQR)


class frameLogin(Frame):
    def __init__(self,master):
        Frame.__init__(self,master,bg="white")
        Label(self,text="   ", width=300, bg="#51B948",font=('arial', '26', 'bold')).pack()
        Message(self, text="Welcome",width = 350,  font=('arial', '30', 'bold'),bg="white").pack(pady=50)
        Label(self,text="Username",pady=10, font=('arial', '18', 'bold'),bg="white").pack(pady=2)
        userInput = Entry(self,width=50)
        userInput.pack()
        Label(self,text="Password",pady=10, font=('arial', '18', 'bold'),bg="white").pack(pady=2)
        passInput = Entry(self,width=50,show='*')
        passInput.pack()
        Button(self, image=master.submit_img,command=lambda:self.saveAndSwitch(master,userInput,passInput),font=('arial', '12'),borderwidth=0,activebackground="white",bg='white').pack(pady=10)
        Button(self,text="Back", borderwidth=0, activebackground="white",command=lambda:master.switch_frame(frameWelcome),bg="white",font=('arial', '12')).pack()
        self.invalid_login = Label(self,text="Invalid Login Information", font=('arial', '12', 'bold'))

    def saveAndSwitch(self,master,user,password):
        master.username = user.get()
        master.password = password.get()
        master.switch_frame(frameHome)

 #:) starting the app
if __name__ == "__main__":
    app = ATM()
    app.mainloop(0)