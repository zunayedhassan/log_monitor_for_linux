__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
APPLICATION:    Log Monitor (GUI)
VERSION:        1.0.1
RELEASE DATE:   18th April, 2013    03:52 PM

DEVELOPER:      Mohammod Zunayed Hassan
EMAIL:          zunayed-hassan@live.com

PURPOSE:        1.  Monitor constantly log  files  of  /var/log/  directory
                    (Example: kern.log, syslog, auth.log, dpkg.log, ... etc)
                    
                2.  If anything changes happpend to those log files for any
                    event, then check those files and notify to user  about
                    what actually happened in GUI.
"""

from LogMonitorProgram import *

def main():
    root = Tk()

    app = LogMonitorProgram(
        parent         = root,
        title          = "Log Monitor",
        width          = 700,
        height         = 500,
        windowPosition = Window.WINDOW_POSITION["DEFAULT"],     # USAGE: (100, 50) or Window.WINDOW_POSITION["DEFAULT"] or Window.WINDOW_POSITION["CENTER_SCREEN"]
        resizeStyle    = None,                                  # USAGE: None or Window.RESIZE_STYLE["FIXED"] or Window.RESIZE_STYLE["WIDTH_ONLY"] or Window.RESIZE_STYLE["HEIGHT_ONLY"]
    )

    app.parent.mainloop()

if __name__ == "__main__":
    main()
    
