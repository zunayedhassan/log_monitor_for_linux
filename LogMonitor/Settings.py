__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle

"""
CLASS NAME:     Settings

PURPOSE:        Hold information about user settings
"""
class Settings:
    SHOW_KERNEL_LOG         = True
    SHOW_SYSTEM_LOG         = True
    SHOW_AUTHENTICATION_LOG = True
    SHOW_DEBIAN_PACKAGE_LOG = True


    def __str__(self):
        return ("[Settings]\n" + "Show Kernel Log:\t\t" + str(self.SHOW_KERNEL_LOG)+ "\nShow System Log:\t\t" + str(self.SHOW_SYSTEM_LOG) + "\nShow Authentication Log:\t" + str(self.SHOW_AUTHENTICATION_LOG) + "\nShow Debian Package Log:\t" + str(self.SHOW_DEBIAN_PACKAGE_LOG) + "\n")
