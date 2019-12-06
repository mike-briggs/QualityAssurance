import subprocess
import os

    class FileNames():
        DAILY_FOLDER_PREFIX = 'D'
        NO_VALID_ACCOUNTS_FILE_INDICATOR = '.no_valid_accounts'
        VALID_ACCOUNTS_FILE = 'valid_accounts.txt'
        INPUT_FILE_SUFFIX = '.input.txt'
        ACTUAL_OUTPUT_FILE_SUFFIX = '.out.actual.txt'
        EXPECTED_NONE_OUTPUT_FILE = 'none.out.expected.txt'
        EXPECTED_OUTPUT_FILE_SUFFIX = '.out.expected.txt'
        ACTUAL_CONSOLE_FILE_SUFFIX = '.console.actual.txt'
        EXPECTED_CONSOLE_FILE_SUFFIX = '.console.expected.txt'

    for currentDirectoryGenerator in os.walk("."):

        # Get the current directory name
        currentDirectory = currentDirectoryGenerator[0]

        # If this is a test case directory
        if(FileNames.TESTCASE_FOLDER_PREFIX in currentDirectory):
            
            # Split the directory name to get separate folder names
            currentDirectory = currentDirectory.replace('\\', '/')
            directoryNames = currentDirectory.split('/')[1:]
            
            # Get the current requirement and test case from folders
            currentRequirementName = directoryNames[0]
            currentTestCaseName = directoryNames[1]
            currentTestName = currentRequirementName + currentTestCaseName

            # Try to extract requirement and testcase number
            try:
                currentRequirementNumber = int(currentRequirementName[1:])
                currentTestCaseNumber = int(currentTestCaseName[1:])

                # If everything is valid, append current testcase to list of testcases to potentially run
                testcaseIdentifiers.append(
                    (currentRequirementNumber, currentTestCaseNumber, currentTestName, currentDirectory)
                )
            except:
                pass # TODO: print error

    currentRequirementName = directoryNames[0]
    currentTestCaseName = directoryNames[1]
    currentTestName = currentRequirementName + currentTestCaseName
    inputFileName = currentDirectory + '/' + currentTestName + FileNames.INPUT_FILE_SUFFIX


    currentInputLines = ''
    with open(inputFileName, 'r') as inputFile:
        currentInputLines = inputFile.read()

    # Run the frontend script and get the output
    # If it takes longer than a set timeout value to complete, kill it
    frontendOutput = ''
    try:
        frontendProcess = subprocess.run(
            currentCommandToRun,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            input=currentInputLines,
            universal_newlines=True,
            timeout=PROCESS_TIMEOUT
        )
        frontendOutput = frontendProcess.stdout
    except subprocess.TimeoutExpired:
        pass
