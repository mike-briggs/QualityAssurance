# backend.py
# handles all (merged) transactions once a day
import sys

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

# Define in and output paths
inMasterAccountListPath = sys.argv[1]
inTransactionListPath = sys.argv[2]
outMasterAccountListPath = sys.argv[3]
outValidAccountListPath = sys.argv[4]

# Define working variables
MasterAccountList = [];
ValidAccountList = [];
TransactionList = [];

class Account(self, accountNumber, balance, name):
    self.accountNumber = accountNumber
    self.balance = balance
    self.name = name

def parseMasterAccounts(filepath):
    masterAccountList = []
    with open(filepath) as f:
        masterAccountList = f.readlines()
        # stores each line (account number) in list
        for i in masterAccountList:
            line = masterAccountList[i].split()
            masterAccountSList[i] = new Account(line[0].strip(), line[1].split(), line[2].split())

    # return list of valid accounts
    return masterAccountList

# returns list (array) of valid accounts
def parseValidAccounts(filepath):
    validAccountList = []
    with open(filepath) as f:
        validAccountList = f.readlines()
        # stores each line (account number) in list
        validAccountList = [x.strip() for x in validAccountList]

    # return list of valid accounts
    return validAccountList

def deposit(accountNumber, amount)

def withdraw(accountNumber, amount)

def transfer(toAccountNumber, amount, fromAccountNumber)

def createacct(accountNumber, accountName)

def deleteacct(accountNumber, accountName)

# Main
# Iterate through all Transactions
for (int i=0; i < len(TransactionList); i++)
    current = TransactionList[i].split(" ")
    # 000 1111111 222 3333333 4444
    # TYP accntTo amt accntFr name
    if current[0] == "DEP"      # Deposit
        deposit(current[1], current[2])

    elif current[0] == "WDR"    # Withdraw
        withdraw(current[1], current[2])

    elif current[0] == "XFR"    # Transfer
        transfer(current[1], current[2], current[3])

    elif current[0] == "NEW"    # Create account
        createacct(current[1], current[4])

    elif current[0] == "DEL"    # Delete account
        deleteacct(current[1], current[4])

