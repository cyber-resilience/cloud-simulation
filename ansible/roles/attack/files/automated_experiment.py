import subprocess
import time
import numpy as np
import random

#set total time for experiment
t = 900
num_attacks = 1

#select attack to be used
attack = np.random.random_integers(1,5,size=(num_attacks))

#select IPs to attack
#list of potential IPs to target
#read /etc/hosts file to get IPs
IPs = np.loadtxt('/etc/hosts', dtype=str, delimiter = ' ', skiprows=2, usecols=0)
#IPs = ['web','db','nfs','genfile','ingest','getfile']
#get number of IPs to target
num_IPs = np.random.random_integers(len(IPs))
victim_idx = np.random.random_integers(len(IPs), size=(num_IPs))
print len(IPs), victim_idx
victims = [IPs[i-1] for i in victim_idx]

#for each IP select an account to target and compile victims.txt
acct_dict = {'sally':'WhatIsThePa55word1', 'cleo':'WhatIsThePa55word2', 'devin':'WhatIsThePa55word3', 'adam':'WhatIsThePa55word4', 'darryl':'WhatIsThePa55word5'}
victims_out = [','.join((ip,)+random.sample(acct_dict.items(),1)[0]) for ip in victims]
np.savetxt('victims.txt', victims_out, delimiter='\n', fmt = '%s')

#launch attacks at random time intervals
#start with 5 minutes of regular traffic
times = [t]
time.sleep(3)
t -= 300
times.append(t)
while t > 0:
    wait = np.random.randint(20)
    time.sleep(wait)
	a = np.random.choice(attack)
    proc = subprocess.Popen(['python', 'attacksim3.py', str(a), str(6)])
    t -= wait
    times.append(t)

#prepare output file with details of attack
output = []
output.append('Selected attack: {}'.format(attack))
output.append('Total time: {}'.format(times[0]))
output.append('Normal traffic: {}'.format(times[0] - times[1]))
n = 1
for i in times[2:]:
    output.append('Attack {0}: {1}'.format(n, times[0] - i))
    n += 1

x = time.localtime()
outfile = 'experiment_output_{0}.{1}.{2}_{3}.{4}.txt'.format(x[1], x[2], x[0], x[3], x[4])
np.savetxt(outfile, output, delimiter='\n', fmt='%s')
np.savetxt('victims_{0}.{1}.{2}_{3}.{4}.txt'.format(x[1], x[2], x[0], x[3], x[4]), victims_out, delimiter='\n', fmt='%s')
