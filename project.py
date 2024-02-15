import pyfiglet, sys, os, csv, time
import pandas as pd
import numpy as np
from tabulate import tabulate

# MAIN

def main():

    # Settings
    global invalid

    # Creation of necessary directories
    if os.path.exists(r"C:\DotSplit\Database") == False:
        os.makedirs(r"C:\DotSplit\Database")

    if os.path.exists(r"C:\DotSplit\\Record") == False:
        os.makedirs(r"C:\DotSplit\\Record")

    # Settings - End


    # Logo
    print(figletText("DotSplit", "slant"))

    # Options
    print("          1 Create Database\n           2 Load Database\n          3 Remove Database\n               4 Help\n               5 Exit")
    
    # Invalid Check
    print(InvalidMsg(invalid))
    
    # Option Selection
    chooseOptionMain(input("           Select Option: "))

def chooseOptionMain(choice):
    r"For option selection of main()."

    global invalid

    if choice == '1':
        createDB()

    elif choice == '2':
        loadDB()

    elif choice == '3':
        remDB()
        
    elif choice == '4':
        help()
        # print __doc__ of main or access help() function

    elif choice == '5':
        sys.exit("\n   Thank You For Using DotSplit :)")

    else:
        invalid = 1
        main()

# 1 CREATE DATABASE

def createDB():
    
        global invalid

        print(displayDatabases())

        print("\n1 Create a Database\n2 Back")

        # Invalid Check
        print(InvalidMsg(invalid))
    
        chooseOptionCreateDB(input("Select Option: "))

def chooseOptionCreateDB(choice):

    global invalid

    if choice == '1':
        createDatabase(input("Enter Name of Database: "))

    elif choice == '2':
        main()

    else:
        invalid = 2
        createDB()

def createDatabase(DBName):

    global invalid

    if fileExist(DBName) == False:

        print("""\nEnter Names of Participants (Press X to Stop)
* A maximum of 10 participants can be added.\n""")
        
        participantList = participants()

        # FILE 1 - WORK FILE
        data = pd.DataFrame([['Due'] + participantList + ['Amount', 'Paid By', 'Transaction']], index = [''])
        data.to_csv(r"C:\DotSplit\Database\\" + DBName + ".csv", header = False, index = False)
        
        # FILE 2 - RECORD FILE
        data = pd.DataFrame([['Due'] + participantList + ['Amount', 'Paid By']], index = [''])
        data.to_csv(r"C:\DotSplit\\Record\\" + DBName + "_record.csv", header = False, index = False)
        
        invalid = 4
        main()
    
    else:
        invalid = 15
        remDB()
    
def participants():

    global invalid

    participants, i = [], 1
    while i <= 10:
        participant = input(f"Enter Name of Participant {i}: ")
        if participant not in participants:
            if participant == 'X':
                if i == 1:
                    invalid = 3
                    createDB()
                else:
                    return participants
            else:
                participants.append(participant)
                i += 1
        else:
            invalid = 13
            createDB()
    return participants

# 2 LOAD DATABASE

def loadDB():
        
        global invalid

        print(displayDatabases())

        print("\n1 Load a Database\n2 Back")

        # Invalid Check
        print(InvalidMsg(invalid))
    
        chooseOptionLoadDB(input("Select Option: "))

def chooseOptionLoadDB(choice):

    global invalid

    if choice == '1':
        select = input("Enter Database Name: ")
        if fileExist(select):
            selecDB(select)
        else:
            invalid = 7
            loadDB()

    elif choice == '2':
        main()

    else:
        invalid = 2
        loadDB()

# 2.1 SELECTED DATABASE
        
def selecDB(DBName):
    
    global invalid

    print(displayDatabase(DBName))

    print("\n1 Add Expense\n2 Delete Expense\n3 Settle Expense(s)\n4 Add Participant\n5 Delete Participant\n6 Back")

    # Invalid Check
    print(InvalidMsg(invalid))

    chooseOptionSelecDB(input("Select Option: "), DBName)

def chooseOptionSelecDB(choice, DBName):

    global invalid

    if choice == '1':
        addExpenseDetails(DBName)

    elif choice == '2':
        deleteExpenseDetails(DBName)

    elif choice == '3':
        settleExpenseDetails(DBName)

    elif choice == '4':
        addParticipantDetails(DBName)

    elif choice == '5':
        deleteParticipantDetails(DBName)

    elif choice == '6':
        loadDB()

    else:
        invalid = 2
        selecDB(DBName)

