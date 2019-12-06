import os
import sys
import json
import re

# Account class holds the account number and how much has been:
# deposited, withdrawn, transfered trhroughout this session.
# As well as holds the temporary "balance"


class Account:
    def __init__(self, number, dep, wdr, bal, xfr):
        self.number = number
        self.dep = dep
        self.wdr = wdr
        self.bal = bal
        self.xfr = xfr

# Writes to the output file that the session has ended
# returns 0 on success


def logout(outputFile):
    with open(outputFile, 'a') as wf:
        wf.write('\nEOS 0000000 000 0000000 ***')
    return 0

# 0     - success/already logged in
# -1    - error/not logged in


def login(outputFile):
    arg2 = input('Enter mode: ')
    print(arg2)

    if(arg2 == 'machine' or arg2 == 'agent'):
        print("Login Successful")
        if(arg2 == 'machine'):
            return 2
        else:
            return 1
    else:
        print("Invalid type")
        return -1

# failed deposit returns false
# successful deposit returns array(accountNum,amount) deposited to update session/acount deposit limit


def deposit(outputFile, validAccounts, loginState, accountDepositArray):

    # Validation cases
    acctNum = input("Enter account number: ")  # account num
    print(acctNum)

    if (len(acctNum) != 7 or not acctNum.isdigit()) or acctNum not in validAccounts:
        print("Invalid account number.")
        return False
    else:
        amount = input("Enter amount: ")
        print(amount)

        if(amount.isdigit()):
            if(loginState == 2 and int(amount) > 2000):
                print("Over machine deposit limit.")
                return False
            elif(loginState == 1 and int(amount) > 99999999):
                print("Over agent deposit limit.")
                return False
            else:
                # initiate dcurrently deposited to check daily limit
                currentlyDeposited = 0
                # find the array index with this account number and store how much was deposited in this session
                for i in range(len(accountDepositArray)):
                    if(accountDepositArray[i].number == acctNum):
                        currentlyDeposited = accountDepositArray[i].dep
                        break
                # check if we can still deposit to this account
                if(currentlyDeposited + int(amount) > 5000):
                    print("Over daily deposit limit.")
                    return False
                else:
                    # successful deposit
                    with open(outputFile, 'a') as wf:
                        wf.write('\nDEP '+acctNum+' '+amount+' 0000000 ***')
                    print("Funds successfully deposited.")
                    return [acctNum, amount]
        else:
            print("Invalid amount.")
            return False

# failed withdrawal returns false
# successful withdrawal returns array(accountNum,amount) withdrawn to update session/acount withdrawal limit


def withdraw(outputFile, validAccounts, accountCaps, loginState):

    acctNum = input("Enter account number: ")  # account num
    print(acctNum)

    if (len(acctNum) != 7 or not acctNum.isdigit()) or acctNum not in validAccounts:
        print("Invalid account number.")
        return False
    else:
        amount = input("Enter amount: ")
        print(amount)

        if(amount.isdigit()):
            if(int(amount) > 1000 and loginState == 2):
                print("Over machine withdrawal limit.")
                return False
            elif(int(amount) > 99999999 and loginState == 1):
                print("Over agent withdrawal limit.")
                return False
            else:
                currentlyWithdrawn = 0
                # find the array index with this account number and store how much was deposited in this session
                for i in range(len(accountCaps)):
                    if(accountCaps[i].number == acctNum):
                        currentlyWithdrawn = accountCaps[i].wdr
                        break
                # check if we can still withdraw from this account
                if(currentlyWithdrawn + int(amount) > 5000):
                    print("Over daily withdraw limit.")
                    return False
                else:
                    with open(outputFile, 'a') as wf:
                        wf.write('\nWDR '+acctNum+' '+amount+' 0000000 ***')
                    print("Funds successfully withdrawn")
                    return [acctNum, amount]
        else:
            print("Invalid amount.")
            return False

# Returns false on failed transfer (and writes to console output)
# Returns array of [Account number, amount] on success


def transfer(outputFile, validAccounts, loginState, accountDetails):
    fromAccount = input("Enter (from) account: ")
    print(fromAccount)

    # Validation cases
    # If accout number not proper, error
    if len(fromAccount) != 7 or not fromAccount.isdigit() or fromAccount not in validAccounts:
        print("Invalid account number.")
        return False
    else:
        toAccount = input("Enter (to) account: ")
        print(toAccount)
        # If accout number not proper, error
        if len(toAccount) != 7 or not toAccount.isdigit() or toAccount not in validAccounts or toAccount == fromAccount:
            print("Invalid account number.")
            return False
        else:
            amount = input("Enter amount: ")
            print(amount)

            transferredThisSession = 0
            for i in range(len(accountDetails)):
                if(accountDetails[i].number == fromAccount):
                    transferredThisSession = accountDetails[i].xfr

            # TODO validate money in account using accountDetails
            if (amount.isdigit()):                          # If amount not proper, error
                if(int(amount) > 10000 and loginState == 2):
                    print("Over machine transfer limit.")
                elif(int(amount) > 99999999 and loginState == 1):
                    print("Over agent transfer limit.")
                else:
                    if(int(amount) + transferredThisSession > 10000):
                        print("Over daily transfer limit.")
                        return False
                    else:
                        print("Funds successfully transfered.")
                        with open(outputFile, 'a') as wf:
                            wf.write('\nXFR '+toAccount+' ' +
                                     amount+' '+fromAccount+' ***')
                        return [fromAccount, amount]
            else:
                print("Invalid amount.")
                return False

