import psycopg2
import datetime

class Customer:
    def __init__(self, Cust_id, Name, Phone, Email, M_pin, Balance, Bank_id, Branch_id, Account_num):
        self.Cust_id   =  Cust_id
        self.Name      =  Name
        self.Phone     =  Phone
        self.Email     =  Email
        self.M_pin     =  M_pin
        self.Balance   =  Balance
        self.Bank_id   =  Bank_id
        self.Branch_id =  Branch_id
        self.Account_num = Account_num

class Transactions:
    def __init__(self, Transaction_id, Receive_id, Send_id, amount):
        self.Transaction_id =   Transaction_id
        self.Receive_id     =   Receive_id
        self.Send_id        =   Send_id
        self.amount         =   amount

class Loan:
    def __init__(self, Loan_id, Amount, Deadline, EMI):
        self.Loan_id  =     Loan_id
        self.Amount   =     Amount
        self.Deadline =     Deadline
        self.EMI      =     EMI

class Defaulters:
    def __intit__(self, Penality, Due):
        self.Penality   =     Penality
        self.Due        =     Due

###########################################################################################################

def account_number(bank_id, branch_id, cust_id):
    return bank_id+branch_id+cust_id

def phone_num_validate(num):
    if( num.isnumeric() == False ):
        return False

    if(len(num)==10):
        return True
    
    return False

def mpin_validate(num):
    if(len(num)==6):
        return True
    
    return False

def email_validate(email):
    if(len(email)<10):
        return False
    
    email_val = email[-10:]
    if(email_val=="@gmail.com"):
        return True
    
    return False

def cust_id_generator(cust_id):
    if cust_id is None:
        cust_id = "00000"

    int_id = int(cust_id)+1
    formatted_string = f'{int_id:05}'

    return formatted_string

def transaction_id_generator(sender,reciever):
    current_datetime = datetime.datetime.now()
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute
    current_second = current_datetime.second
    return sender+str(current_hour)+str(current_minute)+str(current_second)+str(current_day)+str(current_month)+str(current_year)+reciever

def generate_loan_id(bank_id, cust_id):
    return bank_id+cust_id


def search():
    satisfied = False
    
    while not satisfied:
        search_string = input("Enter the string to search : ")

        sql = "SELECT DISTINCT name FROM customer WHERE name LIKE %s"
        mycursor.execute(sql, (search_string + "%", ))
        l = []
        rows = mycursor.fetchall()
        for row in rows:
            l.append(row[0])

        sql = "SELECT DISTINCT name FROM customer WHERE name LIKE %s"
        mycursor.execute(sql, ("%" + search_string + "%", ))
        rows = mycursor.fetchall()
        for row in rows:
            l.append(row[0])

        sql = "SELECT DISTINCT name FROM customer WHERE name LIKE %s"
        mycursor.execute(sql, ("%" + search_string, ))
        rows = mycursor.fetchall()
        for row in rows:
            l.append(row[0])

        s = set(l)

        for ss in s:
            print(s)

        found = input("Enter the full name if you found. Type \'RETRY\' to try again or to exit type EXIT : ")

        if found == "RETRY":
            satisfied = False
        elif found == "EXIT":
            satisfied = True
            return "EXIT"
        else:
            satisfied = True
            sql = "SELECT cust_id FROM customer WHERE name = %s"
            mycursor.execute(sql, (found, ))
            name = mycursor.fetchone()

            if name is None:
                print("No customer with that name. Please enter as shown.")
                return "EXIT"
    
            return name[0]

#########################################################################################################

conn= psycopg2.connect(
   host="localhost",
   port=5432,
   database="phonepe",
   user="ayushmaan",
   password="1234"
   )

mycursor = conn.cursor()

###########################################################################################################

text = "Phonepe"
styled_text = "\033[1;95m" + text + "\033[0m"

print ("|--------------------------------------------------------------------------------------|")
print ("|                                                                                      |")
print ("|                                "+styled_text+"                                               |")
print ("|                A trustworthy app for your transactions, loans, bills and many more   |")
print ("|                                                                                      |")
print ("|--------------------------------------------------------------------------------------|")

print("\n\n")
namaste_emoji = "\U0001F64F"
print ("                            Welcome to PhonePe "+namaste_emoji)
print("\n\n")

###########################################################################################################

print("     1. New Customer: Sign Up                  2. Existing Customer: Login\n")
print("     3. New Merchant: Sign Up                  4. Existing Merchant: Login\n")

while True:
    choice =input("Please Enter your choice: ")
    if choice == "1" or choice == "2" or choice == "3" or choice == "4":
        break
    else:
        print("Enter valid choice")

