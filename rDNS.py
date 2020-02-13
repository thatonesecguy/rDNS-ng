import subprocess
import signal
import sys
import re
import socket 
from netaddr import *
import netaddr
import argparse
from colorama import Fore
from colorama import Style

def banner():
    with open('banner.txt', 'r',encoding = "utf8") as f:
        data = f.read()

        print(f'{Fore.GREEN}%s{Style.RESET_ALL}' % data)
        print("Providing you with Reveese DNS on subnets, IP ranges and IP lists")
        print("Author : Harshil Shah (@harshil-shah004)")

banner()

parser = argparse.ArgumentParser()
parser.add_argument("-il", dest = "file_input", 
                    help = "eg: ip_list.txt", metavar="File Input")
parser.add_argument("-ir", dest="ip_ranges",
                    help = "eg: 192.168.0.1-192.168.2.0", metavar="Ip Range")
parser.add_argument("-is", dest="subnet",
                    help = "eg: 192.168.0.1/24", metavar="Subnet")
parser.add_argument("-f", dest="save_file",
                    help= "write output to a file",metavar="Output File")





if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()


save_flag = False
f = ''
total = 0
found_count = 0
not_found_count = 0
not_found = 0
found = 0






def sig_handler(signum,frm):
    print("\n\n[+] Keyboard Interrupt occured.")
    if save_flag:
        stats()
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

def stats():
    global total
    global not_found
    global found
    save_file = args.save_file
    total_count = "\nTotal IP : %d" %total
    found = "\n Found : %d" %found_count
    not_found = "\n Not Found : %d" %not_found
    print(total_count)
    print(found)
    print(not_found)
    if save_flag:
        f.write(total_count+"\n"+found+"\n"+not_found)
        f.close()
        print("[+]Output file saved.")
        # f.write(total_count+"\n"+found+"\n"+not_found)
		# f.close()
		# print("[+]Output file saved.")

def save_output():
	if args.save_file:
		save_file = args.save_file
		global f
		f = open(save_file,'w')
		global save_flag
		save_flag = True

def iterate_ip_ranges(first_range,last_range):

	try:
		ip_range = IPSet(IPRange(first_range, last_range))
		if (ip_range.iscontiguous() == True):
			# print("\n[+] There are total %s IP's in the given range.\n") %str(len(ip_range))
			save_output()
			global total
			total = len(ip_range)
			for ip in ip_range:
				resolve_ptr(ip)
			stats()
		else:
			print("Error: IP range is not continuous!\n")
			sys.exit(0)
	 
	except netaddr.core.AddrFormatError:
		print("\nError: Lower bound IP greater than upper bound!")
		print("Try again.")

def iterate_ip_subnet(subnet):
	try:
		ip_range = IPNetwork(subnet)
		# print("\n[+] There are total %s IP's in the given subnet.\n") %str(len(ip_range))
		save_output()
		global total
		total = len(ip_range)
		for ip in ip_range:
			resolve_ptr(ip)
		stats()
	except netaddr.core.AddrFormatError:
		print("\nError: Invalid IP Network entered.")
		print("Try again.")
		parser.print_help()
		sys.exit(0)

def resolve_ptr(ip):
	cmd = "host %s 8.8.8.8" %ip
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
	
	match_found = re.search('name pointer'.encode(),p)
	match_not_found = re.search('not found'.encode(),p)
	connection_timed_out = re.search('connection timed out'.encode(),p)
	global found_count, not_found_count, connection_timed_out_count
	if match_found:
		output = "%s  %s" %(ip,p.strip('\n').split(' ')[-1])
		print(output)
		found_count+=1
		if save_flag:
			f.write(output+"\n")
		
	elif match_not_found:
		not_found_count+=1
		# print ip+" - Not found!"
		# if save_flag:
		# 	f.write(ip+" - Not found!"+"\n")
		pass

	elif connection_timed_out:
		output= "%s: Connection Timed out! No servers could be reached." %ip
		not_found_count+=1
		print(output)
		if save_flag:
			f.write(output+"\n")
	
	else:
		print("Can't resolve.") 

if args.ip_ranges:
	first_range = args.ip_ranges.split('-')[0]
	last_range = args.ip_ranges.split('-')[-1]
	try:
	    socket.inet_aton(str(first_range))
	    socket.inet_aton(str(last_range))
	    iterate_ip_ranges(first_range,last_range)
	    
	except socket.error:
	    print("\n[*] Error: Incorrect IP Range entered\n")
	    parser.print_help()
	    sys.exit(0)

if args.subnet:
	subnet = str(args.subnet)
	iterate_ip_subnet(subnet)

if args.file_input:
	file = open(args.file_input,'r').readlines()
	save_output()
	for ip in file:
		ip = ip.strip('\n')
		resolve_ptr(ip)
		total+=1
	stats()
