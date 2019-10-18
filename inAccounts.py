import json
import classes

accountsFile = open("your_accounts_list.txt", "r")
num_lines_in_file = sum(1 for line in open('your_accounts_list.txt'))

for i in num_lines_in_file:
    line = accountsFile.readline()
    delimited = line.split(" ")
    accountNumber = delimited[0]
    accountBalance = delimited[1]
    accountName = delimited[2]

    masterAccountsList = []
    masterAccountsList.append(
        account(accountNumber, accountName, accountBalance))


accountsFile.close()
