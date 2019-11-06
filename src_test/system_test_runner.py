#!/usr/bin/python3

# ======================== IMPORTS ========================

import os                                       # For checking if files exist
import re                                       # For removing ANSI sequences
import sys                                      # For exiting with return code
import difflib                                  # For getting differences in files
import filecmp                                  # For comparing if files are the same
import argparse                                 # For parsing arguments & help message
import subprocess                               # For running frontend script
from enum import Enum                           # For enum helper classes               
from datetime import datetime                   # For timing how long testing takes

# Try to import colorama (required on Windows),
# but fall back to not using it if not found
useColorama = True
try:
    from colorama import init, Fore, Style      # For coloured console output on Windows
except ImportError:
    useColorama = False

# ======================== CONSTANTS ========================

# Terminal output colours
ALL_OFF =           '\033[0m' if not useColorama else Style.RESET_ALL
BOLD =              '\033[1m' if not useColorama else Style.BRIGHT
FG_RED =            '\033[91m' if not useColorama else Fore.LIGHTRED_EX
FG_GREEN =          '\033[92m' if not useColorama else Fore.LIGHTGREEN_EX
FG_YELLOW =         '\033[93m' if not useColorama else Fore.LIGHTYELLOW_EX
FG_BLUE =           '\033[94m' if not useColorama else Fore.LIGHTBLUE_EX
FG_MAGENTA =        '\033[95m' if not useColorama else Fore.LIGHTMAGENTA_EX
FG_CYAN =           '\033[96m' if not useColorama else Fore.LIGHTCYAN_EX

# Helper class containing all the messages that will be printed out
class Strings():
    WARNING = Fore.YELLOW + 'Warning' + Style.RESET_ALL + ': '
    ERROR = Fore.RED + 'Error' + Style.RESET_ALL + ': '

    RUNNING_TESTCASE_START = Fore.CYAN + Style.BRIGHT + '\n========== Running test '
    RUNNING_TESTCASE_END = ' ==========\n'

    FINISHED_TESTING = '\n========== COMPLETED ALL TESTS ==========\n' + ALL_OFF
    ELAPSED_TIME =  'Took:    '
    RAN_TESTS =     'Ran:     '
    SKIPPED_TESTS = 'Skipped: '
    PASSED_TESTS =  'Passed:  '
    FAILED_TESTS =  'Failed:  '
    
    RUNNING = Fore.MAGENTA + 'Running' + Style.RESET_ALL + ': '
    STATUS = '\nStatus: '
    CONSOLE_DIFFERENCES = Fore.BLUE + '\nConsole output differences' + Style.RESET_ALL + ': '
    OUTPUT_DIFFERENCES = Fore.BLUE + '\nTransaction summary file differences' + Style.RESET_ALL + ': '
    TRAILING_NEWLINE = '<trailing newline>'

    ERROR_SKIPPING_TEST_CASE = 'skipping this test case...'
    ERROR_NO_INPUT_FILE = 'Cannot find input file: '
    ERROR_NO_ACTUAL_OUTPUT_FILE = 'Cannot find actual output file (was not generated by script being tested): '
    ERROR_NO_EXPECTED_OUTPUT_FILE = 'Cannot find expected output file: '
    ERROR_NO_EXPECTED_CONSOLE_OUTPUT_FILE = 'Cannot find expected console output file: '
    ERROR_NO_TESTCASE_FOUND = 'The specified test case to run was not found: '

# Helper class containing all the file constants
class FileNames():
    TESTCASE_FOLDER_PREFIX = 'T'
    NO_VALID_ACCOUNTS_FILE_INDICATOR = '.no_valid_accounts'
    VALID_ACCOUNTS_FILE = 'valid_accounts.txt'
    INPUT_FILE_SUFFIX = '.input.txt'
    ACTUAL_OUTPUT_FILE_SUFFIX = '.out.actual.txt'
    EXPECTED_NONE_OUTPUT_FILE = 'none.out.expected.txt'
    EXPECTED_OUTPUT_FILE_SUFFIX = '.out.expected.txt'
    ACTUAL_CONSOLE_FILE_SUFFIX = '.console.actual.txt'
    EXPECTED_CONSOLE_FILE_SUFFIX = '.console.expected.txt'

