# DotSplit: Expense Tracker & Manager

#### Video Demo: https://www.youtube.com/watch?v=8TT0tE-Jb0U&t=34s

#### Description:
DotSplit is an application that allows you to track and manage expenses of people living together. It allows you to create databases where a track of the expenses can be kept. It allows you to export a PDF report of your spendings as well.

#### Project Structure:
- `project.py`: The main Python script that runs the application.
- `test_project.py`: Unit tests for the application.
- `requirements.txt`: Lists all necessary Python libraries for easy installation.
- `README.md`: Documentation for the project.

#### Libraries Used:
- **Pyfiglet:** Used for generating stylish text banners and ASCII art.
- **Pandas:** Used for efficient management of CSV files.
- **NumPy:** Used for array creation.
- **Tabulate:** Used for formatting tables in the application.
- **Fpdf:** Used for generating the PDF report.

Run the following pip command on your terminal to install the above libraries:

```bash
pip install -r requirements.txt
```

#### Functionality:
- **Database Creation:** Various databases can be created to keep track of multiple expense records.
- **Expense Management:** Multiple options are provided to manage the expenses. These include addition and deletion of expenses & addition and deletion of participants. It automatically calculates and displays the amount due by one participant to another.
- **Settling Expenses:** Calculates the overall amount due by one participant to another which is helpful in clearing the dues in one go. Updates the database once the amount is settled.
- **Expense Report Generation:** Generates a monthly report of the all the expenses.
- **Error Handling:** Proper and user-friendly error handling.

#### Usage:
1. On starting it can be seen that multiple options have been provided to start interacting with the application. These include:
   - Create Database
   - Load Database
   - Remove Database
   - Help
   - Exit

2. First of all, go to create your very own database by giving it a name and adding all the participants involved.

3. Then load the database that you have created and start adding the expenses as they keep on coming. The application provides you with multiple options to deal with your expenses and the database as a whole. These include:
   - Add Expense
   - Delete Expense
   - Settle Expense(s)
   - Add Participant
   - Delete Participant

4. The functionality of these options is pretty self-explanatory. The two most important to fun to use ones are 'Settle Expense(s)' and 'Generate Monthly Report'.
The former displays a list of all the dues from one participant to another which helps in clearing them easily, the database is updated automatically once a due is cleared. The latter generates a PDF report of all the expenses pertaining this particular database and stores it in the 'Export' folder.

This application is extremely useful for people living together in shared spaces as keeping track of expenses can be a tough ask in such situations. DotSplit simplifies the entire process, making the entire thing a whole lot easier to keep track of.
