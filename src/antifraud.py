#!python3
#! antifraud.py - A program that prevents fraudulent payment requests from untrusted users

import re

# Read in previous transactions.
previous_transactions = {}
re_groups = re.compile(r'''
        ((\d+)              #year
       	(-|/)               #separator
	(\d+)               #month
	(-|/)               #separator
	(\d+)               #day
	(\s*)               #space
	(\d+)               #hour
	(:)                 #separator
	(\d+)               #minute
	(:)?                #separator
	(\d+)?              #seconds
	(,)                 #comma
	(\s*)               #space
	([0-9]+)            #id1
	(,)                 #comma
	(\s*)               #space
	([0-9]+)            #id2
	)''',re.VERBOSE)
with open('batch_payment.csv','r',encoding='utf-8') as myfile:
    for line in myfile:
        #Look for regular expresson M/D/Y H:M(:S), id1, id2.
        mo = re_groups.findall(line)
        try:
            #Generate transaction directory (If A makes a transaction with B,
            #then B has a transaction with A.
            try:
                if mo[0][17] not in previous_transactions[mo[0][14]]:
                    previous_transactions[mo[0][14]].append(mo[0][17])
            except KeyError:
                previous_transactions[mo[0][14]] = list()
                previous_transactions[mo[0][14]].append(mo[0][17])
            try:
                if mo[0][14] not in previous_transactions[mo[0][17]]:
                    previous_transactions[mo[0][17]].append(mo[0][14])
            except KeyError:
                previous_transactions[mo[0][17]] = list()
                previous_transactions[mo[0][17]].append(mo[0][14])
        except IndexError:
            continue
myfile.close()
previous_transactions2 = previous_transactions
previous_transactions3 = previous_transactions
# Read in new transactions (each line corresponds to a new sequential transaction).
# The program does not update the "1st degree" friends list. To update, just uncomment the lines 
# marked as "#" bellow.
feature1file = open('output1.txt','w')
feature2file = open('output2.txt','w')
feature3file = open('output3.txt','w')
with open('stream_payment.csv','r',encoding='utf-8') as myfile:
    for line in myfile:
        #Look for regular expresson M/D/Y H:M(:S), id1, id2.
        mo = re_groups.findall(line)
        status1 = 'unverified'
        status2 = 'unverified'
        status3 = 'unverified'
        skip = False
        if mo != []:
            #Check if any of the users is new. If so, mark 'unverified' and add it to the dictionary for future transaction.
            if mo[0][14] not in previous_transactions.keys():
                skip = True
                feature1file.write(status1+'\n')
                feature2file.write(status2+'\n')
                feature3file.write(status3+'\n')
            if mo[0][17] not in previous_transactions.keys():
                skip = True
                feature1file.write(status1+'\n')
                feature2file.write(status2+'\n')
                feature3file.write(status3+'\n')
            if skip == False:
                #Feature 1: When anyone makes a payment to another user, they'll be notified if they've never made a transaction with that user before.    
                if mo[0][17] in previous_transactions[mo[0][14]]:
                    status1 = 'trusted'
                #print output1.txt
                feature1file.write(status1+'\n')
                if mo[0][17] in previous_transactions2[mo[0][14]]:
                    status2 = 'trusted'
                if mo[0][17] in previous_transactions3[mo[0][14]]:
                    status3 = 'trusted'
                #Feature 2: User A and User B should be able to pay each other without triggering a warning notification since they're "2nd degree" friends
                status2 = status1
                if status2 == 'unverified':
                    for i in previous_transactions2[mo[0][14]]:
                        for j in previous_transactions2[mo[0][17]]:
                            if i==j:
                                status2 = 'trusted'
                                previous_transactions2[mo[0][17]].append(mo[0][14])
                                previous_transactions2[mo[0][14]].append(mo[0][17])
                                break
                        if status2 == 'trusted':
                            break
                #print output2.txt
                feature2file.write(status2+'\n')
                #Feature 3
                #Implement a feature to warn users only when they're outside the "4th degree friends network"
                status3 = status2
                if status3 == 'unverified':
                    for i in previous_transactions3[mo[0][14]]:
                        if mo[0][17] in previous_transactions3[i]:
                            status3 = 'trusted'
                            previous_transactions3[mo[0][17]].append(mo[0][14])
                            previous_transactions3[mo[0][14]].append(mo[0][17])
                            break
                        for j in previous_transactions3[i]:
                            if mo[0][17] in previous_transactions3[j]:
                                status3 = 'trusted'
                                previous_transactions3[mo[0][17]].append(mo[0][14])
                                previous_transactions3[mo[0][14]].append(mo[0][17])
                                break
                            else:
                                for k in previous_transactions3[j]:
                                    if mo[0][17] in previous_transactions3[k]:
                                        status3='trusted'
                                        previous_transactions3[mo[0][17]].append(mo[0][14])
                                        previous_transactions3[mo[0][14]].append(mo[0][17])
                                        break
                            if status3 == 'trusted':
                                break
                        if status3 == 'trusted':
                            break
                # print output3.txt
                feature3file.write(status3+'\n')        
myfile.close()                   
feature1file.close()                    
feature2file.close()
feature3file.close() 
