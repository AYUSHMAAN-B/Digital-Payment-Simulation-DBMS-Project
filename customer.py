import csv
import psycopg2
from decimal import Decimal
class Customer:
    def __init__(self, Cust_id,Name,Phone,Email,M_pin,Balance,Bank_id,Branch_id,Account_num):
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
    def __init__(self,Transaction_id,Receive_id,Send_id,amount):
        self.Transaction_id =   Transaction_id
        self.Receive_id     =   Receive_id
        self.Send_id        =   Send_id
        self.amount         =   amount

class Loan:
    def __init__(self,Loan_id,Amount,Deadline,EMI):
        self.Loan_id  =     Loan_id
        self.Amount   =     Amount
        self.Deadline =     Deadline
        self.EMI      =     EMI

class Defaulters:
    def __intit__(self,Penality,Due):
        self.Penality   =     Penality
        self.Due        =     Due
###########################################################################################################
def account_number(bank_id,branch_id,cust_id):
    return bank_id+branch_id+cust_id

def phone_num_validate(num):
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

conn= psycopg2.connect(
    host="localhost",
    port=5432,
    database="phonepe",
    user="postgres",
    password="1234"
)

mycursor = conn.cursor()

###########################################################################################################

text = "Phonepe"
styled_text = "\033[1;95m" + text + "\033[0m"

print ("|--------------------------------------------------------------------------------------|")
print ("|                                                                                      |")
print ("|                                "+styled_text+"                                               |")
print ("|                A trustworth app for your transactions,loans, bills and many more     |")
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
    Email = input("Enter Your Email id: ")
    while(email_validate(Email)==False):
        Email = input("Invalid Email entered. Email should end with '@gmail.com'.\nPlease Enter Again: ")
    M_pin = input("Enter a 6-digit UPI pin: ")
    while(mpin_validate(M_pin)==False):
        M_pin = input("UPI Pin should be 6 digits.Please Enter Again: ")


###########################################################################################################

    print("\n           BANKS LIST:")
    sql = "SELECT bank_name FROM bank;"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count = 1
    for row in rows:
        row_str = '\t'.join(map(str, row))
        print(count,". ",row_str)
        count = count +1
    ch = int(input("Enter in which bank is your account: "))

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

    sql = "SELECT branch FROM bank where bank_id = Bank_id;"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count = 1
    for row in rows:
        row_str = '\t'.join(map(str, row))
        print(count,". ",row_str)
        count = count + 1

###########################################################################################################

    ch=int(input("Enter the branch of the bank in which your account is present: "))
    sql = "SELECT branch_id FROM bank where bank_id = Bank_id;"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    count  = 1
    for row in rows:
        row_str = '\t'.join(map(str, row))
        if count == ch:
            Branch_id = row_str
            break
        count = count + 1

###########################################################################################################

    Cust_id  =  "2"
    Account_num=account_number(Bank_id,Branch_id,Cust_id)
    Customer_1 = Customer(Cust_id,Name,Phone,Email,M_pin,0,Bank_id,Branch_id,Account_num)
    # sql = "INSERT INTO customer values ('Cust_id','Name','Phone','Email','M_pin','Account_num',0,'Bank_id','Branch_id');"
    sql = "INSERT INTO customer (cust_id, name, phone, email, mpin, acc_no, balance, bank_id, branch_id) " \
      f"VALUES ('{Customer_1.Cust_id}', '{Customer_1.Name}', '{Customer_1.Phone}', " \
      f"'{Customer_1.Email}', '{Customer_1.M_pin}', '{Customer_1.Account_num}', " \
      f"{Customer_1.Balance}, '{Customer_1.Bank_id}', '{Customer_1.Branch_id}');"

    # cust_id | name | phone | email | mpin | acc_no | balance | bank_id | branch_id
    mycursor.execute(sql)
    conn.commit()





