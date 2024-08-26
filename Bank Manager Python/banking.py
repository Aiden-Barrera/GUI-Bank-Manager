import time
from Checkings import Checking
from Savings import Savings
from datetime import datetime
import calendar
# Class for establishing account creation
class AccountCreation:
    accountMap = {}
    balanceMap = {}
    checkList = []
    savingsList = []
    date = ""
    months = list(calendar.month_name)[1:]
    
    # Constructor
    def __init__(self,username, password, accountType: Checking | Savings = None, checkings: Checking = None, savings: Savings = None):
        self.user_name = username
        self.accountType = accountType
        self.checkings = checkings
        self.savings = savings
        self.transactionList = [self.checkList, self.savingsList]
        self.accountMap[username] = password
        self.balanceMap[username] = [self.checkings, self.savings]
        
    def setAccountType(self, accountType: Checking | Savings):
        self.accountType = accountType
        
    def setChecking(self, checkings: Checking, accountType: Checking):
        self.checkings = checkings
        self.accountType = accountType
        self.balanceMap[self.user_name][0] = self.checkings
        
    def setSavings(self, savings: Savings, accountType: Savings):
        self.savings = savings    
        self.accountType = accountType
        self.balanceMap[self.user_name][1] = self.savings
    
    # Gets the tagger
    def getAccountType(self) -> Checking | Savings:
        return self.accountType  
    
    # Get and Set functions
    def getUserName(self) -> str:
        return self.user_name
    
    def getPassword(self) -> str:
        return self.accountMap.get(self.user_name)
    # Sets the Balance of the Object (Checking or Savings)
    def setBalance(self, balance: float):
        for element in self.balanceMap[self.user_name]:
            if isinstance(element, Checking):
                if type(self.accountType) == type(Checking()):
                    self.date = f"{datetime.now().day}, {self.months[datetime.now().month-1]}:"
                    transText = f"{self.date}                   Deposited +${balance}"
                    self.transactionList[0].append(transText)
                    element.setDeposit(balance)
                    return
            elif isinstance(element, Savings):
                if type(self.accountType) == type(Savings()):
                    self.date = f"{datetime.now().day}, {self.months[datetime.now().month-1]}:"
                    transText = f"{self.date}                   Deposited +${balance}"
                    self.transactionList[1].append(transText)
                    element.setDeposit(balance)
                    return
        return -1
    # Gets the Balance of the Object (Checking or Savings)
    def getBalance(self) -> float:
        for element in self.balanceMap[self.user_name]:
            if isinstance(element, Checking):
                if type(self.accountType) == type(Checking()):
                    return element.getBalance()
            elif isinstance(element, Savings):
                if type(self.accountType) == type(Savings()):
                    return element.getBalance()
        print("Im in GetBalance")
        return -1
            
    # Sets the Withdraw of the Object (Checking or Savings)
    def setWithdraw(self, withdraw: float):
        for element in self.balanceMap[self.user_name]:
            if isinstance(element, Checking):
                if type(self.accountType) == type(Checking()):
                    self.date = f"{datetime.now().day}, {self.months[datetime.now().month-1]}:"
                    transText = f"{self.date}                      Withdrew -${withdraw}"
                    self.transactionList[0].append(transText)
                    element.setWithdraw(withdraw)
            elif isinstance(element, Savings):
                if type(self.accountType) == type(Savings()):
                    self.date = f"{datetime.now().day}, {self.months[datetime.now().month-1]}:"
                    transText = f"{self.date}                       Withdrew -${withdraw}"
                    self.transactionList[1].append(transText)
                    element.setWithdraw(withdraw)
        return -1
    
    def transferMoney(self, amount: float ,fromAccount: Checking | Savings = Checking, toAccount: Checking | Savings = Savings):
        for element in self.balanceMap[self.user_name]:
            if type(element) == type(fromAccount):
                if amount > element.getBalance():
                    return -1
                else:
                    element.setWithdraw(amount)
            if type(element) == type(toAccount):
                element.setDeposit(amount)
            
        
        
