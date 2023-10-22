import mysql.connector 

#database credentials here
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "", #insert MySQL password
    database = "" #insert database name
)

cursor = mydb.cursor()

#following functions are used in database interaction

def get_info(table, attribute, name):
    #code to make sure input is valid and in table, additional parameter name is just for formatting
    query = "SELECT {} FROM {};".format(attribute, table)
    cursor.execute(query)
    all_info = [str(x[0]) for x in cursor]

    cond = True
    while cond:
        #if ssn or department number is not in respective table ask user to input new entry
        info = input("Please enter {}: ".format(name)).strip()

        if info not in all_info:
            print("Invalid {} please try again".format(name))
            print()
        else:
            cond = False

    print()
    return info

def try_query(query, Success_message):
    #code to execute a query, if problem is encountered then print the error for the user to know    
    try:
        cursor.execute(query)
        print(Success_message)
        mydb.commit()
    except (mysql.connector.Error) as error:
        print(error)
    mydb.commit()
    print()

def insert_info(table, input_message, additional_param = None):
    #code to insert new tuple into table
    info = input(input_message)
    info = info.replace(" ", "")
    info = info.split(',')
    info = list(info)

    #additional_param used to add info to beginning of tuple that we already had and don't need to get in the input
    if additional_param != None:
        temp = []
        temp.append(additional_param)
        for i in info:
            temp.append(i)
        info = temp

    info = tuple(info)
    query = "INSERT INTO {} VALUES {};".format(table, info)
        
    try_query(query, "Query Executed Successfully!")

def print_info(query):
    #code to print a tuple in a table
    cursor.execute(query)
    for x in cursor:
        print(x)
    print()

def modify_employee_info(updated_field, input_message, ssn):
    #code to modify one field of a tuple where ssn is the primary key
    new_info = input(input_message).strip()
    query = "UPDATE EMPLOYEE SET {} = '{}' WHERE Ssn = {};".format(updated_field, new_info, ssn)
    
    try_query(query, "Query Executed Successfully!")

