
1) Program description
Antifraud.py is a Python program that detects fraudulent payment requests from untrusted users
when A makes a money transaction to B.
Antifraud.py runs with standard moudles (there is no need to download any additoinal modules).


2) Input files:
The program reads in .csv files. Only two files are needed:

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


4) Running the program
run.sh is the shell script used to run the programs. It must be placed on the folder containing paymo_input, paymo_output, and src.
The shell script has the following form:

#!/bin/bash
#SBATCH --job-name="python"
#SBATCH --output="python.%j.%N.out"
#SBATCH --partition=shared
#SBATCH --share
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --export=ALL
#SBATCH -t 48:00:00
module load python
cd paymo_output
cp ../src/antifraud.py .
cp ../paymo_input/batch_payment.csv .
cp ../paymo_input/stream_payment.csv .
./antifraud.py
rm batch_payment.csv
rm stream_payment.csv
rm antifraud.py

