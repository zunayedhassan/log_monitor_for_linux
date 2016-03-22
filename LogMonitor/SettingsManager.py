__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle, getpass

"""
CLASS NAME:     SettingsManager

PURPOSE:        Save and Load user settings
"""
class SettingsManager:
        def __init__(self):
                self.HomeDirectory    = "/home/" + getpass.getuser() + "/"
                self.SettingsFileName = ".log_monitor_settings.obj"

        """
        METHOD NAME:    SaveSettings
        PARAMETER:      Settings settings
        RETURN:         None

        PURPOSE:        Save settings
        """
        def SaveSettings(self, settings):
                fout = open((self.HomeDirectory + self.SettingsFileName), "w")
                pickle.dump(settings, fout)
                fout.close()

        """
        METHOD NAME:    LoadSettings
        PARAMETER:      None
        RETURN:         Settings settings

        PURPOSE:        Load settings
        """
        def LoadSettings(self):
                fin = open((self.HomeDirectory + self.SettingsFileName), "r")
                settings = pickle.load(fin)
                fin.close()

                return settings
