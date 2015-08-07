import requests
import subprocess
import sys
import os
import time

url = "https://ec2.amazonaws.com/"
#start nodes
start_params = {'Action':'StartInstances','InstanceId.1':,'AUTHPARAMS':}
start = requests.get(url, params=start_params)

#transfer experiment script to attack node and run
#attack script file name provided via command line
f = sys.argv[1]
user = 'admin'
attack_ip = 'GenFile'
proc1 = subprocess.popen(['scp', f, user+'@'+attack_ip':/home/'+user+'/'])
proc1.communicate()
proc2 = subprocess.popen(['python', f])
proc2.communicate()
#stop nodes
stop_params = {'Action':'StopInstances','InstanceId.1':,'AUTHPARAMS':}
stop = requests.get(url, params=stop_params)
