#!/usr/bin/env python
# coding=utf-8

# @Su.Py~#_

import os
import sys
import time
import re
import signal
import subprocess
import shlex

class clr(object):
    """docstring for clr"""
    magenta = "\033[95m"
    cyan = "\033[94m"
    green = "\033[92m"
    warn = "\033[93m"
    err = "\033[91m"
    end = "\033[0m"
    bold = "\033[1m"
    undeline = "\033[4m"


class server(object):
    """docstring for server"""
    def __init__(self):
        super(server, self).__init__()
        self.process = False
        self.run_args = "java -Xms512M -Xmx512M -XX:+UseConcMarkSweepGC -jar spigot.jar"
        self.line = False
        self.clr_end = False
        self.log_user = False
        self.log_time = True
        self.log_warn = False
        self.log_err = False

    def filters(self):
        if(re.search(r"\[(\d{2}):(\d{2}):(\d{2})", self.line)):
            self.line = re.sub(r"\[(\d{2}):(\d{2}):(\d{2})", time.strftime("%I:%M:%S"), self.line)
            self.log_time = True
        else:
            self.log_time = False

        if(re.search(r"INFO\]:", self.line)):
            if(re.search(r"\[/[0-9]+(?:\.[0-9]+){3}:[0-9]+\] logged in with entity id \d", self.line)):
                self.line = re.sub(r"INFO\]:", "{}{}+{}{} INFO:{}{}".format(clr.green, clr.bold, clr.end, clr.cyan, clr.end, clr.green), self.line)
                self.log_user = True
            elif(re.search(r"[a-zA-Z0-9_.-] left the game.", self.line)):
                self.line = re.sub(r"INFO\]:", "{}{}-{}{} INFO:{}{}".format(clr.err, clr.bold, clr.end, clr.cyan, clr.end, clr.err), self.line)
                self.log_user = True
            else:
                self.line = re.sub(r"INFO\]:", "{}| INFO:{}".format(clr.cyan, clr.end), self.line)

            if(self.log_warn):
                self.log_warn = False
            elif(self.log_err):
                self.log_err = False

        elif(re.search(r"WARN\]:", self.line)):
            self.line = re.sub(r"WARN\]:", "{}{}!{}{} WARN:".format(clr.warn, clr.bold, clr.end, clr.warn), self.line)
            self.clr_end = True
            self.log_warn = True
            if(self.log_err):
                self.log_err = False

        elif(re.search(r"ERROR\]:", self.line)):
            self.line = re.sub(r"ERROR\]:", "{}{}x{}{} ERROR:".format(clr.err, clr.bold, clr.end, clr.err), self.line)
            self.clr_end = True
            self.log_err = True
            if(self.log_warn):
                self.log_warn = False

        if(self.log_warn and not(self.log_time)):
            print("                 {}{}{}".format(clr.warn, self.line, clr.end), end="")
        elif(self.log_err and not(self.log_time)):
            print("                  {}{}{}".format(clr.err, self.line, clr.end), end="")
        else:
            print(self.line, end="")
            if(self.clr_end):
                print(clr.end, end="")
                self.clr_end = False
        if(self.log_user):
            print(clr.end, end="")
            self.log_user = False

    def run(self):
        print("{} {}| SYSTM:{} Starting the server...".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end))
        try:
            self.process = subprocess.Popen(shlex.split(self.run_args), stdout = subprocess.PIPE, bufsize = 1)
        except Exception as err:
            print("{} {}| SYSTM:{}{} ERROR: An error has occured while starting the server.{}".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end, clr.err, clr.end))
            print("{} {}| SYSTM:{}{}        {}{}".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end, clr.err, err, clr.end))

            return False
        else:
            print("{} {}| SYSTM:{}{} Successfully started the server.{}".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end, clr.green, clr.end))

        for self.line in iter(self.process.stdout.readline, b''):
            self.line = self.line.decode()
            self.filters()

        self.process.stdout.close()
        self.process.wait()
        self.process = False

    def quit(self, signal, frame):
        print("\n")
        print("{} {}| SYSTM:{} Reviced exit command.".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end))
        if(self.process):
            print("{} {}| SYSTM:{} Stopping the server...".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end))
            self.process.stdin.write("stop\n".encode())
            for self.line in iter(self.process.stdout.readline, b''):
                self.line = self.line.decode()
                self.filters()
            print("{} {}| SYSTM:{} Server stopped.".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end))
        print("{} {}| SYSTM:{} Exiting.".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end))
        sys.exit(0)


if __name__ == '__main__':
    if(len(sys.argv) > 2):
        if(sys.argv[1] == "-et"):
            if(len(sys.argv) == 3):
                if(sys.argv[2] == "0"):
                    et = 0
                elif(sys.argv[2] == "1"):
                    et = 1
                elif(sys.argv[2] == "2"):
                    et = 2
            else:
                print('''Invalid argurement.
        Usage: -et [0/1/2]

        0: Exits when the server closes. (Default)
        1: Asks if you want to restart when the server closes.
        2: Automatically restarts when the server closes (stop with Ctrl + C)
                ''')
                sys.exit(0)
    else:
        et = 0

    svr = server()
    signal.signal(signal.SIGINT, svr.quit)

    if(et == 2):
        while(True):
            run = svr.run()
            print("{} {}| SYSTM:{}{} Server closed, auto restarting. (ar=True).{}".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end, clr.green, clr.end))
            print("                  wait for 5 seconds.")
            time.sleep(5)

    elif(et == 1):
        while(True):
            run = svr.run()
            ask = input("{} {}| SYSTM:{} Server closed, restart? [y/n]: ".format(time.strftime("%I:%M:%S"), clr.magenta, clr.end))
            if(ask == "N" or ask == "n"):
                sys.exit(0)
    elif(et == 0):
        run = svr.run()
