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
    masterTransactionsList = []

    transactionsFile = open(filename, "r")

    numLinesInFile = sum(1 for line in open(filename))

    for i in numLinesInFile:
        line = transactionsFile.readline()
        masterTransactionsList.append(line)

    return masterTransactionsList


def login(transaction, listOfAccounts):

    return True


def logout(transaction, listOfAccounts):

    return True


def deposit(transaction, listOfAccounts, login, outputFile):
    delimited = transaction.split(" ")
    acctNum = delimited[1]
    amount = delimited[2]

    file = open(outputFile, "w+")

    # Validation cases
    if login == 0:
        file.write("You are not logged in.")

        file.close()
        return False

    if len(acctNum) != 7 or not acctNum.isdigit():
        file.write("Invalid account number.")

        file.close()
        return False

    if acctNum not in listOfAccounts:
        file.write("Withdrawal account does not exist.")

        file.close()
        return False

    if not amount.isdigit():
        file.write("Amount is not a valid amount.")

        file.close()
        return False

    if (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):
        file.write("Over withdrawal limit.")

        file.close()
        return False

    return True


def withdrawal(transaction, listOfAccounts, login, outputFile):
    delimited = transaction.split(" ")
    acctNum = delimited[1]
    amount = delimited[2]

    file = open(outputFile, "w+")

    # Validation cases
    if login == 0:
        file.write("You are not logged in.")

        file.close()
        return False

    if len(acctNum) != 7 or not acctNum.isdigit():
        file.write("Invalid account number.")

        file.close()
        return False

    if acctNum not in listOfAccounts:
        file.write("Withdrawal account does not exist.")

        file.close()
        return False

    if not amount.isdigit():
        file.write("Amount is not a valid amount.")

        file.close()
        return False

    if (login == 1 and amount > 1000) or (login == 2 and amount > 999999.99):
        file.write("Over withdrawal limit.")

        file.close()
        return False

    # NOT FINISHED CHECK OVER DAILY LIMIT ##################################################
    if login == 1 and amount > 5000:
        file.write("Amount is not a valid amount.")

        file.close()
        return False

    file.write("WDR "+acctNum+" "+amount+" 0000000 name")

    return True


def transfer(transaction, listOfAccounts):

    return True


def createacct(transaction, listOfAccounts):

    return True


def deleteacct(transaction, listOfAccounts):

    # delete the accout number from list of accounts

    return listOfAccounts


def main():
    # array of strings
    accounts = readValidAccounts("your_account_list_file.txt")

    # array of strings
    transactions = readInTransactions("your_transaction_summary.txt")
    loginState = 0
    numOfTransactions = len(transactions)
    i = 0
    while i <= numOfTransactions:
        current = transactions[i]
        line = current.split(" ")
        if line[0] == "login":
            login(current, accounts)
        elif line[0] == "logout":
            logout(current, accounts)
        elif line[0] == "deposit":
            deposit(current, accounts)
        elif line[0] == "withdrawal":
            withdrawal(current, accounts)
        elif line[0] == "transfer":
            transfer(current, accounts)
        elif line[0] == "createacct":
            accounts = createacct(current, accounts)
        elif line[0] == "deleteacct":
            accounts = deleteacct(current, accounts)


print("Program Finished.")
