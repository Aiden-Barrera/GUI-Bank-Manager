import bcrypt

class Savings:
    deposit = 0
    accessCode = ""
    balanceMap = {}
    accountType = ""
    def __init__(self, accessCode: str = None):
        if accessCode != None:
            hashed = bcrypt.hashpw(accessCode.encode('utf-8'), bcrypt.gensalt())
            self.accessCode = hashed
            self.balanceMap[self.accessCode] = float(0)

    def getBalance(self) -> float:
        return self.balanceMap[self.accessCode]

    def setDeposit(self, amount: float) -> None:
        self.balanceMap[self.accessCode] += amount
        self.balanceMap[self.accessCode] = round(self.balanceMap[self.accessCode], 2)

    def setWithdraw(self, amount: float):
        try:
            if amount > self.balanceMap[self.accessCode]:
                raise Exception()
        except Exception:
            print("Console Log: Exception Caught")
            return -1
        self.balanceMap[self.accessCode] -= amount
        self.balanceMap[self.accessCode] = round(self.balanceMap[self.accessCode], 2)

    def getAccessCode(self) -> str:
        return self.accessCode
    
    def __str__(self) -> str:
        return f"${self.getBalance()}"