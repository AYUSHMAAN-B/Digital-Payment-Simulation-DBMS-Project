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

#########################################################################################################

conn= psycopg2.connect(
    host="localhost",
    port=5432,
    database="phonepe",
    user="postgres",
    password="123456"
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

print("     1.New Customer: Sign Up                  2.Existing Customer: Login\n")
choice =input("Please Enter your choice: ")

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
    sql = "SELECT bank_name FROM bank;"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count = 1

    l = []

    for row in rows:
        row_str = '\t'.join(map(str, row))
        l.append(row_str)

    s = set(l)

    for ss in s:
        print(count, ". ", ss)
        count += 1

    ch = int(input("Enter in which bank is your account in: "))

    sql = "SELECT bank_id FROM bank;"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count = 1

    for row in rows:
        row_str = '\t'.join(map(str, row))

        if count == ch:
            Bank_id = row_str
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

###########################################################################################################

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
    mycursor.execute(sql, (l,))
    
    print("\n\nSign in Successful. Here are your details.\n")

    print("Cust_ID : " , Customer_1.Cust_id)
    print("Name : ", Customer_1.Name)
    print("Phone :", Customer_1.Phone)
    print("Email : ", Customer_1.Email)
    print("MPIN : ",Customer_1.M_pin)
    print("Account Number : ", Customer_1.Account_num)
    print("Balance : ", Customer_1.Balance)

    mycursor.execute("SELECT DISTINCT branch FROM bank WHERE branch_id = %s", Customer_1.Branch_id)
    branch = mycursor.fetchall()[0]

    mycursor.execute("SELECT bank_name FROM bank WHERE bank_id = %s", Customer_1.Bank_id)
    bank = mycursor.fetchall()[0]

    print("Bank : ", bank)
    print("Branch : ", branch)

    print("\n\nThank you for choosing phonepe.")

    conn.commit()
    conn.close()
    mycursor.close()

###########################################################################################################
    
elif choice == "2":

    conn= psycopg2.connect(
    host="localhost",
    port=5432,
    database="phonepe",
    user="postgres",
    password="123456"
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
            print("         1. Make a Transaction                     2. Check Your Balance\n")
            print("         3. Check Your Transactions list           4. Take a loan\n")
            print("         5. Check your details                     6. Edit your details\n")
            print("         7. Exit")
            choice_today = input("Enter your choice: ")

            print("\n\n")

            if choice_today == "1":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="postgres",
                password="123456"
                )

                mycursor = conn.cursor()

                mycursor.execute("BEGIN")

                sql = "SELECT * FROM customer WHERE cust_id = %s AND mpin = %s;"
                mycursor.execute(sql, (Cust_id, UPI_Pin))
                data_from = mycursor.fetchone()

                acc_num = input("Enter the customer id to which you would like to transfer money: ")
                sql = "SELECT * FROM customer WHERE cust_id = %s;"
                mycursor.execute(sql,(acc_num,))
                data_to = mycursor.fetchone()

                if data_to is None:
                    print("The account is not available!!!!")
                    mycursor.execute("ROLLBACK")
                else:
                    pin = input("Enter your UPI pin: ")

                    if pin == data_from[4]:
                        print("Your current balance is : Rs. ", data_from[6], " /-")
                        amount = int(input("Enter the amount you would like to transfer: "))
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
                user="postgres",
                password="123456"
                )

                sql = "SELECT * FROM customer WHERE cust_id = %s;"
                mycursor.execute(sql,(Customer_1.Cust_id,))
                rows=mycursor.fetchone()

                print("|-------------------------------------------")
                print("|   The balance amount is: Rs.",rows[6], "/-\t|")
                print("|-------------------------------------------")

            elif choice_today == "3":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="postgres",
                password="123456"
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
                        print("| Transaction id\t\t| Sender\t| Receiver\t| Date\t\t| Time\t\t\t| amount\t|")
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
                    sql = "SELECT * FROM transactions WHERE sender_id = %s OR reciever_id = %s ORDER BY dte, time DESC"
                    mycursor.execute(sql, (person, person))
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


            elif choice_today == "4":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="postgres",
                password="123456"
                )

                sql = "SELECT * FROM customer WHERE cust_id = %s;"
                mycursor.execute(sql,(Customer_1.Cust_id,))
                rows=mycursor.fetchall()
                if data_out is not None:
                    loan_id = generate_loan_id(data_out[7], data_out[0])
                    loan_amt = int(input("How much loan do you want to take : "))
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
                        sql = "INSERT INTO loan VALUES (%s, %s, %s, %s, %s)"
                        mycursor.execute(sql,(loan_id, data_out[0], loan_amt, emi, deadline))

                        sql = "UPDATE customer SET balance = balance + %s WHERE cust_id = %s"
                        mycursor.execute(sql, (loan_amt, data_out[0]))

                        print("Loan taken successfully")
                        mycursor.execute("COMMIT")

            elif choice_today=="5":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="postgres",
                password="123456"
                )

                pin = input("Enter the upi pin: ")
                if pin == Customer_1.M_pin:
                    print("\n\n|----------------------------------------------------------------|\n")
                    print("|         Customer id: ",Customer_1.Cust_id,"\n")
                    print("|         Name: ",Customer_1.Name,"\n")
                    print("|         Phone Number: ",Customer_1.Phone,"\n")
                    print("|         Email: ",Customer_1.Email,"\n")
                    print("|         Account Number: ",Customer_1.Account_num,"\n")
                    print("|         Balance: Rs.",Customer_1.Balance,"\n")
                    print("|----------------------------------------------------------------|")
                else:
                    print("Invalid UPI Pin!!!!")
            

            elif choice_today =="6":

                conn= psycopg2.connect(
                host="localhost",
                port=5432,
                database="phonepe",
                user="postgres",
                password="123456"
                )

                print("\n\nWhich of the following detail would you like to edit: \n")
                print("             1.Name")
                print("             2.Email")
                print("             3.Phone Number")
                print("             4.mpin")
                edit_choice=input("Enter your choice: ")

            elif choice_today == '7':
                break
            mycursor.execute("COMMIT")
    else:
        print("\nLogin failed. Please check your Customer id and UPI pin.")

################################################################################################################

conn.commit()
conn.close()
mycursor.close()
