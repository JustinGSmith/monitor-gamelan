import os
import socket
running = True
lines = 0


def process_line():
    line = input()
    print("line: " + '"' + line + '"')

def main():
    try:
        while (running and (lines < 20)):
            process_line()
            lines = lines + 1
    except:
        prog = os.getenv("_")
        print(prog + " " + __file__ + " - ERROR - exiting main loop")

main()
