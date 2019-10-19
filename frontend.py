import json
from classes import Account


def readValidAccounts(filename):

    masterAccountsList = []                      # initialize master list of accounts
    accountsFile = open(filename, "r")      # read the file

    # get number of lines in the file
    numLinesInFile = sum(1 for line in open(filename))

    # for every line in the file
    for i in numLinesInFile:
        # read line
        line = accountsFile.readline()
        # append new account to master list
        masterAccountsList.append(line)

    accountsFile.close()

    return masterAccountsList


def readInTransactions(filename):

    masterTransactionsList = []     # initialize master list of transactions
    transactionsFile = open(filename, "r") # read the file
    numLinesInFile = sum(1 for line in open(filename))

    for i in numLinesInFile:
        line = transactionsFile.readline()
        masterTransactionsList.append(line)

    return masterTransactionsList


def login(transaction, listOfAccounts, login, outputFile):
    file = open(outputFile, "w+")
    delimited = transaction.split(" ")
    type = delimited[1]

    # Validation cases
    if type not "machine" and type not "agent"  # Invalid user type
        file.write("Invalid user type")
    elif login == 1 or login == 2               # Already logged in
        file.write("Already logged in")
    elif type == "machine"                      # login machine
        return 1
    elif type == "agent"                        # login agent
        return 2

    return 0

def logout(transaction, listOfAccounts, login, outputFile):
    file = open(outputFile, "w+")
    if login == 0
        file.write("You are not logged in")
    return 0

def deposit(transaction, listOfAccounts, login, outputFile):
    delimited = transaction.split(" ")
    acctNum = delimited[1]
    amount = delimited[2]

    file = open(outputFile, "w+")

    # Validation cases
    if login == 0:
        file.write("You are not logged in.")
        file.close()
    elif len(acctNum) != 7 or not acctNum.isdigit():
        file.write("Invalid account number.")
        file.close()
    elif acctNum not in listOfAccounts:
        file.write("Deposit account does not exist.")
        file.close()
    elif not amount.isdigit():
        file.write("Amount is not a valid amount.")
        file.close()
    elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):
        file.write("Over deposit limit.")
        file.close()
    else
        file.write("DEP "+acctNum+" "+amount+" name")
    return True

def withdraw(transaction, listOfAccounts, login, outputFile):
    delimited = transaction.split(" ")
    acctNum = delimited[1]
    amount = delimited[2]

    file = open(outputFile, "w+")

    # Validation cases
    if login == 0:              # If not logged in, error
        file.write("You are not logged in.")
        file.close()
    elif len(acctNum) != 7 or not acctNum.isdigit():    # If accout number not proper, error
        file.write("Invalid account number.")
        file.close()
    elif acctNum not in listOfAccounts:                 # Make sure account exists
        file.write("Withdrawal account does not exist.")
        file.close()
    elif not amount.isdigit():                          # If amount not proper, error
        file.write("Amount is not a valid amount.")
        file.close()
    elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99): # Enforce limit
        file.write("Over withdrawal limit.")
        file.close()
    elif login == 1 and amount > 5000:                  # Daily limit: TODO
        file.write("Amount is not a valid amount.")
        file.close()
    file.write("WDR "+acctNum+" "+amount+" 0000000 name")
    return True

def transfer(transaction, listOfAccounts, login, outputFile):

    file = open(outputFile, "w+")
    # to from balance
    delimited = transaction.split(" ")
    toAccount = delimited[1]
    fromAccount = delimited[2]
    amount = delimited[3]

    # Validation cases
    if login == 0:              # If not logged in, error
        file.write("You are not logged in.")
        file.close()
    elif len(toAccount) != 7 or not toAccount.isdigit():    # If accout number not proper, error
        file.write("Invalid account number.")
        file.close()
    elif len(fromAccount) != 7 or not fromAccount.isdigit():    # If accout number not proper, error
        file.write("Invalid account number.")
        file.close()
    elif toAccount not in listOfAccounts or fromAccount not in listOfAccounts:   # Make sure account exists
        file.write("Account does not exist.")
        file.close()
    elif not amount.isdigit():                          # If amount not proper, error
        file.write("Amount is not a valid amount.")
        file.close()
    elif (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99): # Enforce limit
        file.write("Over withdrawal limit.")
        file.close()
    elif login == 1 and amount > 5000:                  # Daily limit: TODO
        file.write("Amount is not a valid amount.")
        file.close()
    else
        file.write("XFR "+toAccount+" "+amount+" "+fromAccount" name")

    return True

def createacct(transaction, listOfAccounts):
    # NEW to amount from name
    file = open(outputFile, "w+")
    delimited = transaction.split(" ")

    acctNum = delimited[1]
    amount = delimited[2]
    name = delimited[3]

    # Validation cases
    if login == 0:              # If not logged in, error
        file.write("You are not logged in.")
        file.close()
    elif login == 1:
        file.write("Not priviledged for this command")
    elif len(acctNum) != 7 or not acctNum.isdigit():    # If accout number not proper, error
        file.write("Invalid account number.")
        file.close()
    else
        file.write("NEW "+acctNum+" 0000 "+name)
        listOfAccounts.append(acctNum)

    return listOfAccounts

def deleteacct(transaction, listOfAccounts):

    file = open(outputFile, "w+")
    delimited = transaction.split(" ")

    acctNum = delimited[1]
    amount = delimited[2]
    name = delimited[3]

    # Validation cases
    if login == 0:              # If not logged in, error
        file.write("You are not logged in.")
        file.close()
    elif login == 1:
        file.write("Not priviledged for this command")
    elif len(acctNum) != 7 or not acctNum.isdigit():    # If accout number not proper, error
        file.write("Invalid account number.")
        file.close()
    elif acctNum not in listOfAccounts:    # Make sure account exists
        file.write("Account does not exist.")
        file.close()
    else
        file.write("DEL "+acctNum+" 0000 "+name)
        listOfAccounts.remove(acctNum)

    return listOfAccounts


def main():

    accounts = readValidAccounts("your_account_list_file.txt")
    transactions = readInTransactions("your_transaction_summary.txt")
    outpufFile = "transactionSummary.txt"  #TODO
    loginState = 0
    numOfTransactions = len(transactions)
    i = 0
    while i <= numOfTransactions:
        current = transactions[i]
        line = current.split(" ")
        if line[0] == "login":
            loginState = login(current, accounts, login, outputFile)
        elif line[0] == "logout":
            loginState = logout(current, accounts, login, outputFile)
        elif line[0] == "deposit":
            deposit(current, accounts, loginState, outputFile)
        elif line[0] == "withdrawal":
            withdrawal(current, accounts, loginState, outputFile)
        elif line[0] == "transfer":
            transfer(current, accounts, loginState, outputFile)
        elif line[0] == "createacct":
            accounts = createacct(current, accounts, loginState, outputFile)
        elif line[0] == "deleteacct":
            accounts = deleteacct(current, accounts, loginState, outputFile)

        print("Program Finished.")