# Helper class containing the type of possible test results
class TestResult(Enum):
    NO_RESULT = Fore.YELLOW + 'No result'
    PASSED = Fore.GREEN + 'Passed'
    FAILED_OUTPUT = Fore.RED + 'Failed' + Style.RESET_ALL + ' (transaction summary file differs)'
    FAILED_CONSOLE_OUTPUT = Fore.RED + 'Failed' + Style.RESET_ALL + ' (console output differs)'
    FAILED_BOTH = Fore.RED + 'Failed' + Style.RESET_ALL + ' (both transaction summary file & console output differ)'

# Helper class containing the possible output printing modes
class PrintoutModes(Enum):
    ALL = 'all'
    FAILED = 'failed'
    NONE = 'none'
class PrintoutModesHelp(Enum):
    ALL = 'all: All the test case results are printed'
    FAILED = 'failed: Only results of failed test cases are printed'
    NONE = 'none: Nothing is printed (this mode is for mutation testing)'

# The commad to run for executing the script to test
FRONTEND_COMMAND = ['python'] if os.name == 'nt' else ['python3']

# Regex for removing ANSI sequences (for coloured output) from console output
# This is required to save console output as plain text into files
# From: https://stackoverflow.com/a/14693789
ansi_escape = re.compile(r'''
    \x1B    # ESC
    [@-_]   # 7-bit C1 Fe
    [0-?]*  # Parameter bytes
    [ -/]*  # Intermediate bytes
    [@-~]   # Final byte
''', re.VERBOSE)

# Maximum time the script to test can run for (in seconds)
PROCESS_TIMEOUT = 3

# ======================== COMMAND LINE ARGUMENTS ========================

# The path & name of the script to be tested
scriptToTestFileName = None

# Amount of surrounding lines to include for context in diff output
numberOfContextLinesForDiff = 1

# Automatically delete generated output files after test case is done,
# if this is false all the generated output files are kept
discardActualOutputFiles = False

# The type out output that will be printed
printoutMode = PrintoutModes.ALL

# List of test cases to run (by RxTy names),
# if this is None, all test cases are run
namesOfTestcasesToRun = None

# ======================== FILE HELPER FUNCTIONS ========================

# Return true if the given file exists and it is actually a file (i.e. not a folder)
def check_file_exists(fileName):
    return os.path.exists(fileName) and os.path.isfile(fileName)

# Delete the existing actual output files if they exist from any previous runs
def delete_output_files(outputFileName, consoleOutputFileName):
    if(check_file_exists(outputFileName)):
        os.remove(outputFileName)
    if(check_file_exists(consoleOutputFileName)):
        os.remove(consoleOutputFileName)

# ======================== PRINT HELPER FUNCTIONS ========================

# Print "Status" followed by a message
def print_status_message(message):
    print(Strings.STATUS + Style.BRIGHT + message)

# Print "Error" in red followed by a message
def print_error_message(message):
    print(Strings.ERROR + message)

# Print "Warning" in yellow followed by a message
def print_warning_message(message):
    print(Strings.WARNING + message)

# Print "Running test RxTy" in cyan
def print_running_testcase_message(currentTestName):
    print(Strings.RUNNING_TESTCASE_START + currentTestName + Strings.RUNNING_TESTCASE_END)

# Print "Running" in magenta followed by a the command will currently be ran
def print_running_command_message(message):
    print(Strings.RUNNING + ' '.join(message) + ALL_OFF)

