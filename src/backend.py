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

    def toString(self):
        return self.accountNumber+" "+str(self.balance)+" "+self.name

# returns a list of account objects
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

# returns a list of transactions
def parseTransactionList(filepath):
    transactionList = []
    with open(filepath) as f:
        transactionList = f.readlines()

    # return list of transactions
    return transactionList

# Deposit Money into an account
def deposit(accountList, inputAccountNumber, inputAmount):
    for j in range(len(accountList)):
        if accountList[j].accountNumber == inputAccountNumber:  #if found,
            accountList[j].balance = int(accountList[j].balance) + int(inputAmount)
            return True

# Withdraw money from an account
# figure out if we have to enforce daily limits
def withdraw(accountList, inputAccountNumber, inputAmount):
    for j in range(len(accountList)):
        if accountList[j].accountNumber == inputAccountNumber:
            if int(accountList[j].balance) >= int(inputAmount):
                accountList[j].balance = int(accountList[j].balance) - int(inputAmount)
                return True

# Transfer money from on account to another
def transfer(accountList, toAccountNumber, inputAmount, fromAccountNumber):
    for j in range(len(accountList)):
        if accountList[j].accountNumber == toAccountNumber:
            toAccount = accountList[j].accountNumber
            toIndex = j;
        if accountList[j].accountNumber == fromAccountNumber:
            fromAccount = accountList[j].accountNumber
            fromIndex = j;

    if fromAccount >= inputAmount:
        accountList[toIndex].balance = int(accountList[toIndex].balance) + int(inputAmount)
        accountList[fromIndex].balance = int(accountList[fromIndex].balance) - int(inputAmount)

# Create a new account
def createacct(accountList, inputAccountNumber, accountName):
    accountList.append(Account(inputAccountNumber, 0, accountName))
    return True

# Delete an account
def deleteacct(accountList, inputAccountNumber, accountName):
    for j in range(len(accountList)):
        if accountList[j].accountNumber == inputAccountNumber:
            accountList.remove(accountList[j])
            return True

def sortByAccount(a):
    return a.accountNumber


inMasterAccountListPath = sys.argv[1] # master_accounts.txt
inTransactionListPath = sys.argv[2] # merge2.txt
outMasterAccountListPath = sys.argv[3]  # master_accounts_out.txt
outValidAccountListPath = sys.argv[4]   # valid_accounts_out.txt

MasterAccountList = parseMasterAccounts(inMasterAccountListPath)
TransactionList = parseTransactionList(inTransactionListPath)


# Put account numbers into dictionary, key=index of obj
allAccountNums = {}
for i in range(len(MasterAccountList)):
    allAccountNums[i] = MasterAccountList[i]

## TRANSACTIONS
# Iterate through all Transactions
for i in range(1,len(TransactionList)):
    current = TransactionList[i].split()    # Split each transaction into its arguments
    # 000 1111111 222 3333333 4444
    # TYP accntTo amt accntFr name
    if current[0] == "DEP":      # Deposit
        deposit(MasterAccountList, current[1], current[2])

    elif current[0] == "WDR":    # Withdraw
        withdraw(MasterAccountList, current[1], current[2])

    elif current[0] == "XFR":    # Transfer
        transfer(MasterAccountList, current[1], current[2], current[3])

    elif current[0] == "NEW":    # Create account
        createacct(MasterAccountList, current[1], current[4])

    elif current[0] == "DEL":    # Delete account
        deleteacct(MasterAccountList, current[1], current[4])
    
    elif current[0] == "EOS":    # End of session
        print("EOS")



## OUTPUTS

# Clear previous data in output files, will be overwritten anyways
open(outMasterAccountListPath, 'w').close()
open(outValidAccountListPath, 'w').close()

# For each account
for i in range(len(MasterAccountList)):
    # Write to Master Account List
    with open(outMasterAccountListPath, 'a') as wf:
        wf.write(MasterAccountList[i].toString()) # Write to file
        if(i != len(MasterAccountList) -1):
            wf.write("\n")
    # Write to Valid ACcount List
    with open(outValidAccountListPath, 'a') as wf:
        wf.write(MasterAccountList[i].accountNumber) # Write to file
        if(i != len(MasterAccountList) -1):
            wf.write("\n")