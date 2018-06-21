#!/usr/bin/env python3.5
# Made by Constantine
# vi127001@gmail.com

import urllib.request
import socket
import os
import sys
import time

socket.setdefaulttimeout(5)

def iploader():
    with open('kgnets.txt') as kgnets:
        ip_array = kgnets.readlines()
    return ip_array

def getter():
    try:
        if os.path.isfile('kgnets.txt') == True:
            os.remove('kgnets.txt')
        urllib.request.urlretrieve('http://ip.elcat.kg/kg-nets.txt', 'kgnets.txt')
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        status='error'
    except urllib.error.URLError as e:
        print('Reason: ', e.reason)
        status='error'
    else:
        status='ok'
    return status


if __name__ == '__main__':
    if getter() == 'ok':
        ips = iploader()
        if os.path.isfile('iptables-rules-for-install') == True:
            os.remove('iptables-rules-for-install')
        with open('iptables-rules-for-install', 'w') as f:
            f.write('# Generated by ipkg on '+time.ctime()+'\n')
            f.write('*filter\n')
            f.write(':INPUT ACCEPT [113:7852]\n')
            f.write(':FORWARD ACCEPT [0:0]\n')
            f.write(':OUTPUT ACCEPT [75:6544]\n')
            for x in ips:
                f.write('-A INPUT -s '+x.rstrip()+' -p tcp -m tcp --dport 80 -j ACCEPT\n')
                f.write('-A INPUT -s '+x.rstrip()+' -p tcp -m tcp --dport 443 -j ACCEPT\n')
            f.write('-A INPUT -s 10.0.1.0/24 -p tcp -m tcp --dport 80 -j ACCEPT\n') # Allow some additional network
            f.write('-A INPUT -s 172.16.80.0/24 -p tcp -m tcp --dport 443 -j ACCEPT\n') # Allow some additional network
            f.write('-A INPUT -p tcp -m tcp --dport 80 -j DROP\n')
            f.write('-A INPUT -p tcp -m tcp --dport 443 -j DROP\n') 
            f.write('COMMIT\n')
            f.write('# Completed on '+time.ctime()+'\n')
        f.close()
        os.system("iptables-restore "+"<"+" iptables-rules-for-install")
        os.system("netfilter-persistent "+"save")
    else:
        sys.exit(1)
