# rDNS-ng
A reverse dns lookup tool for a range of given IP's or a whole subnet.

Note : Runs only on Python3.x ... No support for Python2!

# Installation
pip install -r requirements.txt
(or)
pip install netaddr
pip install colorama

# Usage
usage: `rDNS.py [-h] [-ir IP Range] [-is Subnet] [-f Output file]`

optional arguments:

    -h, --help      ----> show this help message and exit
    -ir IP Range    ----> eg: 192.168.0.1-192.168.2.0
    -is Subnet      ----> eg: 192.168.0.1/24
    -f Output file  ----> write output to a file

![alt text](https://github.com/harshil-shah004/rDNS-ng/blob/master/sample.png)
