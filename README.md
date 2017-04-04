1) Program description 

src.py is a Python program that runs with standard modules (there is no need to download any additional modules). The program:\n 
(1) Lists the top 10 most active hosts/PI addresses that have accessed the site. 
(2) Identifies the 10 resources that consume the most bandwith on the site. 
(3) Lists the top 10 busiest (or most requently visited) 60-minute periods. 
(4) Detects patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes and logs those further attempts.

2) Input files 

The program reads in a ".txt" file that has the following information: 
(1) Host/IP address. 
(2) Timestamp in the format [DD/MON/YYYY:HH:MM:SS Z], where DD is the day of the month, MON is the abbreviated name of the month, YYYY is the year, HH:MM:SS is the time of day using a 24-hour clock. Z is the timezone (the program is time- zone aware) 
(3) Request given in quotes. 
(4) HTTP reply code. 
(5) Bytes in the reply. A reply listed as "-" is counted as 0 bytes.

3) Output files

The program generates 4 outputs: 
(1) The top 10 most active hosts/IP addresses are printed in descending order to a file named "hosts.txt". The number of times they accessed any part of the site is printed next to the host/IP address. The program is capable of reading host/IP addresses with special chacarcters in them such as _, @, #, ^, &, *, (, ), %, +, /, \\, and ?. 
(2) The top 10 resources on the site that consume the most bandwidth are printed in descending order to a file named "resources.txt". 
(3) The 10 busiest 60-minute period are printed in descending order to a file named "hours.txt". The number of times the site was accessed during those 60 minutes are printed next to the hour where the 60-minute period starts. 
(4) The attempts to enter the site from the same host/IP address after 3 failed attempts (HTTP reply code of 401) to login (all three attempts within a 20 seconds window) are written to a file named "blocked.txt". This attempts will be shown for the next 5 minutes after the 3rd failed attempt to login.

4) Running the program 

scr.py only needs the input file to run. Blank lines in the input file will be ignored. All lines in the input file that deviate from the information described in (2) will be ignored but will be printed to the "errors.txt" output file to analyze separately. 