# Print test statistics after testcases are completed
def print_test_statistics(total, skipped, passed, failed, startTime):
    
    headerColor = BOLD + (FG_RED if failed > 0 else (FG_GREEN if passed > 0 else FG_YELLOW))
    elapsedTime = datetime.now() - startTime
    percentPassed = round(passed / total * 100) if total > 0 else 0
    percentFailed = round(failed / total * 100) if total > 0 else 0

    print(headerColor + Strings.FINISHED_TESTING + ALL_OFF)
    print(Strings.ELAPSED_TIME + str(elapsedTime) + ALL_OFF)
    print(Strings.RAN_TESTS + FG_CYAN + str(total) + ALL_OFF)
    print(Strings.SKIPPED_TESTS + ('0' if skipped == 0 else FG_YELLOW + str(skipped)) + ALL_OFF)
    print(Strings.PASSED_TESTS + ('0' if passed == 0 else FG_GREEN + str(passed) + ' = ' + str(percentPassed) + '%') + ALL_OFF)
    print(Strings.FAILED_TESTS + ('0' if failed == 0 else FG_RED + str(failed) + ' = ' + str(percentFailed) + '%') + ALL_OFF + '\n')

# Print line-by-line differences in two files
def print_file_differences(fileName1, fileName2, headerText):

    # Open first file to read all lines from it
    file1Lines = ''
    with open(fileName1, 'r') as file1:
        file1Lines = file1.read()

    # Replace trailing newline with explicit text so it can be seen in diff output
    if(file1Lines.endswith('\n')):
        file1Lines = file1Lines + Strings.TRAILING_NEWLINE       
        
    # Open second file to read all lines from it
    file2Lines = ''
    with open(fileName2, 'r') as file2:
        file2Lines = file2.read()

    # Replace trailing newline with explicit text so it can be seen in diff output
    if(file2Lines.endswith('\n')):
        file2Lines = file2Lines + Strings.TRAILING_NEWLINE  

    # Get the line-by-line differences b/w the files
    differingLines = difflib.unified_diff(file1Lines.splitlines(), file2Lines.splitlines(), lineterm='New', n=1)

    # Print out all lines that differ in a diff format
    didPrintHeader = False
    for differingLine in differingLines:

        # Print header the first time around
        if(not didPrintHeader):
            print(headerText)
            didPrintHeader = True

        # Remove file names since they are both empty and not required
        for prefix in ('---', '+++'):
            if differingLine.startswith(prefix):
                break
        else:

            # Colour the removals (-) red and the additions (+) green
            if(differingLine.startswith('-')):
                print(Fore.RED + differingLine)
            elif(differingLine.startswith('+')):
                print(Fore.GREEN + differingLine)

            # All other lines are printed as-is
            else:
                print(differingLine)

# ======================== MAIN ========================