# 2.1.1 ADD EXPENSE
        
def addExpenseDetails(DBName):

    global invalid

    expense = input("Enter Expense: ")
    try:
        amount = int(input("Enter Amount Paid: "))
    except ValueError:
        invalid = 8
        selecDB(DBName)
    paidBy = input("Amount Paid By: ")

    if paidByExists(paidBy, DBName):
        addExpense(expense, amount, paidBy, DBName)
    else:
        invalid = 10
        selecDB(DBName)

def addExpense(expense, amount, paidBy, DBName):

    global invalid

    # File 1 - WORK

    with open(r"C:\DotSplit\Database\\" + DBName + ".csv", 'a', newline = '') as csvfile1:
        csvwriter = csv.writer(csvfile1)
        csvwriter.writerow([expense] + amountSplit(amount, paidBy, DBName) + [amount, paidBy] + [transaction(amount, paidBy, DBName)])

    # File 2 - RECORD

    with open(r"C:\DotSplit\\Record\\" + DBName + "_record.csv", 'a', newline = '') as csvfile2:
        csvwriter = csv.writer(csvfile2)
        csvwriter.writerow([expense] + amountSplit(amount, paidBy, DBName) + [amount, paidBy] + [transaction(amount, paidBy, DBName)])
    
    invalid = 9
    selecDB(DBName)

def amountSplit(amount, paidBy, DBName):
    members = list(readCSV(DBName, "Database"))[1:-3]
    split = []
    for member in members:
        if member != paidBy:
            split.append(amountDivider(amount, len(members)))
        else:
            split.append(0)
    return split

def transaction(amount, paidBy, DBName):
    members = list(readCSV(DBName, "Database"))[1:-3]
    transactions = ""
    for member in members:
        if member != paidBy:
            transactions += (member + "$" + paidBy + ":" + str(amountDivider(amount, len(members))) + '|')
    return transactions[:-1]

def paidByExists(participant, DBName):
    
    if participant in list(readCSV(DBName, "Database"))[1:-3]:
        return True
    else:
        return False
    
# 2.2.2 DELETE EXPENSE

def deleteExpenseDetails(DBName):
    
    global invalid

    expense = input("Enter Expense To Be Deleted: ")

    with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file1:
                data = list(csv.reader(file1))        
            
    if expenseExists(expense, data):
                    
        # FILE 1 - WORK FILE
        fileRewrite(deleteExpense(expense, data), DBName, "Database")

        # FILE 2 - RECORD FILE
        with open(r"C:\DotSplit\\Record\\" + DBName + "_record.csv") as file2:
            data2 = list(csv.reader(file2))        
        
        fileRewrite(deleteExpense(expense, data2), DBName, "Record")
        
        invalid = 12
        selecDB(DBName)
    else:
        invalid = 11
        selecDB(DBName)
    
def deleteExpense(expense, data):
    for i in range(0, len(data)):
        if data[i][0] == expense:
            del data [i]
            break
    return data

def expenseExists(expense, data):
    for entry in data:
        if entry[0] == expense:
            return True
    return False

# 2.2.3 SETTLE EXPENSE(S)

def settleExpenseDetails(DBName):

    global invalid
    
    displaySettlements(DBName)

    # Invalid Check
    print(InvalidMsg(invalid))

    selecSettleExpense(DBName, int(input("Which Expense to Settle? ")))

def selecSettleExpense(DBName, choice):

    global invalid

    dataUpdate = getSettlements(DBName)

    if 0 < choice and choice <= (len(dataUpdate) + 1):
        settleExpense(DBName, dataUpdate, choice)
        invalid = 17
        selecDB(DBName)

    else:
        invalid  = 2
        settleExpenseDetails(DBName)

def settleExpense(DBName, dataUpdate, choice):

    with open(r"C:\DotSplit\Database\\" + DBName + ".csv", 'r') as file1:
        csvreader = csv.reader(file1)
        data = list(csvreader)

    if choice == (len(dataUpdate) + 1):
        
        with open(r"C:\DotSplit\Database\\" + DBName + ".csv", 'w') as file2:
            csvwriter = csv.writer(file2)
            csvwriter.writerows([data[0]])
    
    else:
        with open(r"C:\DotSplit\Database\\" + DBName + ".csv", 'w') as file2:
            csvwriter = csv.writer(file2)
            print(dataUpdate)
        
