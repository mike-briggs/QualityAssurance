import os
import sys
import json

validAccounts = sys.argv[1]  # file path for "valid_accounts.txt"
outputFilepath = sys.argv[2]  # file path for "out.actual.txt"
inputFile = outputFilepath

print("Welcome!")

userInput = input('> ')
print(userInput)
# if(userInput == 'login'):
#     login(current, accounts, login, outputFilepath)
if(userInput == 'logout'):
    logout(outputFilepath)

# loginState = 0
# i = 0
# while i <= numOfTransactions:
#     current = transactions[i]
#     line = current.split(" ")
#     if line[0] == "login":
#         loginState = login(current, accounts, login, outputFilepath)
#     elif line[0] == "logout":
#         loginState = logout(current, accounts, login, outputFile)
#     elif line[0] == "deposit":
#         deposit(current, accounts, loginState, outputFile)
#     elif line[0] == "withdraw":
#         withdraw(current, accounts, loginState, outputFile)
#     elif line[0] == "transfer":
#         transfer(current, accounts, loginState, outputFile)
#     elif line[0] == "createacct":
#         accounts = createacct(current, accounts, loginState, outputFile)
#     elif line[0] == "deleteacct":
#         accounts = deleteacct(current, accounts, loginState, outputFile)

# i += 1

print("Program Finished.\n")


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


# def login(transaction, listOfAccounts, login, outputFile):
#     print('print inside function')
#     with open(outputFile, 'w') as wf:
#         wf.write('Write to actual')

#     # file = open(outputFile, "w+")
#     # delimited = transaction.split(" ")
#     # types = delimited[1]

#     # # Validation cases
#     # if types != "machine" and types != "agent"
#     # print("Invalid user type")
#     # elif login == 1 or login == 2               # Already logged in
#     # print("Already logged in")
#     # elif types == "machine"                      # login machine
#     # return 1
#     # elif types == "agent"                        # login agent
#     # return 2

#     return 0


def logout(outputFile):
    print('inside function')
    with open(outputFile, 'w') as wf:
        wf.write('You are not logged in')

    return 0


# def deposit(transaction, listOfAccounts, login, outputFile):

#     delimited = transaction.split(" ")
#     acctNum = delimited[1]
#     amount = delimited[2]

#     file = open(outputFile, "w+")

#     # Validation cases
#     if login == 0:
#         print("You are not logged in.")

#     elif len(acctNum) != 7 or not acctNum.isdigit():
#         print("Invalid account number.")

#     elif acctNum not in listOfAccounts:
#         print("Deposit account does not exist.")

#     elif not amount.isdigit():
#         print("Amount is not a valid amount.")

#     elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):
#         print("Over deposit limit.")

#     else
#     print("DEP "+acctNum+" "+amount+" name")

#     return True


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
