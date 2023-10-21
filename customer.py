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
############################################################################################################
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


###########################################################################################################

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
        print(ss)

    ch = int(input("Enter in which bank is your account in: "))

###########################################################################################################

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

###########################################################################################################
    print(Bank_id)
    print("             Branches Available \n")
    sql = "SELECT branch FROM bank where bank_id = %s;"
    mycursor.execute(sql,(Bank_id,))
    rows = mycursor.fetchall()
    count = 1

    for row in rows:
        row_str = '\t'.join(map(str, row))
        print(count,". ",row_str)
        count = count + 1
    
###########################################################################################################

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
    l.append(int(0))
    l.append(Customer_1.Bank_id)
    l.append(Customer_1.Branch_id)

    # cust_id | name | phone | email | mpin | acc_no | balance | bank_id | branch_id

    sql = "INSERT INTO customer (cust_id, name, phone, email, mpin, acc_no, balance, bank_id, branch_id) VALUES (%s, %s, %s, %s, %s, %s, %d, %s, %s)"
    mycursor.execute(sql, l)
    
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

###########################################################################################################
    
elif choice == "2":

    print("\n\nPlease Enter your details as follows:\n")
    Cust_id = input("Enter your customer id: ")
    UPI_Pin = input("Enter your UPI pin: ")

    # Check if the customer with the given Cust_id and UPI_Pin exists in the database
    sql = "SELECT * FROM customer WHERE cust_id = %s AND mpin = %s;"
    mycursor.execute(sql, (Cust_id, UPI_Pin))
    data = mycursor.fetchone()
    
    count = 1

    if data is not None:
        while(True):
            Customer_1 = Customer(data[0],data[1],data[2],data[3],data[4],data[6],data[7],data[8],data[5])
            # Customer authentication is successful
            if count == 1:
                print("\nLogin successful. Welcome back, " + Customer_1.Name + "!")  # Assuming the name is in the second column (index 1)
                count += 1
            # Now you can implement the functionality for existing customers
            # For example, display account balance, perform transactions, etc.

            # Implement your functionality here

            print("\n\n         What would you like to do today:\n")
            print("         1. Make a Transaction                     2. Check Your Balance\n")
            print("         3. Check Your Transactions list           4. Take a loan\n")
            print("         5. Check your details                     6. Edit your details\n")
            print("         7. Exit")
            choice_today = input("Enter your choice: ")

            if choice_today == "1":
                sql ="begin;"
                mycursor.execute(sql)
                acc_num = input("Enter the customer id to which you would like to transfer money: ")
                pin = input("Enter your upi pin: ")
                if pin == Customer_1.M_pin:
                    amount = int(input("Enter the amount you would like to transfer: "))
                    balance_amount = int(Customer_1.Balance) - amount
                    if balance_amount > 0:
                        sql = "UPDATE customer SET balance = %s WHERE cust_id = %s;"
                        values = (balance_amount,Customer_1.Cust_id)
                        mycursor.execute(sql,values)
                        sql = "SELECT * FROM customer WHERE cust_id = %s;"
                        mycursor.execute(sql,(acc_num,))
                        data = mycursor.fetchone()
                        if data is not None:
                            transfer_amount = int(data[6])+amount
                            sql = "UPDATE customer SET balance = %s WHERE cust_id = %s;"
                            values = (transfer_amount,acc_num)
                            mycursor.execute(sql,values)
                            t_id=transaction_id_generator(Customer_1.Cust_id,acc_num)
                            current_date = datetime.date.today()
                            current_time = datetime.datetime.now().time()
                            sql = "INSERT INTO transactions VALUES (%s,%s,%s,%s,%s,%s);"
                            values=(t_id,Customer_1.Cust_id,acc_num,current_date,current_time,amount)
                            mycursor.execute(sql,values)
                            sql = "commit;"
                            mycursor.execute(sql)
                        else:
                            print("The account is not available!!!!")
                            sql = "rollback;"
                            mycursor.execute(sql)
                    else:
                        print("Insufficient balance.!!!!")
                        sql = "rollback;"
                        mycursor.execute(sql)
                else:
                    print("Wrong UPI Pin!!!!!")
                    sql = "rollback;"
                    mycursor.execute(sql)

            if choice_today == "2":
                sql = "SELECT * FROM customer WHERE cust_id = %s;"
                mycursor.execute(sql,(Customer_1.Cust_id,))
                rows=mycursor.fetchall()
                if data is not None:
                    print("The balance amount is: Rs.",data[6], "/-")

            if choice_today == "3":
                sql = "SELECT * FROM transactions WHERE sender_id = %s OR reciever_id = %s;"
                mycursor.execute(sql, (Customer_1.Cust_id, Customer_1.Cust_id))
                rows = mycursor.fetchall()
                if rows is None:
                    print("No trasactions found")
                else:
                    print("Transaction id\t\t\t Sender\t Receiver\t amount\t")
                    for row in rows:
                        print(row[0],"\t",row[2],"\t\t",row[5])

            if choice_today=="5":
                pin = input("Enter the upi pin: ")
                if pin == Customer_1.M_pin:
                    print("\n\n----------------------------------------------------------------\n")
                    print("         Customer id: ",Customer_1.Cust_id,"\n")
                    print("         Name: ",Customer_1.Name,"\n")
                    print("         Phone Number: ",Customer_1.Phone,"\n")
                    print("         Email: ",Customer_1.Email,"\n")
                    print("         Account Number: ",Customer_1.Account_num,"\n")
                    print("         Balance: Rs.",Customer_1.Balance,"\n")
                    print("----------------------------------------------------------------")
                else:
                    print("Invalid UPI Pin!!!!")

            if choice_today =="6":
                print("\n\nWhich of the following detail would you like to edit: \n")
                print("             1.Name")
                print("             2.Email")
                print("             3.Phone Number")
                print("             4.mpin")
                edit_choice=input("Enter your choice: ")

            if choice_today == '7':
                break

    else:
        print("\nLogin failed. Please check your Customer id and UPI pin.")

################################################################################################################



conn.commit()
conn.close()
mycursor.close()






