## DNS SPOOFER
**Installation**:
pip3 install -r requirements.txt     ***# Make Sure all packages are installed successfully***
#


**Usage**:
**root@kali~#** python3 dns_spoofer.py -h  **# For usage help**

**root@kali~#** python3 dns_spoofer.py -r "**your server ip or ip to which redirect**" -w "**website to be spoofed or leave empty to spoof all**"
 
 To run attack locally (for your own system not in Network) **comment** out line 65
 
 os.system("iptables -I FORWARD -j NFQUEUE --queue-num 123")
 
and **Uncomment** line 67 and 68

**os.system("iptables -I INPUT -j NFQUEUE --queue-num 123")  
 os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 123")**

**NOTE :**
Running script in local network make sure to run arpspoof against the target so that you can intercept the traffic from target PC