# Function for checking if username exists
def UserName_Exists(account: AccountCreation, username: str) -> bool:
    if account.getUserName() == username:
        return True
    else:
        return False
# Function for searching through a list, to check if the username inputted matches
def SearchThroughList(list: list[AccountCreation], username: str) -> bool:
    for element in list:
        if element.getUserName() == username:
            return True
    return False

def SearchThroughListAndReturn(list: list[AccountCreation], username:str):
    for element in list:
        if element.getUserName() == username:
            return element
    return -1
# Function for checking if password matches with existing password for the account
def checkPassword(list: list[AccountCreation], username:str, password: str) -> bool:
    for element in list:
        if element.getUserName() == username and element.getPassword() == password:
            return True
    return False
# Function for showing the account's balance
def show_balance(account: AccountCreation) -> str:
    return f"Hello {account.getUserName()}! Your Account Balance is: ${account.getBalance()}."

def show_all_balances(account: AccountCreation) -> str:
    if account.checkings != None:
        checkBalance = account.balanceMap[account.getUserName()][0]
    else:
        checkBalance = "Account Not Yet Created"
    if account.savings != None:
        saveBalance = account.balanceMap[account.getUserName()][1]
    else:
        saveBalance = "Account Not Yet Created"
    return f"Hello {account.getUserName()}! Your Account Balances are: Checking ({checkBalance}), Savings ({saveBalance})"

# Function for printing accountList
def printList(list: list[AccountCreation]) -> str:
    sentence = ""
    for element in list:
        sentence = element.getUserName() + " " + element.getPassword() + " " + str(element.getBalance())
        
    return sentence
# Function for creating account
def start_creating(accountName: str) -> bool:
    global account
    global accountList
    global accountType
    index = 0
    accountName = input("Enter your Account Name: ")
    time.sleep(1)
    # Checks whether Account Name inputted exists, if not begin creating account
    if not SearchThroughList(accountList, accountName):
        print(f"You don't have a account with us {accountName}")
        # Asks whether the user wants to create a account and if it's not yes or no, keep asking
        createAccountFlag = False
        while not createAccountFlag:
            createAccount = input("Do you wish to create an account? (yes or no) ")
            # If they wish to create an account they proceed creating their password
            if createAccount == "yes":
                print("Great let's create a password!")
                accountPassword = input("Enter your Account Password: ")
                createCheckOrSave = False
                while not createCheckOrSave:
                    accountTypeBool = input(f"Welcome {accountName} to Kaland Banking!\nDo you wish to create a Checking or Savings account with us? (Checking/Savings) ")
                    time.sleep(1)
                    if accountTypeBool.lower() == "checking":
                        accountType = Checking()
                        account = AccountCreation(accountName, accountPassword, accountType, Checking(accountName))
                        createCheckOrSave = True
                    elif accountTypeBool.lower() == "savings":
                        accountType = Savings()
                        account = AccountCreation(accountName, accountPassword, accountType, None, Savings(accountName))
                        createCheckOrSave = True
                    else:
                        print("Invalid Answer, Try Again.")
                accountList.append(account)
                print(printList(accountList))
                createAccountFlag = True
            # If they don't wish to create an account the program ends
            elif createAccount == "no":
                print("That's fine, have a great day!")
                time.sleep(1)
                createAccountFlag = True
                return False
            else:
                print("Try Again.")
    # Checks whether the account inputted exists, if so compare password
    elif SearchThroughList(accountList, accountName):
        print("It seems you already have an account with us!")
        time.sleep(1)
        correctPass = False
        wrongLimit = 0
        GuessesLeft = 3
        # if account exists, it checks if password matches
        while not correctPass:
            accountPass = input("Enter your Account Password: ")
            # Checks if incorrect guesses exceeds limit
            if wrongLimit >= 2:
                print("You've reached the Limit for Incorrect Guesses!")
                return False
            if checkPassword(accountList, accountName, accountPass):
                time.sleep(1)
                askAgain(accountName)
                correctPass = True
            else:
                GuessesLeft = GuessesLeft - 1
                print(f"Incorrect Password. Try Again. Guesses Left: {GuessesLeft}")
                time.sleep(1)
                wrongLimit = wrongLimit + 1
    return True
