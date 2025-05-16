import re
from pythonosc import udp_client

# hash map from domains to numbers
domains = {}
domain_count = 0
def map_domain(foreign):
    global domains, domain_count
    # eventually (maybe?) params too
    val = domains.get(foreign, False)
    if (val):
        return val
    else:
        domains[foreign] = domain_count
        val = domain_count
        domain_count = domain_count+1
        return val

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
    foreign_domain = foreign_address # process_domain(foreign_address)
    mapped = map_domain(foreign_domain)
    print(parsed, foreign_domain, mapped, '\n')
    return mapped

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
            client.send_message("/event/", connection_info)
        except EOFError:
            running = False
        lines = lines + 1

main()
