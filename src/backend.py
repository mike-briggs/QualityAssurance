# backend.py
# handles all (merged) transactions once a day


# Inputs:
#   - Transaction summary file (merged from several)
#   - Previous instance of Master Account List
# Outputs:
#   - New instance of Master Account List
#   - New Valid Accunts List for next set of frontends


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
