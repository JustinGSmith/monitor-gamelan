from pythonosc import udp_client

def find_match_and_execute(data, monitors):
    for monitor in monitors:
        parsed = monitor.accept(data)
        if (parsed):
            return monitor.consume(parsed)
    return False

# connects to osc server at server, checks data against monitors

# monitors should be a list of objects with accept() and consume() methods

# data_source should be a thunk (function of no arguments) returning False
# to indicate end of execution, or a result consumable by each monitor's
# accept() method

# each monitor's consume() method should be able to use the result of its
# accept() method to produce an OSC message line (list of strings and numbers)
def monitor(server, data_source, monitors):
    running = True
    client = udp_client.SimpleUDPClient(*server)
    while (running):
            data = data_source()
            if (not data):
                running = False
            else:
                result = find_match_and_execute(data, monitors)
                if (result):
                    client.send_message(*result)
