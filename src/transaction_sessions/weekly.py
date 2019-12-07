import os
import subprocess
import glob

# if this string has length of 2 (and starts with D)
# return true, else false


class FileNames():
    DAILY_FOLDER_PREFIX = 'D'


def filterFolderStructure(arr):
    if(len(arr) == 2):
        return True
    else:
        return False


# get all files/folders starting with D
files = glob.glob(FileNames.DAILY_FOLDER_PREFIX+"*")
# get array of folders with our filter applied
folders = filter(filterFolderStructure, files)

# run the daily script with all the "days" we found
for i in folders:
    dayNumber = i[1:]
    print(dayNumber)
    # run daily with what day of the week we want
    dailyCommand = ["python"]+["daily.py"]+[dayNumber]
    try:
        runDaily = subprocess.run(dailyCommand)

        # TODO:     if(command ran successfully):
        backendCommand = ["python"]+["backend.py"]+[dayNumber]
        try:
            runBackend = subprocess.run(backendCommand)
        except subprocess.TimeoutExpired:
            pass
    except subprocess.TimeoutExpired:
        pass