# Function for giving the user choices
def account_choices(accountName: str) -> bool:
    global account
    global accountList
    userChoiceFlag = False
    while not userChoiceFlag:
        time.sleep(1)
        userChoice = input(f"{accountName} Do you wish to\n 1.) Deposit \n 2.) Withdraw \n 3.) Show This Balance \n 4.) Show All Balances\n 5.) Exit Account\n")
        if userChoice == "1":
            time.sleep(1)
            depositAmount = input("How much do you wish to deposit today? ")
            if not is_float(depositAmount):
                print("Invalid Deposit Amount")
                print("Please Try Again!")
            else:
                if type(account.getAccountType()) == type(Checking()):
                    account.setBalance(float(depositAmount))
                    print(account.getBalance())
                elif type(account.getAccountType()) == type(Savings()):
                    account.setBalance(float(depositAmount))
                    print(account.getBalance())
        elif userChoice == "2":
            time.sleep(1)
            withdrawAmount = input("How much do you wish to withdraw today? ")
            if not is_float(withdrawAmount):
                print("Invalid Withdrawal Amount")
                print("Please Try Again")
            elif float(withdrawAmount) > account.getBalance():
                print("ERR: Trying to Withdraw more than you have Deposited")
                print("Please Try Again!")
            elif float(withdrawAmount) < 0.0:
                    print("Invalid Withdrawal Amount")
                    print("Please Try Again")
            else:
                if type(account.getAccountType()) == type(Checking()):
                    account.setWithdraw(float(withdrawAmount))
                    print(account.getBalance())
                elif type(account.getAccountType()) == type(Savings()):
                    account.setWithdraw(float(withdrawAmount))
                    print(account.getBalance())
        elif userChoice == "3":
            time.sleep(1)
            print(show_balance(account))
        elif userChoice == "4":
            time.sleep(1)
            print(show_all_balances(account))
        elif userChoice == "5":
            time.sleep(1)
            print("Have a great day!")
            userChoiceFlag = True
        else:
            print("Try Again")
    return True

def askAgain(accountName):
    global account
    if type(account.getAccountType()) == type(Checking()):
        createCheckOrSave = False
        while not createCheckOrSave:
            accountTypeBool = input(f"Welcome Back {account.getUserName()} to Kaland Banking!\nDo you wish to create a Savings account with us? (Savings) ")
            time.sleep(1)
            if accountTypeBool.lower() == "savings":
                accountType = Savings()
                time.sleep(3)
                account.accountType = accountType
                account.savings = Savings(account.getUserName())
                account.balanceMap[account.getUserName()][1] = account.savings
                createCheckOrSave = True
            elif accountTypeBool.lower() == "no":
                createCheckOrSave = True
                return -1
            else:
                print("Invalid Answer, Try Again.")
    elif type(account.getAccountType()) == type(Savings()):
        createCheckOrSave = False
        while not createCheckOrSave:
            accountTypeBool = input(f"Welcome Back {account.getUserName()} to Kaland Banking!\nDo you wish to create a Checking account with us? (Checking) ")
            time.sleep(1)
            if accountTypeBool.lower() == "checking":
                accountType = Checking()
                account.accountType = accountType
                account.checkings = Checking(accountName) 
                account.balanceMap[accountName][0] = account.checkings               
                createCheckOrSave = True
            elif accountTypeBool.lower() == "no":
                createCheckOrSave = True
                return -1
            else:
                print("Invalid Answer, Try Again.")
    print(printList(accountList))

def is_float(element: str) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

is_running = True
accountList = []
account = None
account2 = Checking()

if __name__ == "__main__":
    while is_running:
        # Starts the Program with a Introduction
        print("***************************")
        print("Welcome to Cloud Banking!")
        print("let's get you started!")
        print("***************************")
        accountName = ""
        if start_creating(accountName) != True:
            is_running = False
            break
        # Give them the option to deposit, withdraw, or show balance
        print("***************************")
        if account_choices(accountName) != True:
            is_running = False
            break
        print("-----------------------------")
        
    print("PROGRAM ENDED")