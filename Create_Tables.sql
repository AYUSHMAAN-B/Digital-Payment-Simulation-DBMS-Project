CREATE TABLE BANK (
			
			branch_id	VARCHAR(100) NOT NULL,
			bank_id		VARCHAR(100) NOT NULL,
			branch		VARCHAR(255) NOT NULL,
			bank_name	VARCHAR(255) NOT NULL,
			
			PRIMARY KEY(branch_id, bank_id),
			UNIQUE(bank_id)
			
			);
			
CREATE TABLE CUSTOMER (
    cust_id VARCHAR(100) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    mpin VARCHAR(100) NOT NULL,
    acc_no VARCHAR(100) NOT NULL,
    balance INT CHECK(balance >= 0),
    bank_id VARCHAR(255) NOT NULL ,
    branch_id VARCHAR(100) NOT NULL,
	FOREIGN KEY (bank_id, branch_id) REFERENCES BANK (bank_id, branch_id)
);

			
CREATE TABLE TRANSACTIONS (

			trans_id	VARCHAR(100) NOT NULL,
			sender_id	VARCHAR(100) NOT NULL REFERENCES CUSTOMER(cust_id),
			reciever_id	VARCHAR(100) NOT NULL REFERENCES CUSTOMER(cust_id),
			dte			VARCHAR(100),
			time		VARCHAR(100),
			amount		INT NOT NULL
			
			);
			
CREATE TABLE LOAN (

			loan_id		VARCHAR(100) NOT NULL PRIMARY KEY,
			bank_id		VARCHAR(255) NOT NULL REFERENCES BANK(bank_id),
			cust_id		VARCHAR(100) NOT NULL REFERENCES CUSTOMER(cust_id),
			amount		int  NOT NULL,
			emi			int NOT NULL,
			deadline	timestamp

			);
			
CREATE TABLE DEFAULTER (

			cust_id VARCHAR(100) NOT NULL REFERENCES CUSTOMER(cust_id),
			due 	int  NOT NULL,
			penalty int NOT NULL

			);
