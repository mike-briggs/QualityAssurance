import os
import sys
import json


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
            return 1
        else:
            return 2
        return 0
    else:
        print("Invalid type")
        return -1


def deposit(outputFile, validAccounts):

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
            with open(outputFile, 'a') as wf:
                wf.write('\nDEP '+acctNum+' '+amount+' 0000000 ***')
            print("Funds successfully deposited")
            return True
        else:
            print("Invalid amount.")
            return False

        # if not amount.isdigit():
        #     print("Amount is not a valid amount.")
        # elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):
        #     print("Over deposit limit.")
        # else:

def withdraw(listOfAccounts, outputFile, validAccounts):

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

# main


validAccountsPath = sys.argv[1]  # file path for "valid_accounts.txt"
outputFilepath = sys.argv[2]  # file path for "out.actual.txt"

loginStatus = 0

file = open(validAccountsPath, 'r')
validAccounts = file.read().split(',')

print("Welcome to Quinterac")
userInput = input('> ')
print(userInput)
with open(outputFilepath, 'w') as wf:
    wf.write('')

if(userInput == 'login'):
    loginStatus = login(outputFilepath)
    if(loginStatus > 0):    # if logged in
        while(loginStatus > 0):
            userInput = input("Enter action: ")
            print(userInput)
            if userInput == "logout":
                loginStatus = logout(outputFilepath)
            elif userInput == "deposit":
                deposit(outputFilepath, validAccounts)
            # elif userInput == "withdraw":
            #     withdraw(current, accounts, loginState, outputFile)
            elif userInput == "transfer":
                transfer(outputFilepath, validAccounts)
            # elif userInput == "createacct":
            #     accounts = createacct(current, accounts, loginState, outputFile)
            # elif userInput == "deleteacct":
            #     accounts = deleteacct(current, accounts, loginState, outputFile)
elif(userInput == 'logout'):
    print("You are not logged in")


# def withdraw(transaction, listOfAccounts, login, outputFile):

#     delimited = transaction.split(" ")
#     acctNum = delimited[1]
#     amount = delimited[2]

#     file = open(outputFile, "w+")

#     # Validation cases
#     if login == 0:              # If not logged in, error
#         print("You are not logged in.")

#     elif len(acctNum) != 7 or not acctNum.isdigit():    # If accout number not proper, error
#         print("Invalid account number.")

#     elif acctNum not in listOfAccounts:                 # Make sure account exists
#         print("Withdrawal account does not exist.")

#     elif not amount.isdigit():                          # If amount not proper, error
#         print("Amount is not a valid amount.")

#     elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):  # Enforce limit
#         print("Over withdrawal limit.")

#     elif login == 1 and amount > 5000:                  # Daily limit: TODO
#         print("Amount is not a valid amount.")

#     print("WDR "+acctNum+" "+amount+" 0000000 name")

#     return True


# def createacct(transaction, listOfAccounts):
#     # NEW to amount from name
#     file = open(outputFile, "w+")
#     delimited = transaction.split(" ")

#     acctNum = delimited[1]
#     amount = delimited[2]
#     name = delimited[3]

#     # Validation cases
#     if login == 0:              # If not logged in, error
#         print("You are not logged in.")

#     elif login == 1:
#         print("Not priviledged for this command")
#     elif len(acctNum) != 7 or not acctNum.isdigit():    # If accout number not proper, error
#         print("Invalid account number.")

#     else
#     print("NEW "+acctNum+" 000 "+"0000000 "+name)
#     listOfAccounts.append(acctNum)

#     return listOfAccounts


# def deleteacct(transaction, listOfAccounts):

# file = open(outputFile, "w+")
# delimited = transaction.split(" ")

# acctNum = delimited[1]
#  amount = delimited[2]
#   name = delimited[3]

#    # Validation cases
#    if login == 0:              # If not logged in, error
#         print("You are not logged in.")

#     elif login == 1:
#         print("Not priviledged for this command")
#     elif len(acctNum) != 7 or not acctNum.isdigit():    # If accout number not proper, error
#         print("Invalid account number.")

#     elif acctNum not in listOfAccounts:    # Make sure account exists
#         print("Account does not exist.")

#     else
#     print("DEL "+acctNum+" 000"+" 0000000 "+name)
#     listOfAccounts.remove(acctNum)

#     return listOfAccounts
