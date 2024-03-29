import os
import subprocess
import glob


# if this string has length of 2 (and starts with D)
# return true, else false


def filterFolderStructure(arr):
    if(len(arr) == 2):
        return True
    else:
        return False


# get all files/folders starting with D
files = glob.glob("D*")
# get array of folders with our filter applied
folders = filter(filterFolderStructure, files)

# run the daily script with all the "days" we found
for i in folders:
    print(i)
    print(i.replace('D',''))
    
    i = i.replace('D','')

    # run daily with what day of the week we want
    runCommand = ["python"]+["daily.py"]+[i]
    try:
        runDaily = subprocess.run(runCommand)

        # TODO: Execute backend at the end of each daily
        #p = subprocess.Popen(...
        
        #poll = p.poll()
        #if poll == None:
        # p.subprocess is alive

        #if(poll != None):
        
        
    except subprocess.TimeoutExpired:
        pass
