__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, random
from Tkinter import *
from ttk import *

class Window(Frame):
    WINDOW_POSITION = {
        "DEFAULT"       : 0,
        "CENTER_SCREEN" : 1
    }

    RESIZE_STYLE = {
        "FIXED"         : 0,
        "WIDTH_ONLY"    : 1,
        "HEIGHT_ONLY"   : 2
    }

    def __init__(self, parent, title, width, height, windowPosition = None, iconName = None, resizeStyle = None, bgColor = None, theme = "clam"):
        Frame.__init__(self, master = parent, background = bgColor)

        self.parent = parent
        self.parent.wm_title(title)
        (Style()).theme_use(theme)

        self.SetIcon(iconName)

        # Setting up window position on the screen
        if   ((windowPosition == Window.WINDOW_POSITION["DEFAULT"]) or (windowPosition == None)):
            self.SetFramePositionToRandom(width, height)
        elif (windowPosition == Window.WINDOW_POSITION["CENTER_SCREEN"]):
            self.SetFramePositionToCenter(width, height)
        else:
            self.parent.wm_geometry(str(width) + "x" + str(height) + "+" + str(windowPosition[0]) + "+" + str(windowPosition[1]))   # EXAMPLE: self.parent.wm_geometry("300x200+100+50")

        # Setting resizable style
        if   (resizeStyle == Window.RESIZE_STYLE["FIXED"]):
            self.parent.resizable(False, False)
        elif (resizeStyle == Window.RESIZE_STYLE["WIDTH_ONLY"]):
            self.parent.resizable(True, False)
        elif (resizeStyle == Window.RESIZE_STYLE["HEIGHT_ONLY"]):
            self.parent.resizable(False, True)


    def SetIcon(self, iconName):
        if (iconName != None):
            windowSystem = self.master.tk.call("tk", "windowingsystem")

            if   (windowSystem == "win32"): # Windows
                iconName += ".ico"
            elif (windowSystem == "x11"):   # Unix
                iconName = "@" + iconName + ".xbm"

            self.parent.wm_iconbitmap(iconName)


    def SetFramePositionToRandom(self, width, height):
        screenWidth  = self.parent.winfo_screenwidth()
        screenHeight = self.parent.winfo_screenheight()

        posX = random.randint(0, (screenWidth - width))
        posY = random.randint(0, (screenHeight - height))

        self.parent.wm_geometry(str(width) + "x" + str(height) + "+" + str(posX) + "+" + str(posY))


    def SetFramePositionToCenter(self, width, height):
        screenWidth  = self.parent.winfo_screenwidth()
        screenHeight = self.parent.winfo_screenheight()
        self.parent.wm_geometry(str(width) + "x" + str(height) + "+" + str((screenWidth - width) / 2) + "+" + str((screenHeight - height) / 2))


