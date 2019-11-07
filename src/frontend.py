import os
import sys
import json
import re


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


def deposit(outputFile, validAccounts, loginState):

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
                with open(outputFile, 'a') as wf:
                    wf.write('\nDEP '+acctNum+' '+amount+' 0000000 ***')
                print("Funds successfully deposited.")
                return True
        else:
            print("Invalid amount.")
            return False


def withdraw(outputFile, validAccounts):

    acctNum = input("Enter account number: ")  # account num
    print(acctNum)

    if (len(acctNum) != 7 or not acctNum.isdigit()) or acctNum not in validAccounts:
        print("Invalid account number.")
        return False
    else:
        amount = input("Enter amount: ")
        print(amount)

        if(amount.isdigit()):
            with open(outputFile, 'a') as wf:
                wf.write('\nWDR '+acctNum+' '+amount+' 0000000 ***')
            print("Funds successfully withdrawn")
            return True
        else:
            print("Invalid amount.")
            return False


def transfer(outputFile, validAccounts):
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

            if (amount.isdigit()):                          # If amount not proper, error
                print("Funds successfully transfered.")
                with open(outputFile, 'a') as wf:
                    wf.write('\nXFR '+toAccount+' ' +
                             amount+' '+fromAccount+' ***')
                return True
            else:
                print("Invalid amount.")
                return False

    # elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):  # Enforce limit
    #     print("Over withdrawal limit.")

    # elif login == 1 and amount > 5000:                  # Daily limit: TODO
    #     print("Amount is not a valid amount.")

    # else


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
                return True

            else:
                print("Invalid account name")

        else:
            print("Invalid account number.")
            return False

    else:
        print("You do not have the priviledge for this command.")
        return False
# main


validAccountsPath = sys.argv[1]  # file path for "valid_accounts.txt"
outputFilepath = sys.argv[2]  # file path for "out.actual.txt"

loginStatus = 0

file = open(validAccountsPath, 'r')
validAccounts = file.read().split(',')

with open(outputFilepath, 'w') as wf:
    wf.write('')

print("Welcome to Quinterac")
while(True):

    userInput = input('Type \'exit\' to leave\n> ')
    print(userInput)

    if(userInput == 'login'):
        # set login status with function
        loginStatus = login(outputFilepath)
        if(loginStatus > 0):                                        # if logged in
            while(loginStatus > 0):                                 # while session is active
                userInput = input("Enter action: ")
                print(userInput)
                if userInput == "logout":
                    loginStatus = logout(outputFilepath)
                elif userInput == "deposit":
                    deposit(outputFilepath, validAccounts, loginStatus)
                elif userInput == "withdraw":
                    withdraw(outputFilepath, validAccounts)
                elif userInput == "transfer":
                    transfer(outputFilepath, validAccounts)
                elif userInput == "createacct":
                    validAccounts.append(createacct(outputFilepath, validAccounts,
                                                    validAccountsPath, loginStatus))
                elif userInput == "deleteacct":
                    accounts = deleteacct(
                        outputFilepath, validAccounts, loginStatus)
    elif(userInput == 'logout'):
        print("You are not logged in")

    if(userInput == 'exit'):
        break