def displaySettlements(DBName):

    print("\nExpenses to Settle\n")

    i = 1
    
    for entry in getSettlements(DBName):
        print(f"{i} {entry.split('$')[0]} to {entry.split('$')[1]} -> {getSettlements(DBName).get(entry)}")
        i += 1
    
    if i > 1:
        print(f"{i} Settle All Expenses")
    else:
        print("\n")

def getSettlements(DBName):
    
    with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file:
        
        data, dataDict, dataList = list(csv.reader(file)), dict(), list()
        
        for entry in data[1:]:
            for transaction in entry[-1].split('|'):
                if transaction.split(':')[0] in dataDict:
                    dataDict.update({transaction.split(':')[0]:dataDict.get(transaction.split(':')[0]) + int(transaction.split(':')[1])})
                else:
                    dataDict[transaction.split(':')[0]] = int(transaction.split(':')[1])

        for transaction in list(dataDict.keys()):
            From, To = transaction.split('$')
            if f"{From}${To}" in list(dataDict.keys()) and f"{To}${From}" in list(dataDict.keys()):
                if dataDict.get(f"{From}${To}") > dataDict.get(f"{To}${From}"):
                    dataDict.update({f"{From}${To}":dataDict.get(f"{From}${To}") - dataDict.get(f"{To}${From}")})
                    del dataDict[f"{To}${From}"]
                else:
                    dataDict.update({f"{To}${From}":dataDict.get(f"{To}${From}") - dataDict.get(f"{From}${To}")})
                    del dataDict[f"{From}${To}"]

        return dataDict

# 2.2.4 ADD PARTICIPANT
    
def addParticipantDetails(DBName):

    global invalid

    participant = input("Enter Name Of Participant: ")

    with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file:
        
        data = list(csv.reader(file))

        if participant in data[0]:
            invalid = 13
            selecDB(DBName)   
        else:

            # FILE 1 - WORK FILE
            fileRewrite(addParticipant(participant, data, -3), DBName, "Database")

            # FILE 2 - RECORD FILE
            with open(r"C:\DotSplit\\Record\\" + DBName + "_record.csv") as file2:
                data2 = list(csv.reader(file2))        
            
            fileRewrite(addParticipant(participant, data2, -2), DBName, "Record")
        
            invalid = 14
            selecDB(DBName)

def addParticipant(participant, data, index):
    data[0].insert(index, participant)
    for i in range(1, len(data)):
        data[i].insert(index, 0)
    return data

# 2.5.5 DELETE PARTICIPANT

def deleteParticipantDetails(DBName):

    global invalid

    participant = input("Enter Name Of Participant: ")

    with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file:
        data = list(csv.reader(file))

        if participant in data[0]:
            
            # FILE 1 - WORK FILE
            fileRewrite(deleteParticipant(participant, data), DBName, "Database")
            
            # FILE 2 - RECORD FILE
            with open(r"C:\DotSplit\\Record\\" + DBName + "_record.csv") as file1:
                data1 = list(csv.reader(file1))
            
            fileRewrite(deleteParticipant(participant, data1), DBName, "Record")
            
            invalid = 16
            selecDB(DBName)

        else:
            invalid = 10
            selecDB(DBName)

def deleteParticipant(participant, data):
    index = data[0].index(participant)
    del data[0][index]

    for entry in data:
        if participant in entry:
            data.remove(entry)

    for i in range(1, len(data)):

        del data[i][index]

        transactions = data[i][-1].split('|')
        for transaction in transactions:
            if participant in transaction:
                transactions.remove(transaction)
        data[i][-1] = "|".join(transactions)
    return data

# 3 REMOVE DATABASES

def remDB():
        
        global invalid

        print(displayDatabases())

        print("\n1 Remove a Database\n2 Back")

        # Invalid Check
        print(InvalidMsg(invalid))
    
        chooseOptionRemDB(input("Select Option: "))

def chooseOptionRemDB(choice):

    global invalid

    if choice == '1':
        removeDatabase(input("Enter Name of Database To Remove: "))
    elif choice == '2':
        main()
    else:
        invalid = 2
        remDB()

