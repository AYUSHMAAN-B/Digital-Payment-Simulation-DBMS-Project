# import psycopg2
# conn= psycopg2.connect(
#     host="localhost",
#     port=5432,
#     database="phonepe",
#     user="postgres",
#     password="1234"
# )

# mycursor = conn.cursor()

# print("             Branches Available \n")
# sql = "SELECT branch FROM bank;"
# mycursor.execute(sql)
# rows = mycursor.fetchall()
# count = 1
# for row in rows:
#     row_str = '\t'.join(map(str, row))
#     print(count,". ",row_str)
#     count = count + 1
# conn.commit()
# conn.close()
# mycursor.close()
# Get the current date
import datetime

# Get the current date and time
current_datetime = datetime.datetime.now()

# Extract year, month, day, hour, minute, and second
current_year = current_datetime.year
current_month = current_datetime.month
current_day = current_datetime.day
current_hour = current_datetime.hour
current_minute = current_datetime.minute
current_second = current_datetime.second

# Print the individual components
print("Year:", current_year)
print("Month:", current_month)
print("Day:", current_day)
print("Hour:", current_hour)
print("Minute:", current_minute)
print("Second:", current_second)

# ALTER TABLE transactions
# ALTER COLUMN time SET DATA TYPE varchar(100);
