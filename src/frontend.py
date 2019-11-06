import os
import sys
import json


def logout(line, outputFile):
    with open(outputFile, 'w') as wf:
        wf.write('EOS 0000000 000 0000000 ***')

    return 0

# 0     - success/already logged in
# -1    - error/not logged in


def login(line, outputFile):
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


def deposit(line, outputFile, validAccounts):

    # Validation cases
    acctNum = input("Enter account number: ")  # account num
    print(acctNum)

    if (len(acctNum) != 7 or not acctNum.isdigit()) or acctNum not in validAccounts:
        print("Invalid account number.")
        return False
    else:
        amount = input("Enter amount: ")
        print(amount)

        # TODO NEED TO VALIDATE THE AMOUNT

        if(amount.isdigit()):
            transactionString = 'DEP ' + \
                str(acctNum)+' '+str(amount)+' 0000000 ***'

            with open(outputFile, 'w') as wf:
                wf.write(str(transactionString))
            print("Funds successfully deposited")
            return True
        else:
            print("Invalid amount.")
            return False

        # elif acctNum not in listOfAccounts:
        # print("Deposit account does not sexist.")

        # if not amount.isdigit():
        #     print("Amount is not a valid amount.")
        # elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):
        #     print("Over deposit limit.")
        # else:

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
    loginStatus = login(userInput, outputFilepath)
    if(loginStatus > 0):    # if logged in
        while(loginStatus > 0):
            userInput = input("Enter action: ")
            print(userInput)
            if userInput == "logout":
                loginStatus = logout(userInput, outputFilepath)
            elif userInput == "deposit":
                deposit(userInput, outputFilepath, validAccounts)
            # elif userInput == "withdraw":
            #     withdraw(current, accounts, loginState, outputFile)
            # elif userInput == "transfer":
            #     transfer(current, accounts, loginState, outputFile)
            # elif userInput == "createacct":
            #     accounts = createacct(current, accounts, loginState, outputFile)
            # elif userInput == "deleteacct":
            #     accounts = deleteacct(current, accounts, loginState, outputFile)
elif(userInput == 'logout'):
    print("You are not logged in")

# def readValidAccounts(filename):

#     masterAccountsList = []  # initialize master list of accounts
#     # accountsFile = open(filename, "r")      # read the file
#     # get number of lines in the file
#     numLinesInFile = sum(1 for line in open(filename))

#     # for every line in the file
#     for i in numLinesInFile:
#         line = accountsFile.readline()  # read line
#         masterAccountsList.append(line)  # append new account to master list

#     accountsFile.close()

#     return masterAccountsList


# def readInTransactions(filename):

#     masterTransactionsList = []  # initialize master list of transactions
#     transactionsFile = open(filename, "r")  # read the file
#     numLinesInFile = sum(1 for line in open(filename))

#     for i in numLinesInFile:
#         line = transactionsFile.readline()
#         masterTransactionsList.append(line)

#     return masterTransactionsList


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


# def transfer(transaction, listOfAccounts, login, outputFile):

#     file = open(outputFile, "w+")
#     delimited = transaction.split(" ")  # to from balance
#     toAccount = delimited[1]
#     fromAccount = delimited[2]
#     amount = delimited[3]

#     # Validation cases
#     if login == 0:              # If not logged in, error
#         print("You are not logged in.")

#     elif len(toAccount) != 7 or not toAccount.isdigit():    # If accout number not proper, error
#         print("Invalid account number.")

#     elif len(fromAccount) != 7 or not fromAccount.isdigit():    # If accout number not proper, error
#         print("Invalid account number.")

#     elif toAccount not in listOfAccounts or fromAccount not in listOfAccounts:   # Make sure account exists
#         print("Account does not exist.")

#     elif not amount.isdigit():                          # If amount not proper, error
#         print("Amount is not a valid amount.")

#     elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):  # Enforce limit
#         print("Over withdrawal limit.")

#     elif login == 1 and amount > 5000:                  # Daily limit: TODO
#         print("Amount is not a valid amount.")

#     else
#     print("XFR "+toAccount+" "+amount+" "+fromAccount+" name")

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
