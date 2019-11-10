# backend.py
# handles all (merged) transactions once a day
import sys
import os

# Inputs:
#   - Transaction summary file (merged from several)
#   - Previous instance of Master Account List
#       AAAAAAA MMMMM NNNN
#       acctNum money name
# Outputs:
#   - New instance of Master Account List
#       AAAAAAA MMMMM NNNN
#       acctNum money name
#   - New Valid Accunts List for next set of frontends
#       AAAAAAA
#       acctNum


# Backend
#   Read in previous Master Account list and store in local data structure
#   Format coming in: AAAAAAA MMMMM NNNN
#                     acctnum money name
#   Read in transaction summary file and store in local data structure
#   Go through each transaction
#       Ensure transaction is valid
#       Perform transaction by updating master account List
#   Create new valid accounts list from Master
#   Output valid accounts and master accounts

# Used to help store the master accounts list
class Account(self, accountNumber, balance, name):
    self.accountNumber = accountNumber
    self.balance = balance
    self.name = name

# returns a list of account objects
def parseMasterAccounts(filepath):
    masterAccountList = []
    with open(filepath) as f:
        masterAccountList = f.readlines()
        # stores each line (account number) in list
        for i in masterAccountList:
            line = masterAccountList[i].split(" ")
            masterAccountList[i] = new Account(line[0].strip(), line[1].strip(), line[2].strip())

    # return list of valid accounts
    return masterAccountList

# Deposit Money into an account
def deposit(accountList, accountNumber, amount):
    accountList[accountList.index(accountNumber)].balance += amount

# Withdraw money from an account
# TODO: make sure account has enough Money
# figure out if we have to enforce daily limits
def withdraw(accountList, accountNumber, amount):
    accountList[accountList.index(accountNumber)].balance -= amount

# Transfer money from on account to another
# TODO: make sure account has enough money
def transfer(accountList, toAccountNumber, amount, fromAccountNumber):
    accountList[accountList.index(toAccountNumber)].balance += amount
    accountList[accountList.index(fromAccountNumber)].balance += amount

# Create a new account
# TODO: Make sure accountnumber is unique
def createacct(accountList, accountNumber, accountName):
    accountList.append(new Account(accountNumber, 0, accountName))

# Delete an account
def deleteacct(accountList, accountNumber, accountName):
    accountList.remove(accountNumber)

#
# MAIN
#
# Define input and output file paths
inMasterAccountListPath = sys.argv[1]
inTransactionListPath = sys.argv[2]
outMasterAccountListPath = sys.argv[3]
outValidAccountListPath = sys.argv[4]

# Define working variables
MasterAccountList = parseMasterAccounts(inMasterAccountListPath) # master list of accounts and balances
ValidAccountList = []
TransactionList = []

# Iterate through all Transactions
for i in TransactionList
    # Split each transaction into its arguments
    current = TransactionList[i].split(" ")
    # 000 1111111 222 3333333 4444
    # TYP accntTo amt accntFr name
    if current[0] == "DEP"      # Deposit
        deposit(MasterAccountList, current[1], current[2])

    elif current[0] == "WDR"    # Withdraw
        withdraw(MasterAccountList, current[1], current[2])

    elif current[0] == "XFR"    # Transfer
        transfer(MasterAccountList, current[1], current[2], current[3])

    elif current[0] == "NEW"    # Create account
        createacct(MasterAccountList, current[1], current[4])

    elif current[0] == "DEL"    # Delete account
        deleteacct(MasterAccountList, current[1], current[4])

