import sys
from sys import argv
from os.path import exists
import time





def cleanName(name):
	name = name.strip()
	name = name.strip('\/@#$%^&*()\'.,-_')
	#tokenise with @.. remove domain name
	name = name.split('@')[0]
	name = name.split('/')[0]
	name = name.replace('<','')
	name = name.replace('>','')
	name = name.replace('*','')
	name = name.replace('(','')
	name = name.replace(')','')
	name = name.replace('\'','')	
	name = name.replace('.',' ')
	name = name.replace('-',' ')
	name = name.replace('_',' ')
	name = name.strip()
	name = name.lower()
	return name
	
			
	
#email threshold for graph
EMAIL_THRESHOLD	= 2000
#load the file
#script, data_file_path = argv
data_file_path = "C:\Users\snadaraj\Documents\BNP1\enron-event-history-all.csv"
if not exists(data_file_path) :
	print "File not found!",data_file_path
	sys.exit(0)

emaildict = {}
f = open(data_file_path, 'r')
for line in f.readlines(): 
	line = line.strip()
	line = line.replace('"','') 
	#print line 
	tokens = line.split(',')
	if len(tokens) == 6:
		#print tokens
		#for sender
		sender = cleanName(tokens[2])
		if sender in emaildict:
			emaildict[sender][0] += 1	
		else:
			emaildict[sender] = [1,0]
		
		#for receiver
		for receiver in tokens[3].split('|'):
			receiver = cleanName(receiver)
			#print receiver
			if  receiver in emaildict:
				emaildict[receiver][1] += 1
			else:
				emaildict[receiver] = [0,1]		

f.close()

#print dict
#print emaildict
#sort the dict according to no of email send
#write the results back
output_file = "output.csv"
outf = open(output_file,'w')

important_senders = []

for key, value in sorted(emaildict.iteritems(), key=lambda (k,v): (v,k)):
	outf.write("%s,%d,%d\n" % (key,value[0],value[1]))
	if value[0] > EMAIL_THRESHOLD :
		important_senders.append(key)

#question 2

#import matplotlib.pyplot as plt
#import numpy as np
#import pandas as pd

#crete 2 d data frame to store the number of emails per month accross important users
data_range = {}
start_yyyymm = "1998-01"
end_yyyymm = "2002-12"
for year in range(1998,2002):
	for month in range(1,12):
		yyyy_mm = "%d-%02d" % (year,month)
		data_range[yyyy_mm] = 0
		
emailsPerMonth = {}
for sender in important_senders:
	emailsPerMonth[sender] = data_range

f1 = open(data_file_path, 'r')
for line in f1.readlines(): 
	line = line.strip()
	line = line.replace('"','') 
	tokens = line.split(',')
	if len(tokens) == 6:
		#print tokens
		#for sender
		sender = cleanName(tokens[2])
		if sender in important_senders:
			yyyymm = time.strftime('%Y-%m',time.localtime(float(tokens[0])/1000))
			if sender in emailsPerMonth:
				if yyyymm in emailsPerMonth[sender]:
					emailsPerMonth[sender][yyyymm] += 1	

#print emailsPerMonth		
			
import matplotlib.pyplot as plt
x= data_range.keys().sorted()

for sender in important_senders:
	value_list = []
	for key in sorted(emailsPerMonth[sender].keys()):
		value_list.append(emailsPerMonth[sender][key])
		
	plt.plot(x,(emailsPerMonth[sender].sorted()).values())

plt.show()



	