import subprocess
import os
import sys


class FileNames():
    DAILY_FOLDER_PREFIX = 'T'
    NO_VALID_ACCOUNTS_FILE_INDICATOR = '.no_valid_accounts'
    VALID_ACCOUNTS_FILE = 'valid_accounts.txt'
    INPUT_FILE_SUFFIX = '.txt'
    OUTPUT_FILE_SUFFIX = '.out.txt'
    EXPECTED_NONE_OUTPUT_FILE = 'none.out.expected.txt'
    EXPECTED_OUTPUT_FILE_SUFFIX = '.out.expected.txt'
    ACTUAL_CONSOLE_FILE_SUFFIX = '.console.actual.txt'
    EXPECTED_CONSOLE_FILE_SUFFIX = '.console.expected.txt'


currentDay = 1
day = sys.argv[1]

#currentDirectory = sys.argv[1]
path = './D%s/'%(day)
for currentDirectoryGenerator in os.walk(path):

    # Get the current directory name
    currentDirectory = currentDirectoryGenerator[0]
    print(currentDirectory)
    # If this is a day directory
    if(FileNames.DAILY_FOLDER_PREFIX in currentDirectory):

        # Split the directory name to get separate folder names
        currentDirectory = currentDirectory.replace('\\', '/')
        directoryNames = currentDirectory.split('/')[1:]

        # Get the current requirement and test case from folders
        currentRequirementName = directoryNames[0]
        currentTestCaseName = directoryNames[1]
        currentTestName = currentRequirementName + currentTestCaseName

        # SEPARATE DAILY SESSIONS
        # In folder structure DxTx currentRequirementName[1] = D(x)
        # ex. D1 : currentRequirementName[1] = 1
        #     D4 : currentRequirementName[1] = 4

        # Check if we need to run backend: no more files in Dx/T1...Dx/T4
        # Keep track of current session number, and if there are no more files
        # after that session number, call backend

        lastElement = currentDirectory[len(currentDirectory)-1]
        # print(lastElement)
        temp = currentDirectory[:-1]
        nextElement = int(lastElement) + 1
        nextElement = str(nextElement)
        nextPath = temp + nextElement
        #print(nextPath) 
        
        if(not os.path.exists(nextPath)):
            
            currentCommandToRun = ['python'] + ['backend.py'] + [str(day)]
            #call backend because next session does not exist
            try:
                backendProcess = subprocess.run(currentCommandToRun)
                currentDay = currentDay + 1
                
            
            except subprocess.TimeoutExpired:
                pass

        
        currentTestName = currentRequirementName + currentTestCaseName
        inputFileName = currentDirectory + '/' + currentTestName + FileNames.INPUT_FILE_SUFFIX
        outputFileName = currentDirectory + '/' + currentTestName + FileNames.OUTPUT_FILE_SUFFIX
        #print(inputFileName)
        #print(outputFileName)

        currentInputLines = ''
        with open(inputFileName, 'r') as inputFile:
            currentInputLines = inputFile.read()
        currentCommandToRun = ['python'] + ['frontend.py'] + ['valid_accounts.txt'] + [outputFileName]
        # Run the frontend script and get the output
        # If it takes longer than a set timeout value to complete, kill it
        frontendOutput = ''
        try:
            frontendProcess = subprocess.run(
                currentCommandToRun,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                input=currentInputLines,
                universal_newlines=True
                
            )
            frontendOutput = frontendProcess.stdout
            
        except subprocess.TimeoutExpired:
            pass
