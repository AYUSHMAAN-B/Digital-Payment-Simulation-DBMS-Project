INSERT INTO bank VALUES ('HYD', 'SBI', 'Hyderabad', 'State Bank of India');
INSERT INTO bank VALUES ('HYD', 'BOB', 'Hyderabad', 'Bank of Boroda');
INSERT INTO bank VALUES ('HYD', 'AXB', 'Hyderabad', 'Axis Bank');
INSERT INTO bank VALUES ('HYD', 'CAB', 'Hyderabad', 'Canara Bank');
INSERT INTO bank VALUES ('DWD', 'SBI', 'Dharwad', 'State Bank of India');
INSERT INTO bank VALUES ('DWD', 'BOB', 'Dharwad', 'Bank of Boroda');
INSERT INTO bank VALUES ('DWD', 'AXB', 'Dharwad', 'Axis Bank');
INSERT INTO bank VALUES ('DWD', 'CAB', 'Dharwad', 'Canara Bank');
INSERT INTO bank VALUES ('BMB', 'SBI', 'Bombay', 'State Bank of India');
INSERT INTO bank VALUES ('BMB', 'BOB', 'Bombay', 'Bank of Boroda');
INSERT INTO bank VALUES ('BMB', 'AXB', 'Bombay', 'Axis Bank');
INSERT INTO bank VALUES ('BMB', 'CAB', 'Bombay', 'Canara Bank');
INSERT INTO bank VALUES ('RJY', 'SBI', 'Rajahmundry', 'State Bank of India');
INSERT INTO bank VALUES ('RJY', 'BOB', 'Rajahmundry', 'Bank of Boroda');
INSERT INTO bank VALUES ('RJY', 'AXB', 'Rajahmundry', 'Axis Bank');
INSERT INTO bank VALUES ('RJY', 'CAB', 'Rajahmundry', 'Canara Bank');

UPDATE customer SET balance = 1000 WHERE cust_id = '00001';


INSERT INTO CUSTOMER (cust_id, name, phone, email, mpin, acc_no, balance, bank_id, branch_id)
VALUES
('00004', 'Sanchi', '9485726132', 'sanchi@gmail.com', '444444', 'AXBDWD00004', 6415, 'AXB', 'DWD'),
('00005', 'Suresh', '1856423579', 'suri@gmail.com', '555555', 'CABHYD00005', 5383, 'CAB', 'HYD'),
('00001', 'Ayushmaan_1', '01234789', 'NA', '1234', 'SBIRJY00001', 4500, 'SBI', 'RJY'),
('00002', 'Ayushmaan_2', '01234789', 'someone@gmail.com', '123123', 'SBIHYD00001', 2202, 'SBI', 'HYD'),
('00006', 'Ayushmaan', '9848156327', 'Stranger@gmail.com', '000000', 'AXBBMB00006', 50000, 'AXB', 'BMB'),
('00003', 'Manikanta', '8681625648', 'ksn@gmail.com', '33333', 'BOBBMB00003', 2050, 'BOB', 'BMB');

INSERT INTO TRANSACTIONS (trans_id, sender_id, reciever_id, dte, time, amount)
VALUES
('00001125532110202300002', '00001', '00002', '2023-10-21', '12:05:53.519679', 150),
('000011433252110202300002', '00001', '00002', '2023-10-21', '14:33:25.689732', 500),
('000011433542110202300002', '00001', '00002', '2023-10-21', '14:33:54.709375', 500);

INSERT INTO LOAN (loan_id, cust_id, amount, emi, deadline)
VALUES
('SBI00002', '00002', 1200, 100, '2024-10-21 00:00:00'),
('AXB00006', '00006', 50000, 208, '2043-10-17 00:00:00');

