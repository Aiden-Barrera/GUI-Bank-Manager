import customtkinter as ctk
from PIL import Image
import calendar
from datetime import datetime
import banking
from Checkings import Checking
from Savings import Savings


class BankingGUI:
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.accountList = []
        self.checkAccountCreated = False
        self.savingsAccountCreated = False
        self.account = ""
        self.userID = ""
        self.password = ""
        self.F_Name = ""
        self.L_Name = ""
        self.birthday = ""
        self.checkBalance = float(0)
        self.savingBalance = float(0)
        
        self.root = ctk.CTk()
        self.root.geometry("870x810")
        
        self.logInScreen()
        
        self.root.mainloop()
        
    def logInScreen(self):
        self.loginFrame = ctk.CTkFrame(master=self.root, border_width=1, corner_radius=8, border_color="#5b5f61")
        self.loginFrame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        self.leftSideFrame = ctk.CTkFrame(master=self.loginFrame, corner_radius=8, fg_color="transparent")
        self.leftSideFrame.grid(row=0, column=0, padx=28, pady=10)
        
        self.rightSideImg = ctk.CTkImage(light_image=Image.open("images/clouds.jpg"), dark_image=Image.open("images/clouds.jpg"), size=(340,390))
        self.rightSideFrame = ctk.CTkFrame(master=self.loginFrame)
        self.rightSideFrame.grid(row=0, column=1, sticky="news")

        self.rightSideImgLabel = ctk.CTkLabel(master=self.rightSideFrame, text="", image=self.rightSideImg)
        self.rightSideImgLabel.grid(row=0, column=0, pady=1, padx=(0,1), sticky="news")
        
        self.bankNameLabel = ctk.CTkLabel(master=self.leftSideFrame, text="Cloud Banking", justify=ctk.CENTER, font=("Copperplate Gothic Bold", 36), text_color="#50C878")
        self.bankNameLabel.grid(row=0, column=0, pady=10, padx=10)
        
        self.introLabel = ctk.CTkLabel(master=self.leftSideFrame, text="Welcome Back to Cloud Banking", justify=ctk.CENTER, font=("Arial", 18))
        self.introLabel.grid(row=1,column=0, pady=(0,20))
        
        self.userID_Entry = ctk.CTkEntry(master=self.leftSideFrame, placeholder_text="User ID", width=220)
        self.userID_Entry.grid(row=2, column=0, pady=(10,30), padx=10)
        
        self.userPassword_Frame = ctk.CTkFrame(self.leftSideFrame, fg_color="transparent")
        self.userPassword_Frame.grid(row=3, column=0)
        
        self.userPassword_Entry = ctk.CTkEntry(master=self.userPassword_Frame, placeholder_text="Password", show="*", width=220)
        self.userPassword_Entry.grid(row=0, column=0, padx=(29,10), pady=(0,5))
        
        self.showPassEyeReg = ctk.CTkImage(light_image=Image.open('images/hide.png'), dark_image=Image.open('images/hide.png'), size=(18,15))
        self.showPassEyeSolid = ctk.CTkImage(light_image=Image.open('images/visible.png'), dark_image=Image.open('images/visible.png'), size=(18,15))
        
        self.showImg_Label = ctk.CTkLabel(master=self.userPassword_Frame, text="",image=self.showPassEyeReg)
        self.showImg_Label.grid(row=0, column=1, sticky="news", pady=(0,5))
        
        self.showImg_Label.bind('<Button-1>', self.showPass)
        
        self.errorMessageLabel = ctk.CTkLabel(master=self.leftSideFrame, text="", text_color="red")
        self.errorMessageLabel.grid(row=4, column=0, sticky="ew")
        
        self.submitBtn = ctk.CTkButton(master=self.leftSideFrame, text="Log In", corner_radius=11, hover_color="#3c825b", width=220,command=self.btnPressed)
        self.submitBtn.grid(row=5,column=0)
        
        self.dashLabel = ctk.CTkLabel(master=self.leftSideFrame, text="_________________________", text_color="#5b5f61", font=("Arial", 14, "bold"))
        self.dashLabel.grid(row=6,column=0, sticky="ew")
        
        self.newAccountBtn = ctk.CTkButton(master=self.leftSideFrame, text="Create new account", corner_radius=11, fg_color="#62acd1", hover_color="#448eb3", width=170,command=self.transitionToNewAccountScreen)
        self.newAccountBtn.grid(row=7, column=0, pady=10,)
        
        
    def showPass(self, event):
        if self.showImg_Label._image == self.showPassEyeReg:
            self.showImg_Label.configure(image=self.showPassEyeSolid)
            self.userPassword_Entry.configure(show="")
        else:
            self.showImg_Label.configure(image=self.showPassEyeReg)
            self.userPassword_Entry.configure(show="*")
            
    def btnPressed(self):
        if self.forgotUserOrPass():
            return
        
        self.userID = self.userID_Entry.get()
        self.password = self.userPassword_Entry.get()
        
        if banking.SearchThroughList(self.accountList, self.userID):
            if banking.checkPassword(self.accountList, self.userID, self.password):
                self.account = banking.SearchThroughListAndReturn(self.accountList, self.userID)
                self.transitionToAccountScreen()
                self.setUpChecking()
                self.setUpSavings()
            else:
                self.clearEntry(signIn=False)
                self.errorMessageLabel.configure(text="Invalid Password")
                return
        else:
            self.clearEntry(signIn=False)
            self.errorMessageLabel.configure(text="Invalid User ID")
            return
        
        
    def forgotUserOrPass(self, signUp=False) -> bool:
        if self.userID_Entry.get() == "" or self.userPassword_Entry.get() == "":
            self.errorMessageLabel.configure(text="Forgot UserID or Password")
            if signUp:
                self.clearEntry(True)
            else:
                self.clearEntry()
            return True
        return False
    
    def setUpChecking(self):
        if self.account.checkings == None:
            self.errorMessageLabel.configure(text="")
            self.account.setChecking(checkings=Checking(self.userID), accountType=Checking())
            self.checkAccountCreated = True
            print(banking.printList(self.accountList))
        else: 
            self.account.setAccountType(accountType=Checking())
        
        self.setUpCheckingBtn.grid_forget()
        self.checkBalanceFrame = ctk.CTkFrame(master=self.accountTypeFrame)
        self.checkBalanceFrame.grid(row=0, column=1, sticky="e")
        
        self.showCheckBalanceLabel = ctk.CTkLabel(master=self.checkBalanceFrame, text=f"${self.account.getBalance()}", font=('Arial Rounded MT Bold', 20), text_color="white")
        self.showCheckBalanceLabel.grid(row=0, column=0, sticky="w", padx=(0,5))
        
        self.showMoreCheckingImg = ctk.CTkImage(light_image=Image.open("images/arrow-right-solid.png"), dark_image=Image.open("images/arrow-right-solid.png")) 
        self.showMoreCheckingLabel = ctk.CTkLabel(master=self.checkBalanceFrame, text="", image=self.showMoreCheckingImg)
        self.showMoreCheckingLabel.grid(row=0, column=1, sticky="e", padx=(5,20))
        
        self.showMoreCheckingLabel.bind("<Button-1>", lambda event: self.transactionHistoryWindow(event, flag=True))
        
    def setUpSavings(self):
        if self.account.savings == None:
            self.account.setSavings(savings=Savings(self.userID), accountType=Savings())
            self.savingsAccountCreated = True
            print(banking.printList(self.accountList))
        else:
            self.account.setAccountType(accountType=Savings())
            
        self.setUpSavingsBtn.grid_forget()
        self.savingBalance = self.account.getBalance()
        self.savingsBalanceFrame = ctk.CTkFrame(master=self.accountTypeFrame)
        self.savingsBalanceFrame.grid(row=2, column=1, sticky="e")
        
        self.showSavingsBalanceLabel = ctk.CTkLabel(master=self.savingsBalanceFrame, text=f"${self.savingBalance}", font=('Arial Rounded MT Bold', 20), text_color="white")
        self.showSavingsBalanceLabel.grid(row=0, column=0, sticky="w", padx=(0,5))
        
        self.showMoreSavingsImg = ctk.CTkImage(light_image=Image.open("images/arrow-right-solid(1).png"), dark_image=Image.open("images/arrow-right-solid(1).png")) 
        self.showMoreSavingsLabel = ctk.CTkLabel(master=self.savingsBalanceFrame, text="", image=self.showMoreSavingsImg)
        self.showMoreSavingsLabel.grid(row=0, column=1, sticky="e", padx=(5,20))
        
        self.showMoreSavingsLabel.bind("<Button-1>", lambda event: self.transactionHistoryWindow(event, flag=False))
        
    # If flag = False then it's Savings else Checkings
    def depoChecking(self, flag: bool):
        if not flag:
            if not self.savingsAccountCreated:
                self.errorMessageLabel.configure(text="No Savings Account Created")
                return
            self.account.setAccountType(accountType=Savings())
        else:
            if not self.checkAccountCreated:
                self.errorMessageLabel.configure(text="No Checking Account Created")
                return
            self.account.setAccountType(accountType=Checking())
            
        self.depoCheckingtopLevel = ctk.CTkToplevel(self.root)
        self.depoCheckingtopLevel.title("Deposit")
        self.depoCheckingtopLevel.geometry("400x400")
        
        self.depoCheckingMainFrame = ctk.CTkFrame(master=self.depoCheckingtopLevel, corner_radius=4, border_width=1, border_color="#5b5f61")
        self.depoCheckingMainFrame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        self.depoCheckingEntry = ctk.CTkEntry(master=self.depoCheckingMainFrame, fg_color="transparent", border_width=0,font=('Arial Rounded MT Bold', 24), text_color="white", justify="center")
        self.depoCheckingEntry.insert(0, "$0")
        self.depoCheckingEntry.icursor(1)
        self.depoCheckingEntry.pack(padx=20, pady=(25, 15), fill="both")
        
        self.errorMessageLabelTopLevel = ctk.CTkLabel(master=self.depoCheckingMainFrame, text="", text_color="red")
        self.errorMessageLabelTopLevel.pack(padx=10, fill="both")
        
        self.confirmVar = ctk.IntVar()
        self.depoCheckingConfirmCheckBox = ctk.CTkCheckBox(master=self.depoCheckingMainFrame, text="Agree to Deposit", font=('Arial Rounded MT Bold', 10), border_color="#5b5f61", border_width=2, checkbox_height=15, checkbox_width=15 ,variable=self.confirmVar, onvalue=1, offvalue=0)
        self.depoCheckingConfirmCheckBox.pack(pady=(0,10), padx=10)
        
        self.depoBtn = ctk.CTkButton(master=self.depoCheckingMainFrame, text="Deposit", corner_radius=4, width=70, height=30, hover_color="#3c825b", border_color="white", border_width=1, command=lambda: self.depoMoneyToChecking(flag))
        self.depoBtn.pack(padx=20, pady=(0, 20), fill="both")
        
    def depoMoneyToChecking(self, flag:bool):
        if self.confirmVar.get() == 0:
            self.errorMessageLabelTopLevel.configure(text="Didn't Agree to Terms")
            return
        if not banking.is_float(self.depoCheckingEntry.get()[1:]):    
            self.errorMessageLabelTopLevel.configure(text="Invalid Amount")
            return
        else:
            if not flag:
                if self.depoCheckingEntry.get().startswith("$"):
                    self.account.setBalance(float(self.depoCheckingEntry.get()[1:]))
                    self.showSavingsBalanceLabel.configure(text=f"${self.account.getBalance()}")
                else:
                    self.account.setBalance(float(self.depoCheckingEntry.get()[0:]))
                    self.showSavingsBalanceLabel.configure(text=f"${self.account.getBalance()}")
            else:
                if self.depoCheckingEntry.get().startswith("$"):
                    self.account.setBalance(float(self.depoCheckingEntry.get()[1:]))
                    self.showCheckBalanceLabel.configure(text=f"${self.account.getBalance()}")
                else:
                    self.account.setBalance(float(self.depoCheckingEntry.get()[0:]))
                    self.showCheckBalanceLabel.configure(text=f"${self.account.getBalance()}")
            
        self.depoCheckingtopLevel.destroy()
        
    # If flag = false then it's savings else checkings
    def withDraw(self, flag: bool):
        if not flag:
            if not self.savingsAccountCreated:
                self.errorMessageLabel.configure(text="No Savings Account Created")
                return
            self.account.setAccountType(accountType=Savings())
        else:
            if not self.checkAccountCreated:
                self.errorMessageLabel.configure(text="No Checking Account Created")
                return
            self.account.setAccountType(accountType=Checking())
            
        self.withdrawtopLevel = ctk.CTkToplevel(self.root)
        self.withdrawtopLevel.title("Savings")
        self.withdrawtopLevel.geometry("400x400")
        
        self.withdrawMainFrame = ctk.CTkFrame(master=self.withdrawtopLevel, corner_radius=4, border_width=1, border_color="#5b5f61")
        self.withdrawMainFrame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        
        self.withdrawEntry = ctk.CTkEntry(master=self.withdrawMainFrame, fg_color="transparent", border_width=0,font=('Arial Rounded MT Bold', 24), text_color="white", justify="center")
        self.withdrawEntry.insert(0, "$0")
        self.withdrawEntry.icursor(1)
        self.withdrawEntry.pack(padx=20, pady=(25, 15), fill="both")
        
        self.errorMessageLabelTopLevel = ctk.CTkLabel(master=self.withdrawMainFrame, text="", text_color="red")
        self.errorMessageLabelTopLevel.pack(padx=10, fill="both")
        
        self.confirmVar = ctk.IntVar()
        self.withdrawConfirmCheckBox = ctk.CTkCheckBox(master=self.withdrawMainFrame, text="Agree to Withdraw", font=('Arial Rounded MT Bold', 10), border_color="#5b5f61", border_width=2, checkbox_height=15, checkbox_width=15 ,variable=self.confirmVar, onvalue=1, offvalue=0)
        self.withdrawConfirmCheckBox.pack(pady=(0,10), padx=10)
        
        self.withdrawBtn = ctk.CTkButton(master=self.withdrawMainFrame, text="Withdraw", corner_radius=4, width=70, height=30, hover_color="#3c825b", border_color="white", border_width=1, command=lambda: self.withdrawMoney(flag))
        self.withdrawBtn.pack(padx=20, pady=(0, 20), fill="both")
        
    def withdrawMoney(self, flag: bool):
        if self.confirmVar.get() == 0:
            self.errorMessageLabelTopLevel.configure(text="Didn't Agree to Terms")
            return
        if not banking.is_float(self.withdrawEntry.get()[1:]):    
            self.errorMessageLabelTopLevel.configure(text="Invalid Amount")
            return
        
        if float(self.withdrawEntry.get()[1:]) > self.account.getBalance():
            self.errorMessageLabelTopLevel.configure(text="Withdraw Amount Higher than Balance")
            return
        else:
            if not flag:
                if self.withdrawEntry.get().startswith("$"):
                    self.account.setWithdraw(float(self.withdrawEntry.get()[1:]))
                    self.showSavingsBalanceLabel.configure(text=f"${self.account.getBalance()}")
                else:
                    self.account.setWithdraw(float(self.withdrawEntry.get()[0:]))
                    self.showSavingsBalanceLabel.configure(text=f"${self.account.getBalance()}")
            else:
                if self.withdrawEntry.get().startswith("$"):
                    self.account.setWithdraw(float(self.withdrawEntry.get()[1:]))
                    self.showCheckBalanceLabel.configure(text=f"${self.account.getBalance()}")
                else:
                    self.account.setWithdraw(float(self.withdrawEntry.get()[0:]))
                    self.showCheckBalanceLabel.configure(text=f"${self.account.getBalance()}")
            
        self.withdrawtopLevel.destroy()
        
    def transferMoneyWindow(self, event):
        if self.account.checkings == None or self.account.savings == None:
            self.errorMessageLabel.configure(text="Both Checking and Savings need to be Created")
            return
        
        self.transferMoneyTopLevel = ctk.CTkToplevel(self.root)
        self.transferMoneyTopLevel.geometry("500x500")
        self.transferMoneyTopLevel.title("Transfer Money")
        
        self.transferMoneyMainFrame = ctk.CTkFrame(master=self.transferMoneyTopLevel, corner_radius=4, border_width=1, border_color="#5b5f61")
        self.transferMoneyMainFrame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        self.transferAmountEntry = ctk.CTkEntry(master=self.transferMoneyMainFrame, fg_color="transparent", text_color="white", border_width=0, font=('Arial Rounded MT Bold', 24), justify="center")
        self.transferAmountEntry.insert(0, "$0")
        self.transferAmountEntry.icursor(1)
        self.transferAmountEntry.pack(padx=30, pady=20, fill="both")
        
        self.transferInfoFrame = ctk.CTkFrame(master=self.transferMoneyMainFrame, fg_color="transparent", border_width=0)
        self.transferInfoFrame.pack(fil="both", padx=5, pady=5)
        
        self.fromLabel = ctk.CTkLabel(master=self.transferInfoFrame, text="From:", font=('Arial Rounded MT Bold', 18), text_color="white")
        self.fromLabel.grid(row=0, column=0, sticky="w", padx=5)
        
        self.fromAccountComboBox = ctk.CTkComboBox(master=self.transferInfoFrame, border_width=1, text_color="white", font=('Arial Rounded MT Bold', 14), dropdown_font=("Arial Rounded MT Bold", 16), button_color="#5b5f61", border_color="#5b5f61" ,values=['Cloud Checking', 'Cloud Savings'], width=200)
        self.fromAccountComboBox.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        self.dashSeparator = ctk.CTkFrame(master=self.transferInfoFrame, height=2, fg_color="#5b5f61")
        self.dashSeparator.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(30,20))
        
        self.transferAmountLogo = ctk.CTkImage(light_image=Image.open("images/transferAmountLogo.png"), dark_image=Image.open("images/transferAmountLogo.png"))
        self.transferAmountLogoLabel = ctk.CTkLabel(master=self.transferInfoFrame, text="", image=self.transferAmountLogo)
        self.transferAmountLogoLabel.grid(row=2, column=0, columnspan=2)
        
        self.toLabel = ctk.CTkLabel(master=self.transferInfoFrame, text="To:", font=('Arial Rounded MT Bold', 18), text_color="white")
        self.toLabel.grid(row=3, column=0, sticky="w", padx=5)
        
        self.toAccountComboBox = ctk.CTkComboBox(master=self.transferInfoFrame, border_width=1, text_color="white", font=('Arial Rounded MT Bold', 14), dropdown_font=("Arial Rounded MT Bold", 16), button_color="#5b5f61", border_color="#5b5f61" ,values=['Cloud Checking', 'Cloud Savings'], width=200)
        self.toAccountComboBox.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        self.errorMessageLabelTopLevel = ctk.CTkLabel(master=self.transferMoneyMainFrame, text="", text_color="red")
        self.errorMessageLabelTopLevel.pack(padx=10, pady=(40, 5),fill="both")
        
        self.transferBtn = ctk.CTkButton(master=self.transferMoneyMainFrame, text="Transfer", corner_radius=4, width=200, height=30, hover_color="#3c825b", border_color="white", border_width=1, command=self.transferMoney)
        self.transferBtn.pack(padx=5, pady=(0, 15))
        
    def transferMoney(self):
        fromAccountClass = ""
        toAccountClass = ""
        if self.fromAccountComboBox.get() == self.toAccountComboBox.get():
            self.errorMessageLabelTopLevel.configure(text="Transfer Accounts are the Same")
            return
        if self.fromAccountComboBox.get() == "Cloud Savings":
            fromAccountClass = Savings()
        else:
            fromAccountClass = Checking()
        if self.toAccountComboBox.get() == "Cloud Savings":
            toAccountClass = Savings()
        else:
            toAccountClass = Checking()    
        
        if not banking.is_float(self.transferAmountEntry.get()[1:]):    
            self.errorMessageLabelTopLevel.configure(text="Invalid Amount")
            return
        else:
            if self.transferAmountEntry.get().startswith("$"):
                if self.account.transferMoney(float(self.transferAmountEntry.get()[1:]), fromAccount=fromAccountClass, toAccount=toAccountClass) == -1:
                    self.errorMessageLabelTopLevel.configure(text="Amount to High to transfer")
                    return
                self.account.setAccountType(accountType=Savings())
                self.showSavingsBalanceLabel.configure(text=f"${self.account.getBalance()}")
                self.account.setAccountType(accountType=Checking())
                self.showCheckBalanceLabel.configure(text=f"${self.account.getBalance()}")
            else:
                if self.account.transferMoney(float(self.transferAmountEntry.get()[1:]), fromAccount=fromAccountClass, toAccount=toAccountClass) == -1:
                    self.errorMessageLabelTopLevel.configure(text="Amount to High to transfer")
                    return
                self.account.setAccountType(accountType=Savings())
                self.showSavingsBalanceLabel.configure(text=f"${self.account.getBalance()}")
                self.account.setAccountType(accountType=Checking())
                self.showCheckBalanceLabel.configure(text=f"${self.account.getBalance()}")
            
        self.transferMoneyTopLevel.destroy()
        
    def transactionHistoryWindow(self, event, flag: bool):
        num = -1
        if not flag:
            num = 1
        else:
            num = 0
        self.transTopLevel = ctk.CTkToplevel(self.root)
        self.transTopLevel.title("Transaction History")
        self.transTopLevel.geometry("500x500")
        
        self.transMainFrame = ctk.CTkFrame(master=self.transTopLevel, corner_radius=4, border_width=1, border_color="#5b5f61")
        self.transMainFrame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        self.transLabelHistory = ctk.CTkLabel(master=self.transMainFrame, text="Transaction History", font=('Arial Rounded MT Bold', 25), text_color="#50C878")
        self.transLabelHistory.pack(padx=30, pady=20, fill="both")
        
        for element in self.account.transactionList[num][::-1]:
            self.transLabel = ctk.CTkLabel(master=self.transMainFrame, text=element, font=('Arial Rounded MT Bold', 18), text_color="white")
            self.transLabel.pack(padx=20, pady=20)
            self.dashSeparator = ctk.CTkFrame(master=self.transMainFrame, height=2, fg_color="#5b5f61")
            self.dashSeparator.pack(padx=10, pady=2, anchor=ctk.CENTER, fill="both")
        
        
    def transitionToAccountScreen(self):
        for widget in self.root.winfo_children():
            widget.place_forget()
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0,weight=1)
        
        self.bgFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        self.bgFrame.grid(row=0, column=0, sticky="news", columnspan=2)
        
        self.mainFrame = ctk.CTkFrame(self.bgFrame, corner_radius=8, border_width=1, border_color="#5b5f61")
        self.mainFrame.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        
        self.bankNameFrame = ctk.CTkFrame(self.mainFrame, border_width=2, border_color="#5b5f61",fg_color="transparent")
        self.bankNameFrame.pack(pady=(0,5), fill="both")
        
        self.bankNameLabel = ctk.CTkLabel(master=self.bankNameFrame, text="Cloud Banking", font=("Copperplate Gothic Bold", 40), text_color="#50C878")
        self.bankNameLabel.pack(padx=50, pady=20)
        
        self.accountFrame = ctk.CTkFrame(master=self.mainFrame, fg_color="transparent")
        self.accountFrame.pack(fill="x", padx=5, pady=(10,0))
        
        self.accountFrame.columnconfigure(0, weight=1)
        self.accountFrame.columnconfigure(1, weight=1)
        
        self.accountsLabel = ctk.CTkLabel(master=self.accountFrame, text="Accounts", font=('Arial Rounded MT Bold', 24), text_color="white")
        self.accountsLabel.grid(row=0, column=0, sticky="w", padx=20)
        
        self.transferFundImg = ctk.CTkImage(light_image=Image.open("images/arrow-right-arrow-left-solid.png"), dark_image=Image.open("images/arrow-right-arrow-left-solid.png"))
        self.transferFundLabel = ctk.CTkLabel(master=self.accountFrame, text="", image=self.transferFundImg)
        self.transferFundLabel.grid(row=0, column=1, sticky="e", padx=20)
        
        self.transferFundLabel.bind("<Button-1>", self.transferMoneyWindow)
        
        self.dashSeparator = ctk.CTkFrame(master=self.accountFrame, height=2, fg_color="#5b5f61")
        self.dashSeparator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=15)
        
        self.accountTypeFrame = ctk.CTkFrame(master=self.mainFrame, fg_color="transparent")
        self.accountTypeFrame.pack(fill="x", padx=5, pady=(0,10))
        
        self.accountTypeFrame.columnconfigure(0, weight=1)
        self.accountTypeFrame.columnconfigure(1,weight=1)
        
        self.checkingLabel = ctk.CTkLabel(master=self.accountTypeFrame, text="Checking", font=('Arial Rounded MT Bold', 20), text_color="white")
        self.checkingLabel.grid(row=0, column=0, sticky="w", pady=5, padx=20)
        
        self.setUpCheckingBtn = ctk.CTkButton(master=self.accountTypeFrame, text="Set Up", corner_radius=4, width=70, height=30, fg_color="transparent", hover_color="#737170", border_color="white", border_width=1, command=self.setUpChecking)
        self.setUpCheckingBtn.grid(row=0, column=1, sticky="e", padx=20)
        
        self.dashSeparator = ctk.CTkFrame(master=self.accountTypeFrame, height=2, fg_color="#5b5f61")
        self.dashSeparator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=15)
        
        self.savingsLabel = ctk.CTkLabel(master=self.accountTypeFrame, text="Savings", font=('Arial Rounded MT Bold', 20), text_color="white")
        self.savingsLabel.grid(row=2, column=0, sticky="w", pady=5, padx=20)
        
        self.setUpSavingsBtn = ctk.CTkButton(master=self.accountTypeFrame,text="Set Up", corner_radius=4, width=70, height=30, fg_color="transparent", hover_color="#737170", border_color="white", border_width=1, command=self.setUpSavings)
        self.setUpSavingsBtn.grid(row=2, column=1, sticky="e", padx=20)
        
        self.dashSeparator = ctk.CTkFrame(master=self.accountTypeFrame, height=2, fg_color="#5b5f61")
        self.dashSeparator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=(15,5))
        
        self.DepoAndWithFrame = ctk.CTkFrame(master=self.mainFrame, fg_color="transparent", border_width=3, corner_radius=3, border_color="#5b5f61")
        self.DepoAndWithFrame.pack(fill="x", padx=15, pady=(0,5))
        self.DepoAndWithFrame.columnconfigure(0, weight=1)
        self.DepoAndWithFrame.rowconfigure(0,weight=1)
        
        self.depositLabel = ctk.CTkLabel(master=self.DepoAndWithFrame, text="Deposit", font=('Arial Rounded MT Bold', 20), text_color="white")
        self.depositLabel.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        self.DepoBtnFrame = ctk.CTkFrame(master=self.DepoAndWithFrame)
        self.DepoBtnFrame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        self.depoCheckBtn = ctk.CTkButton(master=self.DepoBtnFrame, text="Checking", corner_radius=6, width=150, height=30, fg_color="transparent", hover_color="#737170", border_color="white", border_width=1, command=lambda: self.depoChecking(flag=True))
        self.depoCheckBtn.grid(row=0, column=0, padx=15, pady=5)
        
        self.depoSaveBtn = ctk.CTkButton(master=self.DepoBtnFrame, text="Savings", corner_radius=6, width=150, height=30, fg_color="transparent", hover_color="#737170", border_color="white", border_width=1, command=lambda: self.depoChecking(flag=False))
        self.depoSaveBtn.grid(row=1, column=0, padx=15, pady=5)
        
        self.dashSeparator = ctk.CTkFrame(master=self.DepoAndWithFrame, height=2, fg_color="#5b5f61")
        self.dashSeparator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(2,5))
        
        self.withdrawLabel = ctk.CTkLabel(master=self.DepoAndWithFrame, text="Withdraw", font=('Arial Rounded MT Bold', 20), text_color="white")
        self.withdrawLabel.grid(row=2, column=0, sticky="w", padx=20, pady=10)
        
        self.withBtnFrame = ctk.CTkFrame(master=self.DepoAndWithFrame)
        self.withBtnFrame.grid(row=2, column=1, sticky="ew", padx=5, pady=(0,5))

        self.withCheckBtn = ctk.CTkButton(master=self.withBtnFrame, text="Checking", corner_radius=6, width=150, height=30, fg_color="transparent", hover_color="#737170", border_color="white", border_width=1, command=lambda: self.withDraw(flag=True))
        self.withCheckBtn.grid(row=0, column=0, padx=15, pady=5)
        
        self.withSaveBtn = ctk.CTkButton(master=self.withBtnFrame, text="Savings", corner_radius=6, width=150, height=30, fg_color="transparent", hover_color="#737170", border_color="white", border_width=1, command=lambda: self.withDraw(flag=False))
        self.withSaveBtn.grid(row=1, column=0, padx=15, pady=5)
        
        self.errorMessageLabel = ctk.CTkLabel(master=self.mainFrame, text="", text_color="red")
        self.errorMessageLabel.pack(padx=10, pady=(0,5), fill="both")
        
        self.logOutBtn = ctk.CTkButton(master=self.mainFrame, text="Log Out", corner_radius=6, width=200, height=30, fg_color="transparent", hover_color="#737170", border_color="white", border_width=1, command=self.BackToLogInScreen)
        self.logOutBtn.pack(padx=10, pady=10)
        
    def BackToLogInScreen(self):
        for widget in self.root.grid_slaves():
            widget.grid_remove()
            
        self.logInScreen()
            
        
    def transitionToNewAccountScreen(self):
        # Hide current frames
        for widget in self.leftSideFrame.grid_slaves():
            widget.grid_remove()
        for widget in self.rightSideFrame.grid_slaves():
            widget.grid_remove()

        self.leftSideFrame.grid(row=0, column=1, pady=10)
        self.rightSideFrame.grid(row=0, column=0, sticky="news")
        
        self.rightSideImg2 = ctk.CTkImage(light_image=Image.open("images/cloud2.jpg"), dark_image=Image.open("images/cloud2.jpg"), size=(340,410))

        self.rightSideImgLabel = ctk.CTkLabel(master=self.rightSideFrame, text="", image=self.rightSideImg2)
        self.rightSideImgLabel.grid(row=0, column=0, pady=1, sticky="news", columnspan=2)
        
        self.signup_Label = ctk.CTkLabel(master=self.leftSideFrame, text="Sign up",font=("Arial Rounded MT Bold", 36), text_color="white")
        self.signup_Label.grid(row=0, column=0, padx=10, columnspan=2)
        
        self.dashSeparator = ctk.CTkFrame(master=self.leftSideFrame, height=2, fg_color="#5b5f61")
        self.dashSeparator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=15, padx=10)
        
        self.firstNameEntry = ctk.CTkEntry(master=self.leftSideFrame, placeholder_text="First Name")
        self.firstNameEntry.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="ew")
        
        self.lastNameEntry = ctk.CTkEntry(master=self.leftSideFrame, placeholder_text='Last Name')
        self.lastNameEntry.grid(row=2, column=1, padx=(5, 0), pady=5, sticky="ew")
        
        self.userID_Entry = ctk.CTkEntry(master=self.leftSideFrame, placeholder_text="User ID")
        self.userID_Entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(2,3))
        
        self.userPassword_Entry = ctk.CTkEntry(master=self.leftSideFrame, placeholder_text="Password")
        self.userPassword_Entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5,3))
        
        self.birthdayLabel = ctk.CTkLabel(master=self.leftSideFrame, text="Birthday", font=("Arial", 12), text_color="white")
        self.birthdayLabel.grid(row=5, column=0, columnspan=2,sticky="ew", pady=5)
        
        # Configure grid to ensure equal distribution of space
        self.leftSideFrame.grid_columnconfigure(0, weight=1)
        self.leftSideFrame.grid_columnconfigure(1, weight=1)
        
        self.months = list(calendar.month_name)[1:]
        self.days = [str(day) for day in range(1, 32)]
        currentYear = datetime.now().year
        self.years = [str(year) for year in range(currentYear-80, currentYear+1)][::-1]
        
        self.birthdayFrame = ctk.CTkFrame(self.leftSideFrame)
        self.birthdayFrame.grid(row=6, column=0, columnspan=2, pady=(0, 15))
        
        self.birthMonthComboBox = ctk.CTkComboBox(master=self.birthdayFrame, values=self.months, width=100,)
        self.DOBComboBox = ctk.CTkComboBox(master=self.birthdayFrame, values=self.days, width=100)
        self.birthYearComboBox = ctk.CTkComboBox(master=self.birthdayFrame, values=self.years, width=100)
        
        self.birthMonthComboBox.grid(row=0, column=0, padx=(0,3))
        self.DOBComboBox.grid(row=0, column=1, padx=(0,3))
        self.birthYearComboBox.grid(row=0, column=2)   
        
        self.birthdayFrame.grid_columnconfigure(0, weight=1)
        self.birthdayFrame.grid_columnconfigure(1, weight=1)
        self.birthdayFrame.grid_columnconfigure(2, weight=1)
        
        self.genderLabel = ctk.CTkLabel(master=self.birthdayFrame, text="Gender", font=("Arial", 12), text_color="white")
        self.genderLabel.grid(row=1, column=0, columnspan=3, pady=5)
        
        self.selectedChoice = ctk.IntVar(value=0)
        self.femaleGenderRadioButton = ctk.CTkRadioButton(master=self.birthdayFrame, text="Female", variable=self.selectedChoice, value=1)
        self.femaleGenderRadioButton.grid(row=2, column=0)
        
        self.maleGenderRadioButton = ctk.CTkRadioButton(master=self.birthdayFrame, text="Male", variable=self.selectedChoice, value=2)
        self.noGenderRadioButton = ctk.CTkRadioButton(master=self.birthdayFrame, text="Others", variable=self.selectedChoice, value=3)
        self.maleGenderRadioButton.grid(row=2, column=1)
        self.noGenderRadioButton.grid(row=2, column=2)
        
        self.errorMessageLabel = ctk.CTkLabel(master=self.leftSideFrame, text="", text_color="red")
        self.errorMessageLabel.grid(row=7, column=0, columnspan=2)
        
        self.signUp_Btn = ctk.CTkButton(master=self.leftSideFrame, text="Sign Up", hover_color="#3c825b", corner_radius=11, width=200, command=self.signUpInfo)
        self.signUp_Btn.grid(row=8, column=0, columnspan=2, pady=5)
        
    def signUpInfo(self):
        if self.forgotUserOrPass(True):
            return
        
        if self.missingRequiredInfo():
            self.errorMessageLabel.configure(text="Missing First or Last Name")
            return
        else:
            self.errorMessageLabel.configure(text="")
            
        if self.underTheAge():
            self.errorMessageLabel.configure(text="Under the Age to Create a Bank Account")
            return
        else:
            self.errorMessageLabel.configure(text="")
            
        self.F_Name = self.firstNameEntry.get()
        self.L_Name = self.lastNameEntry.get()
        
        self.userID = self.userID_Entry.get()
        self.password = self.userPassword_Entry.get()
        
        self.birthday = f"{self.birthMonthComboBox.get()} {self.DOBComboBox.get()} {self.birthYearComboBox.get()}"
        
        if not banking.SearchThroughList(self.accountList, self.userID):
            self.account = banking.AccountCreation(self.userID, self.password)
            print(self.account.getUserName() + self.account.getPassword())
        else:
            self.clearEntry(signIn=True)
            self.errorMessageLabel.configure(text="User ID Exits Already")
            return
        self.accountList.append(self.account)
        self.transitionToAccountScreen()
            
            
        
    def clearEntry(self, signIn: bool = False):
        self.userID_Entry.delete(0, ctk.END)
        self.userID_Entry.configure(placeholder_text="User ID")
        self.userPassword_Entry.delete(0, ctk.END)
        self.userPassword_Entry.configure(placeholder_text="Password")
        if signIn:
            self.firstNameEntry.delete(0, ctk.END)
            self.firstNameEntry.configure(placeholder_text="First Name")
            self.lastNameEntry.delete(0, ctk.END)
            self.lastNameEntry.configure(placeholder_text="Last Name")
            
    def underTheAge(self) -> bool:
        yearCompare = datetime.now().year - 18
        if int(self.birthYearComboBox.get()) > yearCompare:
            return True
        elif int(self.birthYearComboBox.get()) == yearCompare:
            if self.months.index(self.birthMonthComboBox.get()) > (datetime.now().month - 1):
                return True
            elif self.months.index(self.birthMonthComboBox.get()) == (datetime.now().month - 1):
                if int(self.DOBComboBox.get()) > datetime.now().day:
                    return True
        return False
        
    def missingRequiredInfo(self) -> bool:
        if self.firstNameEntry.get() == "" or self.lastNameEntry.get() == "":
            self.clearEntry(signIn=True)
            return True
        return False


            
if __name__ == "__main__":
    BankingGUI()