if choice == "1":
    print("\n\n             Please Fill the following Details:\n")
    Name=input("Enter Your Name: ")

    Phone = input("Enter Your Phone Number: ")
    while(phone_num_validate(Phone)==False):
        Phone = input("Invalid phone number. Please Enter Again: ")

    Email = input("Enter Your Email id [If you don't have one, enter NA]: ")
    if( Email != "NA" ):
        while(email_validate(Email)==False):
            Email = input("Invalid Email entered. Email should end with '@gmail.com'.\nPlease Enter Again: ")

    M_pin = input("Enter a 6-digit UPI pin: ")
    while(mpin_validate(M_pin)==False):
        M_pin = input("UPI Pin should be 6 digits. Please Enter Again: ")

    print("\n           BANKS LIST:")
    sql = "SELECT DISTINCT bank_name FROM bank ORDER BY bank_name"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count = 1

    l = []

    for row in rows:
        print(count, ". ", row[0])
        count += 1

    ch = int(input("Enter in which bank is your account in: "))

    sql = "SELECT DISTINCT bank_id FROM bank ORDER BY bank_id"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count = 1

    for row in rows:
        if count == ch:
            Bank_id = row[0]
            break
        count = count + 1

    print(Bank_id)
    print("             BRANCHES LIST \n")
    sql = "SELECT branch FROM bank where bank_id = %s;"
    mycursor.execute(sql,(Bank_id,))
    rows = mycursor.fetchall()
    count = 1

    for row in rows:
        row_str = '\t'.join(map(str, row))
        print(count,". ",row_str)
        count = count + 1

    ch=int(input("Enter the branch of the bank in which your account is present: "))

    sql = "SELECT branch_id FROM bank where bank_id = %s;"
    mycursor.execute(sql,(Bank_id,))
    rows = mycursor.fetchall()
    count  = 1

    for row in rows:
        row_str = '\t'.join(map(str, row))
        if count == ch:
            Branch_id = row_str
            break
        count = count + 1

    sql = "SELECT max(cust_id) FROM customer;"
    mycursor.execute(sql)
    max_id = mycursor.fetchone()[0]
    Cust_id=cust_id_generator(max_id)
    Account_num=account_number(Bank_id, Branch_id, Cust_id)
    Customer_1 = Customer(Cust_id, Name, Phone, Email, M_pin, 0, Bank_id, Branch_id, Account_num)

    l = []
    l.append(Customer_1.Cust_id)
    l.append(Customer_1.Name)
    l.append(Customer_1.Phone)
    l.append(Customer_1.Email)
    l.append(Customer_1.M_pin)
    l.append(Customer_1.Account_num)
    l.append(0)
    l.append(Customer_1.Bank_id)
    l.append(Customer_1.Branch_id)

    # cust_id | name | phone | email | mpin | acc_no | balance | bank_id | branch_id

    sql = "INSERT INTO customer (cust_id, name, phone, email, mpin, acc_no, balance, bank_id, branch_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, tuple(l))

    print("\n\nSign in Successful. Here are your details.\n")

    print("Cust_ID : " , Customer_1.Cust_id)
    print("Name : ", Customer_1.Name)
    print("Phone :", Customer_1.Phone)
    print("Email : ", Customer_1.Email)
    print("MPIN : ",Customer_1.M_pin)
    print("Account Number : ", Customer_1.Account_num)
    print("Balance : ", Customer_1.Balance)

    mycursor.execute("SELECT DISTINCT branch FROM bank WHERE branch_id = %s", (Customer_1.Branch_id,))
    branch = mycursor.fetchall()[0]

    mycursor.execute("SELECT bank_name FROM bank WHERE bank_id = %s", (Customer_1.Bank_id,))
    bank = mycursor.fetchall()[0]

    print("Bank : ", bank[0])
    print("Branch : ", branch[0])

    print("\n\nThank you for choosing phonepe.")

    conn.commit()


###########################################################################################################
    
