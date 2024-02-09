import pyfiglet, sys, os, csv, time
import pandas as pd
import numpy as np
from tabulate import tabulate

# MAIN

def main():

    global invalid

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
        forcedBack("\nDatabase By That Name Already Exists!")
    
def participants():

    global invalid

    participants, i = [], 1
    while i <= 10:
        participant = input(f"Enter Name of Participant {i}: ")
        if participant == 'X':
            if i == 1:
                invalid = 3
                createDB()
            else:
                return participants
        else:
            participants.append(participant)
            i += 1
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
        csvwriter.writerow([expense] + amountSplit(amount, paidBy, DBName) + [amount, paidBy] + transaction(amount, paidBy, DBName))

    # File 2 - RECORD

    with open(r"C:\DotSplit\\Record\\" + DBName + "_record.csv", 'a', newline = '') as csvfile2:
        csvwriter = csv.writer(csvfile2)
        csvwriter.writerow([expense] + amountSplit(amount, paidBy, DBName) + [amount, paidBy] + (transaction(amount, paidBy, DBName)))
    
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
    transactions = []
    for member in members:
        if member != paidBy:
            transactions.append(member + "$" + paidBy + ":" + str(amountDivider(amount, len(members))))
    return [transactions]

def paidByExists(participant, DBName):
    
    if participant in list(readCSV(DBName, "Database"))[1:-3]:
        return True
    else:
        return False
    
# 2.2.2 DELETE EXPENSE

def deleteExpenseDetails(DBName):
    
    global invalid

    expense = input("Enter Expense To Be Deleted: ")

    if expenseExists(expense, data):
                    
            # FILE 1 - WORK FILE
            with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file1:
                data1 = list(csv.reader(file1))        
            
            fileRewrite(deleteExpense(expense, data1), DBName)

            # FILE 2 - RECORD FILE
            with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file2:
                data2 = list(csv.reader(file2))        
            
            fileRewrite(deleteExpense(expense, data2), DBName)
            
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

def fileRewrite(newData, DBName):
    with open(r"C:\DotSplit\Database\\" + DBName + ".csv", 'w', newline = '') as csvfile1:
        csvwriter = csv.writer(csvfile1)
        csvwriter.writerows(newData)

def expenseExists(expense, data):
    for entry in data:
        if entry[0] == expense:
            return True
    return False

# 2.2.3 SETTLE EXPENSE(S)

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

def back():
    pass

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
        
    invalid = 0
    return msg

def readCSV(DBName, loc):
    return pd.read_csv(r"C:\DotSplit\\" + loc + "\\" + DBName + ".csv")

def csvToCsvObj(DBName): # TO TEST
    with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file:
        return csv.reader(file)
    
def displayDatabase(DBName):
    with open(r"C:\DotSplit\Database\\" + DBName + ".csv") as file:
        data = np.array(list(csv.reader(file)))
    return tabulate(data[1:, :-3], headers = data[0][:-3])

def displayDatabases():
    r"To display list of .csv files in C:\DotSplit\Database."

    print()
    names = []
    for path in os.listdir(r"C:\DotSplit\Database"):
        path_time = r"C:\DotSplit\Database\\" + path
        names.append([path[:-4], time.ctime(os.path.getctime(path_time)).split()[2] + " " + time.ctime(os.path.getctime(path_time)).split()[1] + " " + time.ctime(os.path.getctime(path_time)).split()[4]])
    return tabulate(names, headers = ["Database Name", "Date of Creation"], stralign = "center")

# START

if __name__ == "__main__":

    global invalid

    invalid = 0 # Variable for checking invalid input in main
    
    # Creation of necessary directories
    if os.path.exists(r"C:\DotSplit\Database") == False:
        os.makedirs(r"C:\DotSplit\Database")

    if os.path.exists(r"C:\DotSplit\\Record") == False:
        os.makedirs(r"C:\DotSplit\\Record")

    main()
