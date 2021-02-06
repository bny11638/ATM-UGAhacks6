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



class ATM(Tk):
    def __init__(self):
        Tk.__init__(self)
        #self.resizable(False,False)
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

#Welcome Screen DESIGN IS FOR MATTHEW
class frameWelcome(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        Message(self, text="Access your money securely & safely.",width = 350, font=('helvetica', '18', 'bold')).pack()
        Button(self, text="Bank Login",command=lambda:master.switch_frame(frameLogin),font=('helvetica', '12')).pack(pady=10)
        Button(self, text="Register",font=('helvetica', '12')).pack(pady=10)

# Frame for selecting action to perform at the ATM
class frameMap(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        prompt = Message(self, text="Search for ATMs", font=('helvetica', '12', 'bold'),width=200).grid(row=0, column=0)
        search_map = Entry(self,width=30).grid(row=0,column=1)
        Button(self, text="Select ATM",command=lambda:master.switch_frame(frameATMAction),font=('helvetica', '12')).grid(row=2,column=1)

class frameATMAction(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        Button(self, text="Back", command=lambda:master.switch_frame(frameMap),font=('helvetica', '12')).grid(row=0,column=0)
        Message(self, text="Select your ATM action below.",width = 350, font=('helvetica', '18', 'bold')).grid(row=0,column=1)
        Button(self, text="Deposit",command=lambda:master.switch_frame(frameDepositAction),font=('helvetica', '12')).grid(row=1,column=1)
        Button(self, text="Withdraw",command=lambda:master.switch_frame(frameWithdrawAction),font=('helvetica', '12')).grid(row=2,column=1)

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
        Frame.__init__(self,master)
        Message(self, text="Welcome Back!",width = 350,  font=('helvetica', '18', 'bold')).pack()
        Label(self,text="Username",pady=10, font=('helvetica', '12', 'bold')).pack(pady=2)
        userInput = Entry(self,width=30)
        userInput.pack()
        Label(self,text="Password",pady=10, font=('helvetica', '12', 'bold')).pack(pady=2)
        passInput = Entry(self,width=30,show='*')
        passInput.pack()
        Button(self, text="Submit",command=lambda:self.saveAndSwitch(master,userInput,passInput),font=('helvetica', '12')).pack(pady=10)
        Button(self,text="Back", borderwidth=0, activebackground="#6B081F",command=lambda:master.switch_frame(frameWelcome)).pack()
        self.invalid_login = Label(self,text="Invalid Login Information", font=('helvetica', '12', 'bold'))

    def saveAndSwitch(self,master,user,password):
        master.username = user.get()
        master.password = password.get()
        master.switch_frame(frameMap)

 #:) starting the app
if __name__ == "__main__":
    app = ATM()
    app.mainloop(0)