elif choice == "2":

    conn= psycopg2.connect(
    host="localhost",
    port=5432,
    database="phonepe",
    user="ayushmaan",
    password="1234"
    )

    mycursor = conn.cursor()

    print("\n\nPlease Enter your details as follows:\n")
    Cust_id = input("Enter your customer id: ")
    UPI_Pin = input("Enter your UPI pin: ")

    # Check if the customer with the given Cust_id and UPI_Pin exists in the database
    sql = "SELECT * FROM customer WHERE cust_id = %s AND mpin = %s;"
    mycursor.execute(sql, (Cust_id, UPI_Pin))
    data_out = mycursor.fetchone()
    
    count = 1

    if data_out is not None:
        while(True):
            Customer_1 = Customer(data_out[0],data_out[1],data_out[2],data_out[3],data_out[4],data_out[6],data_out[7],data_out[8],data_out[5])

            if count == 1:
                print("\nLogin successful. Welcome back, " + Customer_1.Name + "!")
                count += 1

            print("\n\n         What would you like to do today:\n")
            print("         1. Make a Transaction to a Friend                    2. Check Your Transactions list\n")
            print("         3. Make a Transaction to a Merchant                  4. Check Your Merchant Transactions\n")
            print("         5. Check Your Balance                                6. Take a loan\n")
            print("         7. Check your details                                8. Edit your details\n")
            print("         9. Pay loan                                          10. See loan payments\n")
            print("         11. Exit")
            choice_today = input("Enter your choice: ")

            print("\n\n")

            if choice_today == "1":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                mycursor = conn.cursor()

                mycursor.execute("BEGIN")

                sql = "SELECT * FROM customer WHERE cust_id = %s AND mpin = %s;"
                mycursor.execute(sql, (Cust_id, UPI_Pin))
                data_from = mycursor.fetchone()

                sql = "SELECT cust_id FROM defaulter WHERE cust_id = %s"
                mycursor.execute( sql, (Customer_1.Cust_id,) )
                defaulter = mycursor.fetchone()

                if defaulter is not None:
                    print("You are a defaulter. You didn't pay the existing loan. Please clear the loan to make a transaction.")
                    continue

                acc_num = input("Enter the customer id to which you would like to transfer money [Type \'SEARCH\' to search for names]: ")

                if acc_num == "SEARCH":
                    acc_num = search()
                    if acc_num == "EXIT":
                        continue

                sql = "SELECT * FROM customer WHERE cust_id = %s;"
                mycursor.execute(sql,(acc_num,))
                data_to = mycursor.fetchone()

                if data_to is None:
                    print("The account is not available!!!!")
                    mycursor.execute("ROLLBACK")
                else:
                    if data_from[0] == data_to[0]:
                        print("You cant send money to yourself. Try typing different customer ID")
                    else:
                        pin = input("Enter your UPI pin: ")

                        if pin == data_from[4]:
                            print("Your current balance is : Rs. ", data_from[6], " /-")

                            while True:
                                amount = int(input("Enter the amount you would like to transfer: "))
                                if amount < 0:
                                    print("You entered negative amount. Please enter again.")
                                    continue
                                elif amount == 0:
                                    print("You entered 0. Please enter again.")
                                    continue
                                else:
                                    break

                            balance_amount = data_from[6] - amount

                            if balance_amount > 0:
                                sql = "UPDATE customer SET balance = %s WHERE cust_id = %s;"
                                values = (balance_amount, data_from[0])
                                mycursor.execute(sql, values)

                                transfer_amount = int(data_to[6]) + amount
                                sql = "UPDATE customer SET balance = %s WHERE cust_id = %s;"
                                values = (transfer_amount, acc_num)
                                mycursor.execute(sql, values)

                                t_id=transaction_id_generator(data_from[0], acc_num)
                                current_date = datetime.date.today()
                                current_time = datetime.datetime.now().time()

                                sql = "INSERT INTO transactions VALUES (%s,%s,%s,%s,%s,%s);"
                                values=(t_id, data_from[0], acc_num, current_date, current_time, amount)
                                mycursor.execute(sql,values)

                                mycursor.execute("COMMIT")

                                print("The money has been sent successfully.")
                            else:
                                print("Insufficient balance.!!!!")
                                
                                mycursor.execute("ROLLBACK")
                        else:
                            print("Wrong UPI Pin!!!!!")
                            mycursor.execute("ROLLBACK")

            elif choice_today == "2":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                print("\t 1. Complete Transaction")
                print("\t 2. Transactions done by you")
                print("\t 3. Transactions done to you")
                print("\t 4. Transactions with a person")

                trans_choice = input("Select from above : ")

                if( trans_choice == "1" ):

                    sql = "SELECT * FROM transactions WHERE sender_id = %s OR reciever_id = %s ORDER BY dte, time DESC"
                    mycursor.execute(sql, (Customer_1.Cust_id, Customer_1.Cust_id))
                    rows = mycursor.fetchall()
                    if rows is None:
                        print("No trasactions found")
                    else:
                        print("|-----------------------------------------------------------------------------------------------------------------------|")
                        print("| Transaction id\t\t| Sender\t| Reciever\t| Date\t\t| Time\t\t\t| amount\t|")
                        print("|-----------------------------------------------------------------------------------------------------------------------|")

                        for row in rows:
                            print("|", row[0],"\t|",row[1],"\t|",row[2],"\t|",row[3],"\t|",row[4],"\t|",row[5],"\t\t|")

                        print("|-----------------------------------------------------------------------------------------------------------------------|")

                elif trans_choice == "2":
                    sql = "SELECT * FROM transactions WHERE sender_id = %s ORDER BY dte, time DESC"
                    mycursor.execute(sql, (Customer_1.Cust_id,))
                    rows = mycursor.fetchall()

                    if rows is None:
                        print("No transactions found")
                    else:
                        print("|-----------------------------------------------------------------------------------------------------------------------|")
                        print("| Transaction id\t\t| Receiver\t| Date\t\t| Time\t\t\t| amount\t|")
                        print("|-----------------------------------------------------------------------------------------------------------------------|")

                        for row in rows:
                            sql = "SELECT name FROM customer WHERE cust_id = %s"
                            mycursor.execute(sql, (row[2],))
                            name = mycursor.fetchone()

                            print("|", row[0],"\t|",name[0],"\t|",row[3],"\t|",row[4],"\t|",row[5],"\t\t|")
                        
                        print("|-----------------------------------------------------------------------------------------------------------------------|")

                elif trans_choice == "3":
                    sql = "SELECT * FROM transactions WHERE reciever_id = %s ORDER BY dte, time DESC"
                    mycursor.execute(sql, (Customer_1.Cust_id,))
                    rows = mycursor.fetchall()

                    if rows is None:
                        print("No transactions found")
                    else:
                        print("|-----------------------------------------------------------------------------------------------------------------------|")
                        print("| Transaction id\t\t| Sender\t| Date\t\t| Time\t\t\t| amount\t|")
                        print("|-----------------------------------------------------------------------------------------------------------------------|")

                        for row in rows:
                            sql = "SELECT name FROM customer WHERE cust_id = %s"
                            mycursor.execute(sql, (row[1],))
                            name = mycursor.fetchone()

                            print("|", row[0],"\t|",name[0],"\t|",row[3],"\t|",row[4],"\t|",row[5],"\t\t|")
                        
                        print("|-----------------------------------------------------------------------------------------------------------------------|")

                elif trans_choice == "4":
                    person = input("Enter person id : ")
                    sql = "SELECT * FROM transactions WHERE sender_id = %s AND reciever_id = %s OR sender_id = %s AND reciever_id = %s ORDER BY dte, time DESC"
                    mycursor.execute(sql, (person, Customer_1.Cust_id, Customer_1.Cust_id, person))
                    rows = mycursor.fetchall()
                    if rows is None:
                        print("No trasactions found")
                    else:
                        print("|-----------------------------------------------------------------------------------------------------------------------|")
                        print("| Transaction id\t\t| Sender\t| Receiver\t| Date\t\t| Time\t\t\t| amount\t|")
                        print("|-----------------------------------------------------------------------------------------------------------------------|")

                        for row in rows:
                            sql = "SELECT name FROM customer WHERE cust_id = %s"
                            mycursor.execute(sql, (row[1],))
                            sender = mycursor.fetchone()

                            sql = "SELECT name FROM customer WHERE cust_id = %s"
                            mycursor.execute(sql, (row[2],))
                            reciever = mycursor.fetchone()

                            print("|", row[0],"\t|",sender[0],"\t|",reciever[0],"\t|",row[3],"\t|",row[4],"\t|",row[5],"\t\t|")

                        print("|-----------------------------------------------------------------------------------------------------------------------|")


            elif choice_today == "3":
                
                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                mycursor = conn.cursor()

                mycursor.execute("BEGIN")

                sql = "SELECT * FROM customer WHERE cust_id = %s AND mpin = %s;"
                mycursor.execute(sql, (Cust_id, UPI_Pin))
                data_from = mycursor.fetchone()

                sql = "SELECT cust_id FROM defaulter WHERE cust_id = %s"
                mycursor.execute( sql, (Customer_1.Cust_id,) )
                defaulter = mycursor.fetchone()

                if defaulter is not None:
                    print("You are a defaulter. You didn't pay the existing loan. Please clear the loan to make a transaction.")
                    continue

                phone_number = input("Enter the merchant phone number to which you would like to transfer money : ")

                sql = "SELECT * FROM merchant WHERE phone = %s;"
                mycursor.execute(sql,(phone_number,))
                data_to = mycursor.fetchone()

                if data_to is None:
                    print("The merchant is not available!!!!")
                    mycursor.execute("ROLLBACK")
                else:
                    pin = input("Enter your UPI pin: ")

                    if pin == data_from[4]:
                        print("Your current balance is : Rs. ", data_from[6], " /-")

                        while True:
                            amount = int(input("Enter the amount you would like to transfer: "))
                            if amount < 0:
                                print("You entered negative amount. Please enter again.")
                                continue
                            elif amount == 0:
                                print("You entered 0. Please enter again.")
                                continue
                            else:
                                break

                        balance_amount = data_from[6] - amount

                        if balance_amount > 0:
                            sql = "UPDATE customer SET balance = %s WHERE cust_id = %s;"
                            values = (balance_amount, data_from[0])
                            mycursor.execute(sql, values)

                            sql = "SELECT merch_id FROM merchant WHERE phone = %s"
                            mycursor.execute(  sql, (phone_number,))
                            phone_rows = mycursor.fetchone()

                            transfer_amount = int(data_to[6]) + amount
                            sql = "UPDATE merchant SET balance = %s WHERE merch_id = %s;"
                            values = (transfer_amount, phone_rows[0])
                            mycursor.execute(sql, values)

                            t_id=transaction_id_generator(data_from[0], phone_rows[0])
                            current_date = datetime.date.today()
                            current_time = datetime.datetime.now().time()

                            sql = "INSERT INTO merchant_transactions VALUES (%s,%s,%s,%s,%s,%s);"
                            values=(t_id, data_from[0], phone_rows[0], current_date, current_time, amount)
                            mycursor.execute(sql,values)

                            mycursor.execute("COMMIT")

                            print("The money has been sent successfully.")
                        else:
                            print("Insufficient balance.!!!!")
                            
                            mycursor.execute("ROLLBACK")
                    else:
                        print("Wrong UPI Pin!!!!!")
                        mycursor.execute("ROLLBACK")

            elif choice_today == "4":

                sql = "SELECT * FROM merchant_transactions WHERE sender_id = %s"
                mycursor.execute( sql, (Customer_1.Cust_id, ) )
                rows = mycursor.fetchall()

                print("|-------------------------------------------------------------------------------------------------------------------| ")

                print("  Transaction_ID\t\t Merchant_Name \t Merchant_Phone \t Date \t\t Time \t\t\t Amount ")

                for row in rows:
                    sql = " SELECT * from merchant WHERE merch_id = %s "
                    mycursor.execute( sql, (row[2], ) )
                    merchant = mycursor.fetchone()

                    print(" ", row[0], "\t", merchant[1], "\t", merchant[2], "\t", row[3], "\t", row[4], "\t", row[5])

                print("|-------------------------------------------------------------------------------------------------------------------| ")


            elif choice_today == "5":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                sql = "SELECT * FROM customer WHERE cust_id = %s;"
                mycursor.execute(sql,(Customer_1.Cust_id,))
                rows=mycursor.fetchone()

                print("|-------------------------------------------")
                print("|   The balance amount is: Rs.",rows[6], "/-\t|")
                print("|-------------------------------------------")
        
            elif choice_today == "6":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )
                
                sql = "SELECT cust_id FROM loan WHERE cust_id = %s"
                mycursor.execute(sql,(Customer_1.Cust_id,))
                row = mycursor.fetchone()

                if row is None:
                    sql = "SELECT * FROM customer WHERE cust_id = %s;"
                    mycursor.execute(sql,(Customer_1.Cust_id,))
                    rows=mycursor.fetchall()
                    if data_out is not None:
                        loan_id = generate_loan_id(data_out[7], data_out[0])

                        while True:
                                loan_amt = int(input("How much loan do you want to take : "))
                                if loan_amt < 0:
                                    print("You entered negative amount. Please enter again.")
                                    continue
                                elif loan_amt == 0:
                                    print("You entered 0. Please enter again.")
                                    continue
                                else:
                                    break
                        
                        duration = int(input("For How long (in years): "))

                        emi = (loan_amt*1.0) / (duration*12.0)
                        today = datetime.date.today()
                        deadline = today + datetime.timedelta(days=365 * duration)

                        print("Here is you loan details : \n")
                        print("Total loan is Rs. " , loan_amt, "/-")
                        print("Your emi will be Rs. ", emi, " /-" )
                        print("Time to repay the loan (in years) : ", duration)
                        print("Last date to repay the loan : ", deadline)
                        choice_loan = input("Do you want to take the loan? [Y/N] : ")
                        if choice_loan == "Y":
                            sql = "INSERT INTO loan VALUES (%s, %s, %s, %s, %s, %s)"
                            mycursor.execute(sql,(loan_id, data_out[0], loan_amt, emi, deadline, loan_amt))

                            sql = "UPDATE customer SET balance = balance + %s WHERE cust_id = %s"
                            mycursor.execute(sql, (loan_amt, data_out[0]))

                            print("Loan taken successfully")
                            mycursor.execute("COMMIT")
                else:
                    print("You already have a loan. Clear that loan to take another loan.")

            elif choice_today=="7":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                sql = "SELECT * FROM customer WHERE cust_id = %s"
                mycursor.execute(sql, (Customer_1.Cust_id,))
                row = mycursor.fetchone()

                pin = input("Enter the UPI : ")
                if pin == Customer_1.M_pin:
                    print("\n\n|----------------------------------------------------------------|\n")
                    print("|         Customer id: ",Customer_1.Cust_id,"\n")
                    print("|         Name: ",Customer_1.Name,"\n")
                    print("|         Phone Number: ",Customer_1.Phone,"\n")
                    print("|         Email: ",row[3],"\n")
                    print("|         Account Number: ",Customer_1.Account_num,"\n")
                    print("|         Balance: Rs.",row[6],"\n")
                    print("|----------------------------------------------------------------|")
                else:
                    print("\nInvalid UPI Pin!!!!")
            

            elif choice_today =="8":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                print("\n\nWhich of the following detail would you like to edit: \n\n")
                print("             1. Name")
                print("             2. Phone Number")
                print("             3. Email")
                print("             4. MPIN")
                edit_choice=input("\nEnter your choice: ")

                if edit_choice != "1" and edit_choice != "2" and edit_choice != "3" and edit_choice != "4":
                    print("Wrong option")
                    continue

                if edit_choice == "1":
                    new = input("Enter your new name : ")
                    sql = "UPDATE customer SET name = %s WHERE cust_id = %s"
                    mycursor.execute(sql, ( new, Customer_1.Cust_id ))
                if edit_choice == "2":
                    new = input("Enter your new phone number : ")
                    while(phone_num_validate(new)==False):
                        Phone = input("Invalid phone number. Please Enter Again: ")
                    sql = "UPDATE customer SET phone = %s WHERE cust_id = %s"
                    mycursor.execute(sql, ( new, Customer_1.Cust_id ))
                if edit_choice == "3":
                    new = input("Enter your new email : ")
                    while(email_validate(new)==False):
                        Email = input("Invalid Email entered. Email should end with '@gmail.com'.\nPlease Enter Again: ")
                    sql = "UPDATE customer SET email = %s WHERE cust_id = %s"
                    mycursor.execute(sql, ( new, Customer_1.Cust_id ))
                if edit_choice == "4":
                    new = input("Enter your new MPIN : ")
                    while(mpin_validate(M_pin)==False):
                        M_pin = input("UPI Pin should be 6 digits. Please Enter Again: ")
                    sql = "UPDATE customer SET mpin = %s WHERE cust_id = %s"
                    mycursor.execute(sql, ( new, Customer_1.Cust_id ))

                print("Information updated successfully.")

            elif choice_today == "9":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                sql = "SELECT * FROM loan WHERE cust_id = %s"
                mycursor.execute( sql, (Customer_1.Cust_id,) )
                row = mycursor.fetchone()

                if row is not None:
                    print("-------------------------------------------------------------")
                    print("Your Loan Details :")
                    print(" Amount Taken \t EMI \t Deadline \t\t Due")
                    print(" ", row[2], " \t\t ", row[3], "\t ", row[4], "\t ", row[5])
                    print("-------------------------------------------------------------")

                    payment = int(input("Enter how much you want to pay : "))
                    sql = "SELECT balance FROM customer WHERE cust_id = %s"
                    mycursor.execute(sql,(Customer_1.Cust_id,))
                    result = mycursor.fetchone()
                    new_balance = int(result[0])-payment
                    if new_balance < 0:
                        print("Insufficient Balance!!!. You cannot pay the loan")
                    else:
                        new_due = int(row[5]) - payment
                        if new_due >= 0:
                            sql = "UPDATE customer SET balance = %s WHERE cust_id = %s"
                            mycursor.execute( sql, (new_balance, Customer_1.Cust_id) )
                            sql = "UPDATE loan SET due = %s WHERE cust_id = %s"
                            mycursor.execute( sql, (new_due, Customer_1.Cust_id) )
                            if new_due != 0:
                                print("Congratulations. Your new due is : ", new_due)
                            else:
                                print("Congratulations. You have cleared your debt.")
                                sql = "DELETE FROM loan WHERE cust_id = %s"
                                mycursor.execute( sql, (Customer_1.Cust_id,) )

                            sql = "INSERT INTO payments VALUES (%s, %s, %s, %s)"
                            current_date = datetime.date.today()
                            current_time = datetime.datetime.now().time()
                            mycursor.execute( sql, (Customer_1.Cust_id, current_date, current_time, payment) )

                        else:
                            print("You are paying more than what is owed. Not allowed")
                else:
                    print("You don't have any loan.")

                mycursor.execute("COMMIT")

            elif choice_today == "10":
                sql = "SELECT dte AS Date, time AS Time, payment AS Payment FROM payments WHERE cust_id = %s"
                mycursor.execute( sql, (Customer_1.Cust_id,) )
                rows = mycursor.fetchall()
                
                print("|----------------------------------------------|")

                if rows is None:
                    print("You don't have any loan payments")
                else:
                    
                    print("| Date \t\t Time \t\t Amount Paid |")
                    print()
                    for row in rows:
                        print("| ", row[0]," \t ", row[1]," \t ", row[2], " |")
                    
                    print()

                print("|----------------------------------------------|")

            elif choice_today == '11':
                break
            mycursor.execute("COMMIT")
    else:
        print("\nLogin failed. Please check your Customer ID and UPI pin.")