# Run all system tests
def main():

    # Counter values
    testsRan = 0
    skippedTests = 0
    passedTests = 0
    failedTests = 0

    # Record time when testing started
    startTime = datetime.now()

    # Test cases to potentially run
    testcaseIdentifiers = []
    
    # ======================== PROCESS ALL TEST CASES ========================

    # Recursively walk down the current directory (system-tests)
    for currentDirectoryGerenrator in os.walk("."):

        # Get the current directory name
        currentDirectory = currentDirectoryGerenrator[0]

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
    
    # For all testcases to potentially run (in increasing sorted order)
    for currentTestcaseIdentifier in sorted(testcaseIdentifiers):

        # If this testcase should be run, try to run it
        if(namesOfTestcasesToRun == None or currentTestcaseIdentifier[2] in namesOfTestcasesToRun):
            
            # Remove the name of this test case from the ones left to run
            if(namesOfTestcasesToRun != None):
                namesOfTestcasesToRun.remove(currentTestcaseIdentifier[2])

            # Setup test case parameter for the current test case being run
            currentTestName = currentTestcaseIdentifier[2]
            currentDirectory = currentTestcaseIdentifier[3]

            # The messages that were printed so far
            didPrintRunningTestCaseMessage = False
            didPrintRunningCommandMessage = False
            didPrintWarningMessage = False

            # Indicate that this test case is being run
            if(printoutMode == PrintoutModes.ALL):
                print_running_testcase_message(currentTestName)
                didPrintRunningTestCaseMessage = True
            
            # ======================== SET INPUT / OUTPUT FILE NAMES ========================

            # By default, the valid accounts file is the common one in the base directory this is being run from (system-tests)
            validAccountsFileName = FileNames.VALID_ACCOUNTS_FILE

            # If a .no_valid_accounts file exists in the current test case folder,
            # a non-existent file is used instead (this function may be needed for some test cases)
            currentLocalValidAccountsFileName = currentDirectory + '/' + FileNames.VALID_ACCOUNTS_FILE
            currentNoValidAccountsFileName = currentDirectory + '/' + FileNames.NO_VALID_ACCOUNTS_FILE_INDICATOR
            if(check_file_exists(currentNoValidAccountsFileName)):
                validAccountsFileName = os.devnull

            # Otherwise, if a local valid accounts file exists in the current test case folder, it is used instead
            elif(check_file_exists(currentLocalValidAccountsFileName)):
                validAccountsFileName = currentLocalValidAccountsFileName
            
            # By default, the expected output file is RxTy.out.expected.txt
            expectedOutputFileName = currentDirectory + '/' + currentTestName + FileNames.EXPECTED_OUTPUT_FILE_SUFFIX
            
            # If the none.out.expected.txt file exists, expect no output file to be created
            isExpectingNoOutputFile = False
            currentExpectedNoneOutputFileName = currentDirectory + '/' + FileNames.EXPECTED_NONE_OUTPUT_FILE
            if(check_file_exists(currentExpectedNoneOutputFileName)):
                expectedOutputFileName = currentExpectedNoneOutputFileName
                isExpectingNoOutputFile = True

            # Construct rest of filenames
            inputFileName = currentDirectory + '/' + currentTestName + FileNames.INPUT_FILE_SUFFIX
            actualOutputFileName = currentDirectory + '/' + currentTestName + FileNames.ACTUAL_OUTPUT_FILE_SUFFIX
            actualConsoleOutputFileName = currentDirectory + '/' + currentTestName + FileNames.ACTUAL_CONSOLE_FILE_SUFFIX
            expectedConsoleOutputFileName = currentDirectory + '/' + currentTestName + FileNames.EXPECTED_CONSOLE_FILE_SUFFIX

            # ======================== CHECK INPUT / OUTPUT FILES EXIST ========================

             # Check that the expected transaction summary output file exists
            expectedOutputFileIsValid = True
            if(not(check_file_exists(expectedOutputFileName))):

                # If not, print error message
                if(printoutMode != PrintoutModes.NONE):
                    if(not didPrintRunningTestCaseMessage):
                        print_running_testcase_message(currentTestName)
                        didPrintRunningTestCaseMessage = True
                    print_warning_message(Strings.ERROR_NO_EXPECTED_OUTPUT_FILE + expectedOutputFileName)
                    didPrintWarningMessage = True
                expectedOutputFileIsValid = False

                # In this case, still continue running the test case

             # Check that the expected console output file exists
            expectedConsoleOutputFileIsValid = True
            if(not(check_file_exists(expectedConsoleOutputFileName))):

                # If not, print error message
                if(printoutMode != PrintoutModes.NONE):
                    if(not didPrintRunningTestCaseMessage):
                        print_running_testcase_message(currentTestName)
                        didPrintRunningTestCaseMessage = True
                    print_warning_message(Strings.ERROR_NO_EXPECTED_CONSOLE_OUTPUT_FILE + expectedConsoleOutputFileName)
                    didPrintWarningMessage = True
                expectedConsoleOutputFileIsValid = False

                # In this case, still continue running the test case

            # Check that the input file exists
            if(not(check_file_exists(inputFileName))):

                # If not, print error message
                if(printoutMode != PrintoutModes.NONE):
                    if(not didPrintRunningTestCaseMessage):
                        print_running_testcase_message(currentTestName)
                        didPrintRunningTestCaseMessage = True
                    print_error_message(Strings.ERROR_NO_INPUT_FILE + inputFileName + ', ' + Strings.ERROR_SKIPPING_TEST_CASE)

                # Skip this test case
                skippedTests = skippedTests + 1
                continue

            # ======================== RUN TEST CASE ========================

            # Otherwise, if the required input file exists for this testcase, run it

            # First, delete the existing actual output files if they exist from any previous runs
            delete_output_files(actualOutputFileName, actualConsoleOutputFileName)

            # Construct the command to be executed & print it out
            currentCommandToRun = FRONTEND_COMMAND + [scriptToTestFileName] + [validAccountsFileName] + [actualOutputFileName]
            if(printoutMode == PrintoutModes.ALL):
                print_running_command_message(currentCommandToRun)
                didPrintRunningCommandMessage = True

            # Open input file and read in all the input lines
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

            # Get the console output
            actualConsoleOutput = ansi_escape.sub('', str(frontendOutput))

            # Open file for actual console output and write actual console output to it
            with open(actualConsoleOutputFileName, 'w') as actualConsoleOutputFile:
                actualConsoleOutputFile.write(actualConsoleOutput)

            # ======================== CHECK RESULTS ========================

            # Check that the actual transaction summary output file was created if required
            actualOutputFileIsValid = False if isExpectingNoOutputFile else True
            if(not(check_file_exists(actualOutputFileName)) and not isExpectingNoOutputFile):

                # If not, print error message
                if(printoutMode != PrintoutModes.NONE):
                    if(not didPrintRunningTestCaseMessage):
                        print_running_testcase_message(currentTestName)
                        didPrintRunningTestCaseMessage = True
                    if(not didPrintRunningCommandMessage):                    
                         print_running_command_message(currentCommandToRun)
                         didPrintRunningCommandMessage = True
                    print_warning_message(Strings.ERROR_NO_ACTUAL_OUTPUT_FILE + actualOutputFileName)
                    didPrintWarningMessage = True
                actualOutputFileIsValid = False

                # In this case, still continue running the test case

            # Initialize the test result as invalid since no comparison has been done yet
            testResult = TestResult.NO_RESULT

            # Check if the actual transaction summary file exists if it is supposed to, if not indicate that the test failed
            if(not actualOutputFileIsValid and not isExpectingNoOutputFile):
                testResult = TestResult.FAILED_OUTPUT
            # If the actual transaction summary file does exist but it is not supposed to, indicate that the test failed
            elif(actualOutputFileIsValid and isExpectingNoOutputFile):
                testResult = TestResult.FAILED_OUTPUT
            # Otherwise, check if transaction summary file is equal to expected output, if not indicate that the test failed
            elif(expectedOutputFileIsValid and actualOutputFileIsValid and not filecmp.cmp(expectedOutputFileName, actualOutputFileName)):
                testResult = TestResult.FAILED_OUTPUT
                
            # Check if console output is equal to expected output, if not indicate that the test failed
            if(expectedConsoleOutputFileIsValid and not filecmp.cmp(expectedConsoleOutputFileName, actualConsoleOutputFileName)):
                testResult = TestResult.FAILED_BOTH if testResult == TestResult.FAILED_OUTPUT else TestResult.FAILED_CONSOLE_OUTPUT

            # Only print out differences if printout mode allows printing
            if(printoutMode != PrintoutModes.NONE):
                if(testResult != TestResult.NO_RESULT):

                    if(not didPrintRunningTestCaseMessage):
                        print_running_testcase_message(currentTestName)
                        didPrintRunningTestCaseMessage = True
                    if(not didPrintRunningCommandMessage):                    
                         print_running_command_message(currentCommandToRun)
                         didPrintRunningCommandMessage = True
                    
                    # If output is not equal to expected output, print all differing lines
                    if(expectedOutputFileIsValid and actualOutputFileIsValid and (testResult == TestResult.FAILED_OUTPUT or testResult == TestResult.FAILED_BOTH)):
                        print_file_differences(expectedOutputFileName, actualOutputFileName, Strings.OUTPUT_DIFFERENCES)

                    # If console output is not equal to expected console output, print all differing lines
                    if(expectedConsoleOutputFileIsValid and (testResult == TestResult.FAILED_CONSOLE_OUTPUT or testResult == TestResult.FAILED_BOTH)):
                        print_file_differences(expectedConsoleOutputFileName, actualConsoleOutputFileName, Strings.CONSOLE_DIFFERENCES)
            
            # If both the expected files exist and there is still no result at this point, this test passed
            if(expectedOutputFileIsValid and expectedConsoleOutputFileIsValid):
                if(testResult == TestResult.NO_RESULT):
                    testResult = TestResult.PASSED

            # Print the result of this test
            if(printoutMode == PrintoutModes.ALL or ((testResult != TestResult.PASSED or didPrintWarningMessage) and printoutMode == PrintoutModes.FAILED)):
                print_status_message(testResult.value)

            # If set, delete the actual output files after test case
            if(discardActualOutputFiles):
                delete_output_files(actualOutputFileName, actualConsoleOutputFileName)

            # Increment test counters
            testsRan = testsRan + 1
            if(testResult == TestResult.PASSED):
                passedTests = passedTests + 1
            else:
                failedTests = failedTests + 1

    
    # ======================== PRINT RESULTS SUMMARY & EXIT ========================

    # If there are any remaining test case names that were not run
    if(namesOfTestcasesToRun != None and len(namesOfTestcasesToRun) > 0):
        print() # Newline

        # Print out a warning message that the test case with tat name was not found
        for currentRemainingTestcaseName in namesOfTestcasesToRun:
            print_warning_message(Strings.ERROR_NO_TESTCASE_FOUND + FG_CYAN + currentRemainingTestcaseName + ALL_OFF)

    # Once all tests are done, print statistics
    if(printoutMode != PrintoutModes.NONE):
        print_test_statistics(testsRan, skippedTests, passedTests, failedTests, startTime)

    # Exit with code 0 if all tests were run and passed, otherwise with 1
    sys.exit(0 if (failedTests + skippedTests) == 0 else 1)

