
1) Program description
Antifraud.py is a Python program that detects fraudulent payment requests from untrusted users
when A makes a money transaction to B.
Antifraud.py runs with standard moudles (there is no need to download any additoinal modules).


2) Input files:
Only two files are needed:

  a) batch_payment.csv
  Contains information about the previous transaction history of all users.
  
  b)stream_payment.csv
  Contains information about new transaction requests. Every line of stream_payment.csv is 
  considered to be a new transaction. If A makes a new transaction to B, he will be notified. 
  If A makes another transaction to B, there will be no new notifications.
  
  
3) Output files:
The program generates 3 outputs:

  a) output1.txt:
  The user will be notified if he tries to make a payment to another user when they have not 
  had any transaction between them before.

  b) output2.txt:
  The user will be notified if he tries to make a payment to another user when they have not
  had any transaction between them before, unless they have had a transaction with someone
  in common ("2nd degree friends").

  c) output3.txt:
  The user will be notified if he tries to make a payment to another user when they have not 
  had any transaction between them before, unless the second user is inside a "4th degree
  friend circle".

