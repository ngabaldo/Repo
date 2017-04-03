#!/bin/bash
#Executing the program with the input directory log_input and ouput the fiels in the directory log_output
python ./src/process_log.py ./log_input/log.txt ./log_output/hosts.txt ./log_output/hours.txt ./log_output/resources.txt ./log_output/blocked.txt