elif choice == "3":
    print("\n\n             Please Fill the following Details:\n")
    Name=input("Enter Your Name: ")

    Phone = input("Enter Your Phone Number: ")
    while(phone_num_validate(Phone)==False):
        Phone = input("Invalid phone number. Please Enter Again: ")

    Email = input("Enter Your Email id [If you don't have one, enter NA]: ")
    if( Email != "NA" ):
        while not email_validate(Email):
            Email = input("Invalid Email entered. Email should end with '@gmail.com'.\nPlease Enter Again: ")

    M_pin = input("Enter a 6-digit UPI pin: ")
    while(mpin_validate(M_pin)==False):
        M_pin = input("UPI Pin should be 6 digits. Please Enter Again: ")

    print("\n           BANKS LIST:")
    sql = "SELECT DISTINCT bank_name FROM bank ORDER BY bank_name"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count = 1

    l = []

    for row in rows:
        print(count, ". ", row[0])
        count += 1

    ch = int(input("Enter in which bank is your account in: "))

    sql = "SELECT DISTINCT bank_id FROM bank ORDER BY bank_id"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count = 1

    for row in rows:
        if count == ch:
            Bank_id = row[0]
            break
        count = count + 1

    print(Bank_id)
    print("             BRANCHES LIST \n")
    sql = "SELECT branch FROM bank where bank_id = %s;"
    mycursor.execute(sql,(Bank_id,))
    rows = mycursor.fetchall()
    count = 1

    for row in rows:
        row_str = '\t'.join(map(str, row))
        print(count,". ",row_str)
        count = count + 1

    ch=int(input("Enter the branch of the bank in which your account is present: "))

    sql = "SELECT branch_id FROM bank where bank_id = %s;"
    mycursor.execute(sql,(Bank_id,))
    rows = mycursor.fetchall()
    count  = 1

    for row in rows:
        row_str = '\t'.join(map(str, row))
        if count == ch:
            Branch_id = row_str
            break
        count = count + 1

    sql = "SELECT max(merch_id) FROM merchant"
    mycursor.execute(sql)
    max_id = mycursor.fetchone()[0]
    Cust_id=cust_id_generator(max_id)
    Account_num=account_number(Bank_id, Branch_id, Cust_id)
    Customer_1 = Customer(Cust_id, Name, Phone, Email, M_pin, 0, Bank_id, Branch_id, Account_num)

    l = []
    l.append(Customer_1.Cust_id)
    l.append(Customer_1.Name)
    l.append(Customer_1.Phone)
    l.append(Customer_1.Email)
    l.append(Customer_1.M_pin)
    l.append(Customer_1.Account_num)
    l.append(0)
    l.append(Customer_1.Bank_id)
    l.append(Customer_1.Branch_id)

    # cust_id | name | phone | email | mpin | acc_no | balance | bank_id | branch_id

    sql = "INSERT INTO merchant VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, tuple(l))

    print("\n\nSign in Successful. Here are your details.\n")

    print("Merch_ID : " , Customer_1.Cust_id)
    print("Name : ", Customer_1.Name)
    print("Phone :", Customer_1.Phone)
    print("Email : ", Customer_1.Email)
    print("MPIN : ",Customer_1.M_pin)
    print("Account Number : ", Customer_1.Account_num)
    print("Balance : ", Customer_1.Balance)

    mycursor.execute("SELECT DISTINCT branch FROM bank WHERE branch_id = %s", (Customer_1.Branch_id,))
    branch = mycursor.fetchall()[0]

    mycursor.execute("SELECT bank_name FROM bank WHERE bank_id = %s", (Customer_1.Bank_id,))
    bank = mycursor.fetchall()[0]

    print("Bank : ", bank[0])
    print("Branch : ", branch[0])

    print("\n\nThank you for choosing phonepe.")

    conn.commit()

