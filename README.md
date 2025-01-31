# mabu
Control code for the Catalia Health Mabu robot

These health care support robots were dumped by the manufacturer around January 2025. They are controlled by a tablet computer that is attached to the front of the little yellow guys.

The tablet communicates to the head via a UART connection.  The head contains a CPU (Holtek HT32F12345) connected to 4 dual motor controllers (TB6612FNG). This drives 7 motors that control head movement.

Since the communication was via UART, I hooked up a cheap USB logic analyser to the port and used Pulseview to capture the commands sent from the tablet to the head. I figured if I parsed them out and sent them to the head controller I would be able to independently control the head. This turned out to be, for the most part, true.

The UART settings: 57400 bps, bits=8, parity=None, stop=1

The code provided here is a small python program that runs on a Raspberry Pi Pico.

There are three wires that connect the head to the tablet. On the head circuit board they are marked as such:

  RED = UTX
  
  WHITE = URX
  
  BLACK =  GROUND


On the RPi Pico:

  RED = GP5
  
  WHITE = GP4[250, 0, 4, 1, 64, 1, 127, 55, 192, 'left eye lid half open', 1]
  
  BLACK = GROUND
  

There is also a power connection to the circuit board in the head. Just leave that connected.

The tablet interface provides access to test and calibration via the "Mabu Factory Mode" icon. By running the various tests and monitoring the UART output I was able to piece together a set of commands to control the head.

The code reads commands from a text file. Here is an example line:

[250, 0, 4, 1, 64, 1, 127, 55, 192, 'left eye lid half open', 1]

Basically a python list. The first set of numbers is the head movement UART bytes. The number of bytes is variable. Then there is a comment string and the last number is a delay, in seconds.

Enjoy!