while True:
    print("MENU")
    print("(1) Add new employee")
    print("(2) View employee")
    print("(3) Modify employee")
    print("(4) Remove employee")
    print("(5) Add new dependent")
    print("(6) Remove dependent")
    print("(7) Add new department")
    print("(8) View department")
    print("(9) Remove department")
    print("(10) Add department location")
    print("(11) Remove department location")
    print("(0) Exit")
    choice = input("Select the number of desired option: ")

    choice = choice.strip()

    if choice == "1":
        #code for add new employee
        insert_info("EMPLOYEE", "Please enter employee information in the form of Fname, Minit, Lname, Ssn, Bdate (YYYY-MM-DD), Address, Sex, Salary, Super_ssn, Dno (To leave a field blank type nothing): \n")

    elif choice == "2":
        #code for view employee
        ssn = get_info("EMPLOYEE", "Ssn", "employee's ssn")
        query = """SELECT E.Fname, E.Minit, E.Lname, E.Ssn, E.Bdate, E.Address, E.Sex, E.Salary, E.Super_ssn, E.Dno, E2.Fname, E2.Minit, E2.Lname, D.Dname, D2.Dependent_name FROM EMPLOYEE E JOIN EMPLOYEE E2 ON E.Super_ssn = E2.Ssn JOIN DEPARTMENT D ON E.Super_Ssn = D.Mgr_ssn LEFT JOIN DEPENDENT D2 ON E.Ssn = D2.Essn WHERE E.Ssn = '{}';""".format(ssn)
        print("Employee Information in the form of (Employee Fname, Employee Minit, Employee Lname, Employee Ssn, Employee DOB, Employee Address, Employee Sex, Employee Salary, Employee's Manager Ssn, Employee Department #, Manager Fname, Manager Minit, Manager Lname, Employee Department Name, Employee Dependent Name):")
        print_info(query)

    elif choice == "3":
        #code for modify employee
        ssn = get_info("EMPLOYEE", "Ssn", "employee's ssn")
        
        while True:
            print("Current Employee Information in the form of (Employee Fname, Employee Minit, Employee Lname, Employee Ssn, Employee DOB, Employee Address, Employee Sex, Employee Salary, Employee's Manager Ssn, Employee Department #):")
            query = "SELECT * FROM EMPLOYEE WHERE Ssn = '{}' FOR UPDATE;".format(ssn)
            #lock is built in for update command, will unlock when mydb.commit() is done
            print_info(query)
            #can put this into print_info function

            #employee modification menu, similar structure to general menu
            print("Employee Modification Menu")
            print("(1) Modify address")
            print("(2) Modify sex")
            print("(3) Modify salary")
            print("(4) Modify super_ssn")
            print("(5) Modify Dno")
            print("(0) Exit")

            choice = input("Select the number of desired option: ").strip()

            if choice == "1":
                #modify_employee function built to reduce repreating lines of cod for this menu
                modify_employee_info("Address", "Please input new employee address: ", ssn)

            elif choice == "2":
                modify_employee_info("Sex", "Please input new employee sex (1 character): ", ssn)

            elif choice == "3":
                modify_employee_info("Salary", "Please input new employee salary (no commas): ", ssn)

            elif choice == "4":
                modify_employee_info("Super_ssn", "Please input new supervisor ssn (no dashes): ", ssn)

            elif choice == "5":
                modify_employee_info("Dno", "Please input new department number: ", ssn)

            elif choice == "0":
                mydb.commit()
                print("Exiting Employee Modification Menu")
                print()
                break

            else:
                mydb.commit()
                print("Invalid input, please try again")
                print()


    elif choice == "4":
        #code for remove employee
        #get_info function in this case will only work when given an ssn in the database, not entering a valid ssn return a message to input a valid ssn
        ssn = get_info("EMPLOYEE", "Ssn", "employee's ssn")

        print("Current Employee Information in the form of (Employee Fname, Employee Minit, Employee Lname, Employee Ssn, Employee DOB, Employee Address, Employee Sex, Employee Salary, Employee's Manager Ssn, Employee Department #):")
        query = "SELECT * FROM EMPLOYEE WHERE Ssn = '{}' FOR UPDATE;".format(ssn)
        print_info(query)

        while True:

            choice = input("Are you sure you wish to delete this employee? [Y/N]: ")

            if choice == "Y":
                query = "DELETE FROM EMPLOYEE WHERE Ssn = '{}'".format(ssn)
                try:
                    #successful case
                    cursor.execute(query)
                    mydb.commit()
                    print("Employee removed")
                    print()
                    break
                except (mysql.connector.Error) as error:
                    #failed case
                    #double check about warnings message
                    print(error)
                    print("Please fix the above error and try again")
                    print()
                    break

            elif choice == "N":
                mydb.commit()
                print("Employee Information not deleted")
                print()
                break

            else:
                print("Invalid input, please try again")
                print()

    elif choice == "5":
        #code for add new dependent
        ssn = get_info("EMPLOYEE", "Ssn", "employee's ssn")

        print("Current Dependent Information in the form of (Employee Ssn, Dependent Name, Dependent DOB, Dependent Relationship):")
        query = "SELECT * FROM DEPENDENT WHERE Essn = '{}' FOR UPDATE;".format(ssn)
        print_info(query)

        insert_info("DEPENDENT", "Please enter dependent information in the form of Dependent_name, Sex, Bdate (YYYY-MM-DD), Relationship to Employee: \n", additional_param = ssn)
    
    elif choice == "6":
        #code for remove dependent
        ssn = get_info("EMPLOYEE", "Ssn", "employee's ssn")

        print("Current Dependent Information")
        query = "SELECT * FROM DEPENDENT WHERE Essn = '{}' FOR UPDATE;".format(ssn)
        print_info(query)

        name = input("Please input name of dependent to be removed: ")
        query = "DELETE FROM DEPENDENT WHERE Dependent_name = '{}'".format(name)

        try_query(query, "Dependent Removed!")

    elif choice == "7":
        #code for add new department
        insert_info("DEPARTMENT", "Please enter department information in the form of Dname, Dnumber, Mgr_ssn, Mgr_start_date (YYYY-MM-DD): \n")

    elif choice == "8":
        #code for view department
        dnumber = get_info("DEPARTMENT", "Dnumber", "department number")
        query = """SELECT DEPARTMENT.Dnumber, EMPLOYEE.Fname, EMPLOYEE.Minit, EMPLOYEE.Lname, DEPT_LOCATIONS.Dlocation FROM DEPARTMENT JOIN EMPLOYEE ON DEPARTMENT.Mgr_ssn = EMPLOYEE.Ssn JOIN DEPT_LOCATIONS ON
DEPARTMENT.Dnumber = DEPT_LOCATIONS.Dnumber WHERE DEPARTMENT.Dnumber = {};""".format(dnumber)

        print("Departments in the form of (Department #, Manager Fname, Manager Minit, Manager Lname, Department Location):")
        print_info(query)

    elif choice == "9":
        #code for remove department
        dnumber = get_info("DEPARTMENT", "Dnumber", "department number")
        query = "SELECT * FROM DEPARTMENT WHERE Dnumber = {} FOR UPDATE;".format(dnumber)
        
        print("Departments in the form of (Department Name, Department #, Manager Ssn, Manager Start Date): ")
        print_info(query)

        while True:
            #similar in structure to option 4 remove employee

            choice = input("Are you sure you wish to delete this department? [Y/N]: ")

            if choice == "Y":
                query = "DELETE FROM DEPARTMENT WHERE Dnumber = '{}';".format(dnumber)
                try:
                    cursor.execute(query)
                    mydb.commit()
                    print("Department removed")
                    print()
                    break
                except (mysql.connector.Error) as error:
                    #double check about warnings message
                    mydb.commit()
                    print(error)
                    print("Please fix the above error and try again")
                    print()
                    break

            elif choice == "N":
                mydb.commit()
                print("Department Information not deleted")
                print()
                break

            else:
                print("Invalid input, please try again")
                print()

    elif choice == "10":
        #code for add department location
        dnumber = get_info("DEPARTMENT", "Dnumber", "department number")
        query = "SELECT Dlocation FROM DEPT_LOCATIONS WHERE Dnumber = '{}' FOR UPDATE;".format(dnumber)
        
        print_info(query)
        insert_info("DEPT_LOCATIONS", "Please enter new department location: ", additional_param = dnumber)

    elif choice == "11":
        #code for remove department location
        dnumber = get_info("DEPARTMENT", "Dnumber", "department number")
        query = "SELECT Dlocation FROM DEPT_LOCATIONS WHERE Dnumber = '{}' FOR UPDATE;".format(dnumber)

        print_info(query)
        location = get_info("DEPT_LOCATIONS", "Dlocation", "department location")

        query = "DELETE FROM DEPT_LOCATIONS WHERE Dlocation = '{}' and Dnumber = '{}';".format(location, dnumber)
        try_query(query, "Department Successfully Deleted!")

    elif choice == "0":
        print("Bye")
        print()
        break

    else:
        print("Invalid input, please try again")

cursor.close()
mydb.close()

#test tuples
#add employee test
#Fname, M, Lname, 000000000, 1999-11-11, Address, S, 00000, 123456789, 1

#add dependent test
#Test, M, 1999-10-11, Test

#add department test
#Test, '100', '123456789', '2002-11-11' 
