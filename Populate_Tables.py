import psycopg2
import csv

conn = psycopg2.connect(host="localhost",
                        user="postgres",
                        password="1234",
                        port=5432)

mycursor = conn.cursor()
        
with open("Bank_Data.csv", "r") as ip:
    csv_reader = csv.reader(ip)

    for record in csv_reader:
        line = "INSERT INTO BANK VALUES (\'" + record[0] + "\',\'" + record[1] + "\',\'" + record[2] + "\',\'" + record[3] + "\');"
        mycursor.execute(line)

with open("Customer_Data.csv", "r") as ip:
    csv_reader = csv.reader(ip)

    for record in csv_reader:
        line = "INSERT INTO CUSTOMER VALUES (\'" + record[0] + "\',\'" + record[1] + "\',\'" + record[2] + "\',\'" + record[3] + "\',\'" + record[4] + "\',\'" + record[5] + "\',\'" + record[6] + "\',\'" + record[7] + "\');"
        mycursor.execute(line)
        
with open("Tranactions_Data.csv", "r") as ip:
    csv_reader = csv.reader(ip)

    for record in csv_reader:
        line = "INSERT INTO TRANSACTIONS VALUES (\'" + record[0] + "\',\'" + record[1] + "\',\'" + record[2] + "\',\'" + record[3] + "\',\'" + record[4] + "\',\'" + record[5] + "\');"
        mycursor.execute(line)
        
with open("Loan_Data.csv", "r") as ip:
    csv_reader = csv.reader(ip)

    for record in csv_reader:
        line = "INSERT INTO LOAN VALUES (\'" + record[0] + "\',\'" + record[1] + "\',\'" + record[2] + "\',\'" + record[3] + "\',\'" + record[4] + "\',\'" + record[5] + "\');"
        mycursor.execute(line)
        
with open("Defaulters_Data.csv", "r") as ip:
    csv_reader = csv.reader(ip)

    for record in csv_reader:
        line = "INSERT INTO DEFAULTER VALUES (\'" + record[0] + "\',\'" + record[1] + "\',\'" + record[2] + "\');"
        mycursor.execute(line)

conn.commit()
conn.close()
mycursor.close()
