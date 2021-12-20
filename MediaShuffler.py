# LOGGING & EXCEPTIONS SETUP
import logging
from datetime import datetime, timedelta, time, date
import traceback
now = datetime.now()
current_time = now.strftime("%y-%m-%d-%H-%M-%S")
logging.basicConfig(filename="logs/MediaShullfer-" + current_time + ".log",level=logging.INFO, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# MAIN IMPORTS
logging.info("MediaShuffle is starting...")
try:
    import configparser
    from pathlib import Path
    import os
    import random
    import regex as re
    import inquirer # For menu
    from sys import exit

except Exception as e:
    logging.error('Exception in importing modules.\nException: '  + str(e))
    print('Exception in importing modules.\nException: '  + str(e))
    traceback.print_exc()
    input('Press ENTER to exit.')
    exit()

# CHOICE MENU
def actionType():
    try:
        questions = [
          inquirer.List('actionType',
                        message="Please select: ",
                        choices=['Replacing existing tags (remove and generate new)', 'Removing tags only', 'Generating tags only'],
                    ),
        ]
        answers = inquirer.prompt(questions)

        if str(answers["actionType"]) == "Replacing existing tags (remove and generate new)":
            choice = 1
            return choice
        elif str(answers["actionType"]) == "Removing tags only":
            choice = 2
            return choice
        else:
            choice = 3
            return choice

    except Exception as e:
        logging.error('Exception in function "actionType".\nException: '  + str(e))
        print('Exception in function "actionType".\nException: '  + str(e))
        traceback.print_exc()
        input('Press ENTER to exit.')
        exit()

# GET FILES EXTENSIONS
def fileTypes():
    parser = configparser.ConfigParser()
    parserpath = Path("configs/configurations.txt")
    parser.read(parserpath)
    mediaTypes = parser.get("config", "mediaTypes").replace(' ','')

    filetypes = str(mediaTypes).split(',')

    return filetypes

# CHECKING FOR TAGS & REMOVING THEM IF THEY EXIST
def removefiletags(FilePath, filetypes):
    logging.info("Checking for tags...")
    try:
        # PROGRESS BAR
        CountBAR = 0
        iteration = 0

        for item in os.listdir(FilePath):
            CountBAR +=1

        printProgressBar(iteration, CountBAR, prefix = f'Progress:', suffix = 'Complete', length = 50)

        # FILE RENAMING
        #filetype = ['wav','mp3','m3u','wma', 'txt']
        for file in os.listdir(FilePath):
            if any(extension in str(file) for extension in filetypes):
                pat = r'([0-9]{4}_)'
                new1 = re.sub(pat,'',file,re.MULTILINE)

                old_file_name = f'{FilePath}/{file}'
                new_file_name = f'{FilePath}/{new1}'

                os.rename(old_file_name, new_file_name)

            iteration = iteration + 1
            printProgressBar(iteration, CountBAR, prefix = f'Progress:', suffix = 'Complete', length = 50)

    except Exception as e:
        logging.error('Exception in function "removefiletags".\nException: '  + str(e))
        print('Exception in function "removefiletags".\nException: '  + str(e))
        traceback.print_exc()
        exit()

# RENAMING EACH FILES WITH A RANDOM NUMBER TO SHUFFLE THE ORDER
def renamefiles(FilePath, filetypes):
    logging.info("Renaming files...")
    try: 
        # PROGRESS BAR
        CountBAR = 0
        iteration = 0

        for item in os.listdir(FilePath):
            CountBAR +=1

        printProgressBar(iteration, CountBAR, prefix = f'Progress:', suffix = 'Complete', length = 50)

        # FILE RENAMING
        NumList = random.sample(range(1000,5000), CountBAR) # create a list of X random numbers between a range without diplicates. (In this case, X = CountBAR, would be the numbers of files in te folder)
        NumCount = 0

        #filetype = ['wav','mp3','m3u','wma', 'txt']
        for file in os.listdir(FilePath):
            if any(extension in str(file) for extension in filetypes):
                #randomNumb = random.randint(1000,5000) # will have duplicates
                randomNumb = NumList[NumCount]
                tag = f'{randomNumb}_'

                old_file_name = f'{FilePath}/{file}'
                new_file_name = f'{FilePath}/{tag}{file}'

                os.rename(old_file_name, new_file_name)

            NumCount += 1
            iteration = iteration + 1
            printProgressBar(iteration, CountBAR, prefix = f'Progress:', suffix = 'Complete', length = 50)

        print("Files renamed!")

    except Exception as e:
        logging.error('Exception in function "renamefiles".\nException: '  + str(e))
        print('Exception in function "renamefiles".\nException: '  + str(e))
        traceback.print_exc()
        exit()

# OFFERS THE USER TO START AGAIN
def playAgain():
    logging.info("User prompted to 'play' again...")
    try:
        yesChoice = ['yes', 'y']
        noChoice = ['no', 'n']
        print()
        input1 = input('Do you want to return to the main menu? ').lower()

        if input1 in yesChoice:
            main()           

        elif input1 in noChoice:
            input("Press ENTER to exit.")
            exit()
        else: 
            print('Invalid input, please try again.')
            playAgain()

    except Exception as e:
        logging.error('Exception in function "playAgain".\nException: '  + str(e))
        print('Exception in function "playAgain".\nException: '  + str(e))
        traceback.print_exc()
        input('Press ENTER to exit.')
        exit()

# PROGRESS BAR SETUP
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    try:
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()
            
    except Exception as e:
        logging.error('Exception in function "printProgressBar".\nException: '  + str(e))
        print('Exception in function "printProgressBar".\nException: '  + str(e))
        traceback.print_exc()
        exit()

def main():
    FilePath = input('Please enter the path of you files: ')
    Choice = actionType()
    filetypes = fileTypes()

    if Choice == 1:
        removefiletags(FilePath, filetypes)
        renamefiles(FilePath, filetypes)
        playAgain()
    elif Choice == 2:
        removefiletags(FilePath, filetypes)
        playAgain()
    else:
        renamefiles(FilePath, filetypes)
        playAgain()

# RUNS THE SCRIPT
if __name__ == "__main__":
    main()
