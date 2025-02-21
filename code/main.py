"""

Control the Catalia Mabu health care support robot head.

Written by Josef Szuecs
January 31, 2025

"""
from machine import Pin,UART
import time
import random

DEBUG = True

uart = UART(1, 57600)                         # init with given baudrate
uart.init(57600, bits=8, parity=None, stop=1) # init with given parameters

# the head controller sends back responses to the tablet. Just read and ignore.
def clear_RX_data():
    
    d = uart.read()
    

def send_command(data):

    clear_RX_data()

    uart.write(bytearray(data))
    

# read the command file and send each line to the head.
def run_script(fname, label='test'):
    
    count = 1
    
    if DEBUG:
        print("running: ", label)
    
    with open(fname, 'r') as f:
        for line in f:
            # Evaluate the line as a Python list
            a = eval(line)
            l = len(a)
            info = a[-2:]
            cmd = a[:-2]
            if DEBUG:
                print(f"{count}: {cmd} : {info[0]}")
            count = count + 1
            send_command(cmd)
            time.sleep(int(info[1]))
                                
def main():
    
    while True:
    
        run_script("movements.txt")
    
        time.sleep(5)
            
if __name__ == "__main__":
    main()
    
    
