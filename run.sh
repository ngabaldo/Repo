#!/bin/bash
cd paymo_output
cp ../src/antifraud.py .
cp ../paymo_input/batch_payment.txt .
cp ../paymo_input/stream_payment.txt .
./antifraud.py
rm batch_payment.txt
rm stream_payment.txt
rm antifraud.py
