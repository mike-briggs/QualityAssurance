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
class Account:
    def __init__(self, accountNumber, balance, name):
        self.accountNumber = accountNumber
        self.balance = balance
        self.name = name

    

# returns a list of account objects

def toString(acc_num, bal, name):
        return str(acc_num+" "+bal+" "+name)


def parseMasterAccounts(filepath):
    masterAccountList = []
    with open(filepath) as f:
        masterAccountList = f.readlines()
        length = len(masterAccountList)
        # stores each line (account number) in list
        for i in range(length):
            line = masterAccountList[i].split(" ")
            masterAccountList[i] = Account(line[0].strip(), line[1].strip(), line[2].strip())

    # return list of valid accounts
    return masterAccountList

def parseTransactionList(filepath):
    transactionList = []
    with open(filepath) as f:
        transactionList = f.readlines()
        #length = len(transactionList)
        # stores each line (account number) in list
        #for i in range(length):
        #    line = transactionList[i].split(" ")
        #    transactionList[i] = Account(line[0].strip(), line[1].strip(), line[2].strip())

    # return list of valid accounts
    return transactionList


# Deposit Money into an account
def deposit(accountList, inputAccountNumber, inputAmount):
    accountList[accountList.index(inputAccountNumber)].balance += inputAmount
    return True

# Withdraw money from an account
# figure out if we have to enforce daily limits
def withdraw(accountList, inputAccountNumber, inputAmount):
    inputAccount = accountList[accountList.index(inputAccountNumber)]
    if(float(inputAccount.balance) >= float(inputAmount)):
        inputAccount.balance -= inputAmount
        return True
    else:
        # Insufficient funds
        return False

# Transfer money from on account to another
def transfer(accountList, toAccountNumber, inputAmount, fromAccountNumber):
    fromAccount = accountList[accountList.index(fromAccountNumber)]
    toAccount = accountList[accountList.index(toAccountNumber)]
    if(float(fromAccount.balance) >= float(inputAmount)):
        toAccount.balance += inputAmount
        fromAccount.balance -= inputAmount
        return True
    else:
        # Insufficient funds
        return False

# Create a new account
def createacct(accountList, inputAccountNumber, accountName):
    accountList.append(Account(inputAccountNumber, 0, accountName))
    return True

# Delete an account
def deleteacct(accountList, inputAccountNumber, accountName):
    accountList.remove(inputAccountNumber)
    return True

def sortByAccount(a):
    return a.accountNumber

#
# MAIN
#
## INPUTS
# Define input and output file paths
inMasterAccountListPath     = sys.argv[1]
inTransactionListPath       = sys.argv[2]
outMasterAccountListPath    = sys.argv[3]
outValidAccountListPath     = sys.argv[4]

# Define working variables
MasterAccountList   = parseMasterAccounts(inMasterAccountListPath) # master list of accounts and balances
TransactionList     = parseTransactionList(inTransactionListPath)        # list of incoming transactions

## TRANSACTIONS
length3 = len(TransactionList)
# Iterate through all Transactions
for i in range(length3):
    # Split each transaction into its arguments
    current = TransactionList[i].split(" ")
    # 000 1111111 222 3333333 4444
    # TYP accntTo amt accntFr name
    if current[0] == "DEP"  :    # Deposit
        deposit(MasterAccountList, current[1], current[2])

    elif current[0] == "WDR"    :# Withdraw
        withdraw(MasterAccountList, current[1], current[2])

    elif current[0] == "XFR" :   # Transfer
        transfer(MasterAccountList, current[1], current[2], current[3])

    elif current[0] == "NEW" :   # Create account
        createacct(MasterAccountList, current[1], current[4])

    elif current[0] == "DEL" :   # Delete account
        deleteacct(MasterAccountList, current[1], current[4])

## OUTPUTS
# Sort master list by account number
MasterAccountList.sort(key=sortByAccount)
length2 = len(MasterAccountList)
# For each account
for i in range(length2):
    # Write to Master Account List
    with open(outMasterAccountListPath, 'a') as wf:
        wf.write(toString(MasterAccountList[i].accountNumber,MasterAccountList[i].balance,MasterAccountList[i].name)) # Write to file
        if(i != len(MasterAccountList) -1):
            wf.write("\n")
    # Write to Valid ACcount List
    with open(outValidAccountListPath, 'a') as wf:
        wf.write(MasterAccountList[i].accountNumber) # Write to file
        if(i != len(MasterAccountList) -1):
            wf.write("\n")


