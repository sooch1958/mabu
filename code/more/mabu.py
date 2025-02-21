"""

Control the Catalia Mabu health care support robot head.


Written by Josef Szuecs
February 14, 2025

"""

from machine import Pin,UART
import time


uart = 0
    

def initialize():

    global uart

    uart = UART(1, 57600)                         # init with given baudrate
    uart.init(57600, bits=8, parity=None, stop=1) # init with given parameters
    

# the head controller sends back responses to the tablet. Just read and ignore.
def clear_RX_data():
    
    d = uart.read()
    

def send_command(data, delay=0.0):

    clear_RX_data()

    uart.write(bytearray(data))
    
    time.sleep(delay)
    

# read the command file and send each line to the head.
def run_commands(fname, label='test', delay=0.1):
    
    count = 1
        
    with open(fname, 'r') as f:
        for line in f:
            # Evaluate the line as a Python list
            a = eval(line)
            l = len(a)
            info = a[-2:]
            cmd = a[:-2]
            count = count + 1
            send_command(cmd, delay)
            
            
# read the command file and and put it in a list.
def load_commands(fname, label='test'):

    count = 1
    cmds = []

    with open(fname, 'r') as f:
        for line in f:
            # Evaluate the line as a Python list
            a = eval(line)
            l = len(a)
            info = a[-2:]
            cmd = a[:-2]
            count = count + 1            
            cmds.append(cmd)
            
        f.close()

    return cmds


# take a slice out of the list of commands based on the start/stop values
# (values are from 0 to 180)
# then assign timestamps to the list of movements
def action(fname, start, stop, speed, offset):
    
    a = []
    c = load_commands(fname)
    l = len(s) 

    adj_start = int((start/180) * l);
    adj_stop = int((stop/180) * l);

    # print(f"start: {adj_start} stop: {adj_stop}")

    for i in range(adj_start, adj_stop):
       a.append(c[i])

    print(len(a))

    timestamp_action(a, offset, speed)

    return a


# simple move from start to stop angle
# c = the ordered list of motion commands
def move(c, start, stop, delay=0.2):
    
    a = []
    l = len(c) 

    adj_start = int((start/180) * l);
    adj_stop = int((stop/180) * l);
    
    if adj_start < 1:
        adj_start = 1
    elif adj_start >= len(c):
        adj_start = len(c)-1

    if adj_stop < 1:
        adj_stop = 1
    elif adj_stop >= len(c):
        adj_stop = len(c)-1

    # print(f"move start: {adj_start} stop: {adj_stop}")
    
    send_command(c[adj_start], delay)
    send_command(c[adj_stop], delay)


# put timestamps into the list of movement commands
def timestamp_action(action, time_offset, time_tic):
  
    count = 0
    elapsed_time = time_offset

    for a in action:
        a.insert(0, elapsed_time)
        elapsed_time += time_tic 
         
    return count


# cycle through the list of actions and send commands to head
# based on execution times
def perform_script(seq):

    posns = [0] * len(seq) # keep track of each sequence current position
    end_count = 0
    
    start = time.time_ns()

    while True: # step through timed actions

        now = (time.time_ns() - start) / 1000000000
        
        end_count = 0
        for i, a in enumerate(seq): # check the next action in each sequence to see if time to send
            if (posns[i] < (len(a)-1)):  # not at the end of the movement
                if (now > a[posns[i]][0]):  # time to send command to head
                    send_command(a[posns[i]][1:])
                    posns[i] += 1
            else:
                end_count += 1  # count number of finished movements

        if (end_count >= len(seq)):  # if all movements done, exit
            print('done')
            break
        
