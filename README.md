# minecraft-server-wrapper
A wrapper for your minecraft server.

This is my very first usable python program. Hope you liked it.

Basically it's a replacement for 'run.bat' or 'run.sh'
It runs the server using the module subprocess and using re (regular expression)
it changes the way log data is displayed.

Adding colors to errors, warnings, player join, player leave, etc.
Making the console look a bit more colorful.


The project was originally written as a web based server console,
with PHP and Javascript working heavily together, using "screen" sessions to run the
server and execute commands.

Now because I was bored and had nothing to do, I tried to do the same thing but with Python.

# Usage:
Just put the run.py file in the same directory as spigot.jar / craftbukkit.jar
and run it from the terminal /  command prompt

~$ python3 run.py
  
# Args:
  -et (exit type): specify what to do when the server stops.
  - et 0: Exits when the server closes. (default)
  - et 1: Asks if you want to restart when the server closes.
  - et 2: Automatically restarts when the server closes (stop with Ctrl + C)

~$ python3 run.py -et 1
  
  exit type will by default be set to 0 if no arguements is specified.
        
This program has only been tested on Ubuntu 16.04 LTS.
modules: sys, time, shlex, subprocess, signal and re
