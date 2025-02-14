"""

Control the Catalia Mabu health care support robot head.

Written by Josef Szuecs
January 31, 2025

"""

import time
import random
import sys
from machine import Pin, ADC

from mabu import *

# store the commands and number of commands for each motor
commands = []
cmd_lens = []

EYES_LR = 0
EYES_UD = 1
EYELID_LEFT = 2
EYELID_RIGHT = 3
NECK_UD = 4
NECK_LR = 5
NECK_ROT = 6


def start_timer():
    
    global duration_start
    
    duration_start = time.time_ns()

    
def end_timer():
    
    global duration_start
    
    delta = (time.time_ns() - duration_start) / 1000000

    print(f"elapsed_time: {delta}ms")


def send_start_command():
    
    # This must be sent before trying to move the head using the commands
    # in the files.
    
    send_command([250, 0, 2, 79, 127, 11, 203, 250, 0, 1, 71, 53, 67])
    time.sleep(0.5)
    
        
def sequence_test():
    
    # sequence: start_time, data file, start, stop, time_step

    sequence = []
    
    sequence.append(action("ldls.txt", 5, 90, 0.25, 3.0))
    sequence.append(action("ldrs.txt", 5, 90, 0.1, 1.5))
    sequence.append(action("elrs.txt", 5, 170, 0.1, 0.5))
    sequence.append(action("euds.txt", 5, 170, 0.1, 1.5))

    perform_script(sequence)


def load_command_info():
    
    # Load head movement commands into memory for all of the motors.\
    # Memory is limited on the Pico, so these files are subsets of the
    # full motion command set.
    #
    # There are three sets of files. Full movement set, shortened movement set
    # and extra-shortened movement set. The naming is as such:
    #
    #  elrs.txt = full set
    #  elrs_t.txt = shortened set
    #  elrs_tt.txt = extra short set
    
    global commands
    global cmd_lens
    
    commands.append(load_commands("elrs_tt.txt", 'rando'))
    commands.append(load_commands("euds_tt.txt", 'rando'))
    commands.append(load_commands("ldls_tt.txt", 'rando'))
    commands.append(load_commands("ldrs_tt.txt", 'rando'))
    commands.append(load_commands("nts_tt.txt", 'rando'))
    commands.append(load_commands("nes_tt.txt", 'rando'))
    commands.append(load_commands("nrs_tt.txt", 'rando'))
    
    for c in range(0, len(commands)):
        cmd_lens.append(len(commands[c]))


def move_part(id, start, stop, delay=0.2):
    
    move(commands[id], start, stop, delay)
    
    
def rando():
    
    # Randomly move the head around.
    
    global commands
    global cmd_lens
    
    print(cmd_lens)
        
    while True:

        for i in range(len(commands)):
            send_command(commands[i][random.randint(0, cmd_lens[i])-1], 0.2)
            

def joystick_control():
    
    # Control the head using an inexpensive 5 pin joystick controller.
    #
    # joystick : RPI Pico
    # GND : GND
    # +5V : 3V3
    # VRx : GPIO27
    # VRy : GPIO26
    # SW  : GPIO16
    #
    # Controls two motors at a time. Pressing the knob down changes the motor pair.
    
    xAxis = ADC(Pin(27))
    yAxis = ADC(Pin(26))
    button = Pin(16,Pin.IN, Pin.PULL_UP)
    
    mode = 0

    lr = EYES_LR
    ud = EYES_UD
        
    while True:
        
        xValue = xAxis.read_u16()
        yValue = yAxis.read_u16()
        buttonValue = button.value()
                
        xStatus = "middle"
        yStatus = "middle"
        buttonStatus = "not pressed"
        
        if xValue <= 600:
            xStatus = "left"
        elif xValue >= 60000:
            xStatus = "right"
        if yValue <= 600:
            yStatus = "up"
        elif yValue >= 60000:
            yStatus = "down"
        if buttonValue == 0:
            buttonStatus = "pressed"
            time.sleep(0.2)
            
        if buttonStatus == "pressed":
            for p in range(0, 6):
                move_part(p, 0, 0, 0)

            mode += 1
            mode = mode % 3
            
            if mode == 0:
                lr = EYELID_LEFT
                ud = EYELID_RIGHT
            elif mode == 1:
                lr = NECK_LR
                ud = NECK_UD
            elif mode == 2:
                lr = EYES_LR
                ud = EYES_UD
                            
        if xStatus == "middle":
            move_part(lr, 90, 90, 0)
        elif xStatus == "left":
            move_part(lr, 0, 0, 0)
        else:
            move_part(lr, 180, 180, 0)
            
        if yStatus == "middle":
            move_part(ud, 90, 90, 0)
        elif yStatus == "up":
            move_part(ud, 0, 0, 0)
        else:
            move_part(ud, 180, 180, 0)
                

def main():
    
    initialize() # set up the UART
    
    load_command_info() # pre-load commands for all motors into memory

    send_start_command() # put the head into the proper state to accept commands
   
    # kinda get the head centered
    move_part(EYELID_LEFT, 180, 0)
    move_part(EYELID_RIGHT, 180, 0)
    move_part(NECK_ROT, 90, 90)
    
    # joystick_control() # uncomment to play around with a joystick
    
    move_part(EYELID_LEFT, 45, 135)
    move_part(EYELID_RIGHT, 45, 135)
    move_part
    run_commands("ldrs.txt", "test", 0.01) # stream the contents of a movement file to the head
    
    rando() # jerk the head around randomly
    
    move_part(EYELID_LEFT, 180, 0)
    move_part(EYELID_RIGHT, 180, 0)
    move_part(NECK_ROT, 90, 90)
    
    
if __name__ == "__main__":
    main()
    