def removeDatabase(DBname):
    r"To remove a selected .csv file from C:\DotSplit\Database."
    
    global invalid

    try:

        # Remove WORK FILE
        os.remove(r"C:\DotSplit\Database\\" + DBname + r".csv")
        
        # Remove RECORD FILE
        os.remove(r"C:\DotSplit\\Record\\" + DBname + r"_record.csv")
        
        invalid = 5
        main()

    except FileNotFoundError:
        invalid = 6
        main()

# 4 HELP

def help():
    
    global invalid

    print(figletText("Help", "contessa"))

    print("1 Documentation\n2 Back")

    # Invalid Check
    print(InvalidMsg(invalid))

    chooseOptionHelp(input("Select Option: "))

def chooseOptionHelp(choice):

    global invalid

    if choice == '1':
        pass # Documentation

    elif choice == '2':
        main()
    else:
        invalid = 2
        help()

# FUNCTIONALITY

def figletText(prompt, style):
    r"Converts text in prompt to stylized text."
    
    return pyfiglet.figlet_format(prompt, font = style)

def forcedBack(prompt):
    print(prompt)
    condition = input("\nPress X To Go Back: ")
    if condition == 'X':
        main()
    else:
        forcedBack(prompt)

def fileExist(DBname):

    if os.path.exists(r"C:\DotSplit\Database\\" + DBname + ".csv"):
        return True
    else:
        return False

def amountDivider(amount, divideBy):
    return int(amount/divideBy)

def InvalidMsg(code = 0):
    r"""Returns to Main() with corresponding error message according to the code.
    It also resets global variable invalid back to 0."""

    global invalid

    if code == 0:
        return ""
    
    elif code == 1:
        msg = "\n   Invalid Input, Please Select Again!\n"

    elif code == 2:
        msg = "\nInvalid Input, Please Select Again!\n"

    elif code == 3:
        msg = "\nNot Enough Participants!\n"

    elif code == 4:
        msg = "\n          Database Created!\n"

    elif code == 5:
        msg = "\n          Database Removed!\n"

    elif code == 6:
        msg = "\n         Database Not Found!\n"

    elif code == 7:
        msg = "\nDatabase Doesn't Exist!\n"

    elif code == 8:
        msg = "\nAmount Should Be Integer!\n"
    
    elif code == 9:
        msg = "\nExpense Added!\n"

    elif code == 10:
        msg = "\nPerson Doesn't Exist In Database!\n"

    elif code == 11:
        msg = "\nExpense Doesn't Exist In Database!\n"

    elif code == 12:
        msg = "\nExpense Deleted!\n"

    elif code == 13:
        msg = "\nRepetition Of Participants Is Not Allowed!\n"

    elif code == 14:
        msg = "\nParticipant Added!\n"

    elif code == 15:
        msg = "\nDatabase By That Name Already Exists!\n"

    elif code == 16:
        msg = "\nParticipant Removed!\n"

    elif code == 17:
        msg = "\nAll Expenses Settled!\n"

    invalid = 0
    return msg

def readCSV(DBName, loc):
    return pd.read_csv(r"C:\DotSplit\\" + loc + "\\" + DBName + ".csv")

def csvToCsvObj(DBName): # TO TEST
    with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file:
        return csv.reader(file)
    
def displayDatabase(DBName):
    with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file:
        data = np.array(list(csv.reader(file)), dtype = object)
    
    try:
        return tabulate(data[1:, :-3], headers = data[0][:-3])
    except IndexError:
        data = np.array([list(data)[0]])
        # print('\n', data, '\n') # Test
        return tabulate(data[1:, :-3], headers = data[0][:-3])
    
def displayDatabases():
    r"To display list of .csv files in C:\DotSplit\Database."

    print()
    names = []
    for path in os.listdir(r"C:\DotSplit\Database"):
        path_time = r"C:\DotSplit\Database\\" + path
        names.append([path[:-4], time.ctime(os.path.getctime(path_time)).split()[2] + " " + time.ctime(os.path.getctime(path_time)).split()[1] + " " + time.ctime(os.path.getctime(path_time)).split()[4]])
    return tabulate(names, headers = ["Database Name", "Date of Creation"], stralign = "center")

def fileRewrite(newData, DBName, loc):
    with open(r"C:\DotSplit\\" + loc + "\\" + DBName + ".csv", 'w', newline = '') as csvfile1:
        csvwriter = csv.writer(csvfile1)
        csvwriter.writerows(newData)

# START

if __name__ == "__main__":

    global invalid

    invalid = 0 # Variable for checking invalid input in main
    
    main()
