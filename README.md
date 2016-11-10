1) Program description
antifraud.py is a Python program that detects fraudulent payment requests from untrusted users
when UserA makes a money transaction to UserB. The program runs with standard modules (there is 
no need to download any additional modules).

antifraud.py detects 'trusted' and 'unverified' transactions between UserA and UserB. When a 
transaction is marked as 'trusted', the history of transactions between UserA and UserB is
updated (see (3) Output files to see how 'trusted' transactions are defined). Each feature history 
is updated independently of the other features, so updating for Feature 3 does not affect the result 
of Output1.txt if the user only wants to implement Feature 1.

Lines that are entered incorrectly as input data will not be taken into account in the output file
(i.e. "Some line of text" that is entered instead of the date, time, userA, userB, amount, and message
will be skipped by the program).



2) Input files:
The program reads in .txt files that have the following information: date and time, id1, id2, amount,
optional message. These values must be separated by a comma. id1 refers to UserA and id2 refers to UserB. 
Only two files are needed:

  a) batch_payment.txt
  Contains information about the previous transaction history of all users.
  
  b)stream_payment.txt
  Contains information about new transaction requests. Every line of stream_payment.txt is 
  considered to be a new ral-time transaction. 
  
  
  
3) Output files:
The program generates 3 outputs:

  a) output1.txt:
  This output is generated for Feature 1. The user will be notified if he tries to make a payment 
  to another user when they have not had any transaction between them before.

  b) output2.txt:
  This output is generated for Feature 2. The user will be notified if he tries to make a payment to 
  another user when they have not had any transaction between them before, unless they have had a 
  transaction with someone in common ("2nd degree friends").

  c) output3.txt:
  This output is generated for Feature 3. The user will be notified if he tries to make a payment to 
  another user when they have not had any transaction between them before, unless the second user is 
  inside a "4th degree friend circle".



4) Running the program
run.sh is the shell script used to run the programs. It must be placed on the folder containing paymo_input, 
paymo_output, and src. The shell script moves into the paymo_output folder and it copies antifraud.py, 
batch_payment.txt, and stream_payment.txt. This way the program does not have to move between folders to run. 
run.sh deletes the copied files at the end, so only output1.txt, output2.txt, and output3.txt are left inside 
the paymo_output folder.