# Returns the new account number on success
# otherwise returns false


def createacct(outputFile, validAccounts, validAccountsPath, loginState):
    # NEW to amount from name
    if(loginState == 1):
        acctNum = input("Enter account number: ")
        print(acctNum)

        if(acctNum in validAccounts):
            print("Account number already in use.")
            return False
        else:
            if(len(acctNum) != 7 or not acctNum.isdigit() or str(acctNum)[:1] == '0'):
                print("Invalid account number.")
            else:
                acctName = input("Enter account name: ")
                print(acctName)
                regex = "^ [A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _] *$"
                if((len(acctName) >= 3 and len(acctName) <= 30) or re.match(regex, acctName) or acctName.startswith(' ') or acctName.endswith(' ')):
                    print("Account created successfully.")
                    with open(outputFile, 'a') as wf:
                        wf.write('\nNEW '+acctNum+' 000 '+'0000000 '+acctName)
                    return acctNum
                else:
                    print("Invalid account name.")
                    return False

    else:
        print("You do not have the priviledge for this command.")
        return False

# return the account number of the account to delete on success
# otherwise returns false


def deleteacct(outputFile, validAccounts, loginState):

    if(loginState == 1):
        acctNum = input("Enter account number: ")
        print(acctNum)

        if(acctNum in validAccounts):
            acctName = input("Enter account name: ")
            print(acctName)

            if((len(acctName) >= 3 and len(acctName) <= 30) or not acctName.isalnum() or acctName.startswith(' ') or acctName.endswith(' ')):
                print("Account deleted successfully")
                with open(outputFile, 'a') as wf:
                    wf.write('\nDEL '+acctNum+' 000 '+'0000000 '+acctName)
                return acctNum

            else:
                print("Invalid account name")

        else:
            print("Invalid account number.")
            return False

    else:
        print("You do not have the priviledge for this command.")
        return False
# main


# file path for "valid_accounts.txt"
validAccountsPath = sys.argv[1]
outputFilepath = sys.argv[2]                # file path for "out.actual.txt"
transaction_session = sys.argv[3] #file path for input transaction session

# initialize the login state as 0 (not logged in)
loginStatus = 0

file = open(validAccountsPath, 'r')
validAccounts = file.read().split(',')

# we need an array that holds account objects which hold
# how much has been deposited in this session

validAccountsObj = []
for i in range(len(validAccounts)):
    validAccountsObj.append(Account(validAccounts[i], 0, 0, 0, 0))

with open(outputFilepath, 'w') as wf:
    wf.write('')

with open(transaction_session) as f:
    session = f.readlines()

#session = [x.strip() for x in session] 
count = -1

print("Welcome to Quinterac")
while(True):    # First loop is the state before being logged in
    count = count + 1
    #userInput = input('Type \'exit\' to leave\n> ')
    #print(userInput)

    userInput = session[count]
    print(userInput)
    if(userInput == 'login'):
        # set login status with function
        loginStatus = login(outputFilepath)
        if(loginStatus > 0):                                        # if logged in
            while(loginStatus > 0):                                 # while session is active
                # User is now logged in and has access to functions
                userInput = input("Enter action: ")
                print(userInput)
                if userInput == "logout":
                    loginStatus = logout(outputFilepath)
                elif userInput == "deposit":
                    amountDeposited = deposit(outputFilepath, validAccounts,
                                              loginStatus, validAccountsObj)
                    if(amountDeposited):
                        # find account number and update amount of that account
                        for i in range(len(validAccountsObj)):
                            if(validAccountsObj[i].number == amountDeposited[0]):
                                validAccountsObj[i].dep += int(
                                    amountDeposited[1])
                                validAccountsObj[i].bal += int(
                                    amountDeposited[1])
                elif userInput == "withdraw":
                    amountWithdrawn = withdraw(
                        outputFilepath, validAccounts, validAccountsObj, loginStatus)

                    if(amountWithdrawn):
                        # find account number and update withdrawn amount of that account
                        for i in range(len(validAccountsObj)):
                            if(validAccountsObj[i].number == amountWithdrawn[0]):
                                validAccountsObj[i].wdr += int(
                                    amountWithdrawn[1])
                                validAccountsObj[i].bal -= int(
                                    amountDeposited[1])
                elif userInput == "transfer":
                    amountTransfered = transfer(outputFilepath, validAccounts,
                                                loginStatus, validAccountsObj)
                    # need to update the accounts object to keep record of transaction limits
                    if(amountTransfered):
                        for i in range(len(validAccountsObj)):
                            if(validAccountsObj[i].number == amountTransfered[0]):
                                validAccountsObj[i].xfr += int(
                                    amountTransfered[1])
                elif userInput == "createacct":
                    validAccounts.append(createacct(outputFilepath, validAccounts,
                                                    validAccountsPath, loginStatus))
                elif userInput == "deleteacct":
                    accounts = deleteacct(
                        outputFilepath, validAccounts, loginStatus)

                    # remove the deleted account from valid accounts
                    if(accounts):
                        for i in range(len(validAccounts)):
                            if validAccounts[i] == accounts:
                                del validAccounts[i]
                                break

    elif(userInput == 'logout'):
        print("You are not logged in")

    if(userInput == 'exit'):
        break
