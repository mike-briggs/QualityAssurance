import subprocess
import os

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