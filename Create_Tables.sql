CREATE TABLE BANK (
			
			branch_id	CHAR(3) NOT NULL PRIMARY KEY,
			bank_id		CHAR(3) NOT NULL PRIMARY KEY,
			branch		VARCHAR(255) NOT NULL,
			bank_name	VARCHAR(255) NOT NULL
			
			);
			
CREATE TABLE CUSTOMER (
			
			cust_id CHAR(5) NOT NULL PRIMARY KEY,
			name	VARCHAR(100) NOT NULL,
			phone	NUMERIC(10,0) NOT NULL,
			email	VARCHAR(100),
			mpin	NUMERIC(6,0) NOT NULL,
			acc_no	CHAR(11) NOT NULL,
			balance	NUMERIC(15,0) CHECK(balance >= 0),
			bank_id REFERENCES BANK(bank_id)
			
			);
			
CREATE TABLE TRANSACTIONS (

			trans_id	CHAR(22) NOT NULL,
			sender_id	REFERENCES CUSTOMER(cust_id),
			reciever_id	REFERENCES CUSTOMER(cust_id),
			dte			date,
			time		timestamp,
			amount		NUMERIC(15,0) NOT NULL
			
			);
			
CREATE TABLE LOAN (

			loan_id		CHAR(8) NOT NULL PRIMARY KEY,
			bank_id		REFERENCES BANK(bank_id),
			cust_id		REFERENCES CUSTOMER(cust_id),
			amount		NUMERIC(15,0) NOT NULL,
			emi			NUMERIC(15,0) NOT NULL,
			deadline	timestamp

			);
			
CREATE TABLE DEFAULTER (

			cust_id REFERENCES CUSTOMER(cust_id),
			due 	NUMERIC(15,0) NOT NULL,
			penalty NUMERIC(15,0) NOT NULL

			);
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