# ======================== RUN ========================

if __name__== "__main__":

    # Initialize terminal colours
    if(useColorama):
        init()

    # Setup arguments parser
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # Add script to test file name arguments
    parser.add_argument('scriptToTestFileName',
    help='The path & name of the script to be tested, can be relative to this script')
    
    parser.add_argument('-c', '--contextDiffLines', type=int,
    help='Set the amount of surrounding lines to include for context in diff output (default is ' + str(numberOfContextLinesForDiff) + ')')
    
    parser.add_argument('-d', '--discardOutputFiles', action='store_true',
    help='Set to automatically delete generated output files after test case is done, if this is not set all the generated output files are kept')
    
    parser.add_argument("-p", "--printoutMode", type=str, 
    choices=[mode.value for mode in PrintoutModes],
    help=('\n'.join([modeHelp.value for modeHelp in PrintoutModesHelp]))
    )
    
    parser.add_argument('-t', '--testcases', nargs='+', type=str,
    help='Set names (RxTy) of test cases to run, if this is not set all the test cases will be run')
    
    # Read in the arguments passed in from the command line
    args = parser.parse_args()

    # Process the arguments
    scriptToTestFileName = args.scriptToTestFileName
    numberOfContextLinesForDiff = args.contextDiffLines if args.contextDiffLines and args.contextDiffLines >= 0 else 0
    discardActualOutputFiles = args.discardOutputFiles
    printoutMode = PrintoutModes(args.printoutMode) if args.printoutMode else printoutMode
    namesOfTestcasesToRun = args.testcases

    # Start the main program
    main()