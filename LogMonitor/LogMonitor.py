__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
from LogFile import *

"""
CLASS NAME:     LogMonitor

PURPOSE:        Search log files for changes on every given time
"""

class LogMonitor(threading.Thread):
    DELAY                       = 0.20
    FILE_CHECKING_INTERVAL      = 1
    LOG_FILES                   = []

    """
    METHOD NAME:    SetValue
    PARAMETER:      list<string> logFiles
    RETURN:         None

    PURPOSE:        Initialize LogMonitor object thread
    """
    def SetValue(self, logFiles):
        LogMonitor.LOG_FILES = logFiles

    """
    METHOD NAME:    run
    PARAMETER:      None
    RETURN:         None

    PURPOSE:        Check every log files for changes

    ALGORITHM:      1. Store total number of lines for given file as last number of
                       lines.

                    2. Check every certain amount of  time  for  file  modification
                       time changes.

                    3. If last file modification time is not same as  current  file
                       modification time, then follow through step 4.

                    4. Open the file and compare that file for changes.

                    5. Display/print notification.

                    6. Now, store current time  as  last  file  checking  time  and
                       current total number of lines as last total number of  lines
                       and  current  file  modification  date  time  as  last  file
                       modification date time.

                    7. Close file.
                    
                    8. Wait certain amount of  time and continue the whole  process
                       from step 4 to step 8
    """
    def run(self):
        self.Stop = False
        lastTime = time.time()

        while(not self.Stop):
            # If certain amount of  time of waiting is over
            if((time.time() - lastTime) >= LogMonitor.FILE_CHECKING_INTERVAL):
                for log in LogMonitor.LOG_FILES:
                    log.Notify()

                # Preparing for the next cycle
                lastTime = time.time()

            # Wait for certain amount of time.
            # NOTE: This line of code will save a lot of CPU process
            time.sleep(LogMonitor.DELAY)

        print("\n[i] MESSAGE: Log Monitor (Command Line Interface) is terminating now.\n")

    def __str__(self):
        logFileNames = ""

        for index in range(len(LogMonitor.LOG_FILES)):
            logFileNames += (str(LogMonitor.LOG_FILES[index]) + " ")

        return logFileNames

