import re
import gamelan_monitor

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

# currently unused, will be used in more selective monitor definitions
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

# TODO - other monitors with more picky accept criteria
class RemoteHost:
    def accept(self, parsed):
        return parsed

    def consume(self, parsed):
        foreign_domain = parsed[4]
        # print("mapping domain:", foreign_domain, "\n")
        remote = map_domain(foreign_domain)
        return ["/remote/", remote]

def get_line():
    try:
        raw = input()
        line = raw.split()
    except EOFError:
        line = False
    return line

monitors = [RemoteHost()]

gamelan_monitor.monitor(["127.0.0.1", 2666], get_line, monitors)