elif choice == "4":
    print()

    conn= psycopg2.connect(
    host="localhost",
    port=5432,
    database="phonepe",
    user="ayushmaan",
    password="1234"
    )

    mycursor = conn.cursor()

    print("\n\nPlease Enter your details as follows:\n")
    Cust_id = input("Enter your Merchant id: ")
    UPI_Pin = input("Enter your UPI pin: ")

    # Check if the customer with the given Cust_id and UPI_Pin exists in the database
    sql = "SELECT * FROM merchant WHERE merch_id = %s AND mpin = %s;"
    mycursor.execute(sql, (Cust_id, UPI_Pin))
    data_out = mycursor.fetchone()
    
    count = 1

    if data_out is not None:
        while(True):
            Merchant = Customer(data_out[0],data_out[1],data_out[2],data_out[3],data_out[4],data_out[6],data_out[7],data_out[8],data_out[5])

            if count == 1:
                print("\nLogin successful. Welcome back, " + Merchant.Name + "!")
                count += 1

            print("\n\n         What would you like to do today:\n")
            print("         1. Check Your Transactions list           2. Check Your Balance\n")
            print("         3. Check your details                     4. Edit your details\n")
            print("         5. Exit")
            choice_today = input("Enter your choice: ")

            if choice_today == "1":
                
                sql = "SELECT * FROM merchant_transactions WHERE reciever_id = %s"
                mycursor.execute( sql, (Merchant.Cust_id, ) )
                rows = mycursor.fetchall()

                print("|-------------------------------------------------------------------------------------------------------------------| ")

                print("  Transaction_ID\t\t Sender_Name \t Sender_Phone \t Date \t\t Time \t\t\t Amount ")

                for row in rows:
                    sql = " SELECT * from customer WHERE cust_id = %s "
                    mycursor.execute( sql, (row[1], ) )
                    customer = mycursor.fetchone()

                    print(" ", row[0], "\t", customer[1], "\t", customer[2], "\t", row[3], "\t", row[4], "\t", row[5])

                print("|-------------------------------------------------------------------------------------------------------------------| ")

            elif choice_today == "2":
                
                sql = "SELECT balance FROM merchant WHERE merch_id = %s"
                mycursor.execute( sql, (Merchant.Cust_id, ) )
                row = mycursor.fetchone()

                print("|---------------------------------------|")
                print("|   The balance amount is: Rs.",row[0], "/-\t|")
                print("|---------------------------------------|")

            elif choice_today == "3":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                sql = "SELECT * FROM merchant WHERE merch_id = %s"
                mycursor.execute(sql, (Merchant.Cust_id,))
                row = mycursor.fetchone()

                pin = input("Enter the UPI : ")
                if pin == Merchant.M_pin:
                    print("\n\n|----------------------------------------------------------------|\n")
                    print("|         Merchant id: ",Merchant.Cust_id,"\n")
                    print("|         Name: ",Merchant.Name,"\n")
                    print("|         Phone Number: ",Merchant.Phone,"\n")
                    print("|         Email: ",row[3],"\n")
                    print("|         Account Number: ",Merchant.Account_num,"\n")
                    print("|         Balance: Rs.",row[6],"\n")
                    print("|----------------------------------------------------------------|")
                else:
                    print("\nInvalid UPI Pin!!!!")

            elif choice_today == "4":
                
                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="ayushmaan",
                password="1234"
                )

                print("\n\nWhich of the following detail would you like to edit: \n\n")
                print("             1. Name")
                print("             2. Phone Number")
                print("             3. Email")
                print("             4. MPIN")
                edit_choice=input("\nEnter your choice: ")

                if edit_choice != "1" and edit_choice != "2" and edit_choice != "3" and edit_choice != "4":
                    print("Wrong option")
                    continue

                if edit_choice == "1":
                    new = input("Enter your new name : ")
                    sql = "UPDATE merchant SET name = %s WHERE merch_id = %s"
                    mycursor.execute(sql, ( new, Merchant.Cust_id ))
                if edit_choice == "2":
                    new = input("Enter your new phone number : ")
                    while(phone_num_validate(new)==False):
                        Phone = input("Invalid phone number. Please Enter Again: ")
                    sql = "UPDATE merchant SET phone = %s WHERE merch_id = %s"
                    mycursor.execute(sql, ( new, Merchant.Cust_id ))
                if edit_choice == "3":
                    new = input("Enter your new email : ")
                    while(email_validate(new)==False):
                        Email = input("Invalid Email entered. Email should end with '@gmail.com'.\nPlease Enter Again: ")
                    sql = "UPDATE merchant SET email = %s WHERE merch_id = %s"
                    mycursor.execute(sql, ( new, Merchant.Cust_id ))
                if edit_choice == "4":
                    new = input("Enter your new MPIN : ")
                    while(mpin_validate(M_pin)==False):
                        M_pin = input("UPI Pin should be 6 digits. Please Enter Again: ")
                    sql = "UPDATE merchant SET mpin = %s WHERE merch_id = %s"
                    mycursor.execute(sql, ( new, Merchant.Cust_id ))

                print("Information updated successfully.")

            elif choice_today == "5":
                break

    else:
        print("Login Failed. Check your Merch_ID / MPIN.")


################################################################################################################

conn.commit()
conn.close()
mycursor.close()
