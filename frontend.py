import json
from classes import Account


def readValidAccounts(filename):

    masterAccountsList = []                      # initialize master list of accounts

    accountsFile = open(filename, "r")      # read the file

    # get number of lines in the file
    numLinesInFile = sum(1 for line in open(filename))

    # for every line in the file
    for i in numLinesInFile:

        line = accountsFile.readline()               # read line
        delimited = line.split(" ")                  # split line by delimiter
        number = delimited[0]                        # get name from number
        balance = delimited[1]                       # get name from balance
        name = delimited[2]                          # get name from line

        newAccount = Account(name, number, balance)  # create new account

        # append new account to master list
        masterAccountsList.append(newAccount)

    accountsFile.close()

    return masterAccountsList


def readInTransactions(filename):
    masterTransactionsList = []

    transactionsFile = open(filename, "r")

    numLinesInFile = sum(1 for line in open(filename))

    for i in numLinesInFile:

    return masterTransactionsList
