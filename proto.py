import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import threading
import time
from datetime import date
import calendar
import requests
import json

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
        Message(self, text="Protecting what matters.",width = 350, font=('helvetica', '18', 'bold')).pack()
        Button(self, text="Bank Login",command=lambda:master.switch_frame(frameLogin),font=('helvetica', '12')).pack(pady=10)
        Button(self, text="Register",font=('helvetica', '12')).pack(pady=10)

# Frame for selecting action to perform at the ATM
class frameATMAction(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        Message(self, text="Select your ATM action below.",width = 350, font=('helvetica', '18', 'bold')).pack()
        Button(self, text="Deposit",command=lambda:master.switch_frame(frameDepositAction),font=('helvetica', '12')).pack(pady=10)
        Button(self, text="Withdraw",command=lambda:master.switch_frame(frameWithdrawAction),font=('helvetica', '12')).pack(pady=10)

class frameDepositAction(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        Button(self, text="Test", command=print(master.username)).grid()
        Button(self, text="Back", command=lambda:master.switch_frame(frameATMAction),font=('helvetica', '12')).grid()
        Message(self, text="Enter the amount you would like to deposit.",width = 350, font=('helvetica', '18', 'bold')).grid(row=1,column=1)
        depositAmount = Entry(self,width=30)
        depositAmount.grid(row=2,column=1)


class frameWithdrawAction(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        Message(self, text="Enter the amount you would like to withdraw.",width = 350, font=('helvetica', '18', 'bold')).pack()

class frameLogin(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Message(self, text="Protecting what matters.",width = 350,  font=('helvetica', '18', 'bold')).pack()
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
        master.switch_frame(frameATMAction)

 #:) starting the app
if __name__ == "__main__":
    app = ATM()
    app.mainloop(0)