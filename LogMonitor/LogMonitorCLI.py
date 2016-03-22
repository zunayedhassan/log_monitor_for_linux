__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
APPLICATION:    Log Monitor (Command Line Interface)
VERSION:        1.0
RELEASE DATE:   18th April, 2013    03:52 PM

DEVELOPER:      Mohammod Zunayed Hassan
EMAIL:          zunayed-hassan@live.com

PURPOSE:        1.  Monitor constantly log  files  of  /var/log/  directory
                    (Example: kern.log, syslog, auth.log, dpkg.log, ... etc)
                    
                2.  If anything changes happpend to those log files for any
                    event, then check those files and notify to user  about
                    what actually happened in GUI.
"""

from LogMonitor import *
from LogFile    import *

def main():
    print("\nLOG MONITOR:\t")

    kernelLogFile = LogFile("kern.log")
    sysLogFile = LogFile("syslog")
    authLogFile = LogFile("auth.log")
    dpkgLogFile = LogFile("dpkg.log")

    logMonitor = LogMonitor()
    logMonitor.SetValue(logFiles = [kernelLogFile, sysLogFile, authLogFile, dpkgLogFile])
    print(str(logMonitor) + "\n")
    logMonitor.run()

if __name__ == "__main__":
    main()
