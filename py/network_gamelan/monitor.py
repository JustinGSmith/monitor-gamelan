# TODO - note python-osc is installed to my ~/py-local/
# so start python as ~/bin/python3
import re
from pythonosc import udp_client

def is_unresolved(domain_parts):
    for part in domain_parts:
        if(not(re.match('[0-9]+', part))):
            return False
    return True

def process_domain(foreign_address):
    domain = foreign_address.split(':')
    parts = domain[0].split('.')
    if(len(parts) > 1):
        if(is_unresolved(parts)):
            return foreign_address
        else:
            domain_part = parts[-2]
            return domain_part
    else:
        return foreign_address

def process_line(line):
    parsed = line.split()
    foreign_address = parsed[4]
    foreign_domain = process_domain(foreign_address)
    print(parsed, foreign_domain, '\n')

def main():
    running = True
    lines = 0
    client = udp_client.SimpleUDPClient("127.0.0.1", 2666)
    while (running):
        try:
            # receiving socket events from STDIN
            connection_info = process_line(input())
            # TODO some magic goes here
            # use above connection_info info to construct this message
            client.send_message("/event/", 1)
        except EOFError:
            running = False
        lines = lines + 1

main()
