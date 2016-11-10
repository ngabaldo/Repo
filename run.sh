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
cp ../paymo_input/batch_payment.txt .
cp ../paymo_input/stream_payment.txt .
./antifraud.py
rm batch_payment.txt
rm stream_payment.txt
rm antifraud.py
