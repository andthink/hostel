import sys
from shutil import copyfile

import wx


class Hostel(wx.Frame):

    def __init__(self, parent, title):
        self.w = 700
        self.h = 600
        super(Hostel, self).__init__(parent, title=title, size=(self.w, self.h))
        self.cb = []
        try:
            copyfile("/etc/hosts", "/tmp/hosts.bak")
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
        except:
            print("Unexpected error:", sys.exc_info())
            exit(1)

        text_file = open("/etc/hosts", "r")
        self.lines = text_file.read().split("\n")
        print(self.lines)

        text_file.close()

        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)

        i = 0
        for val in self.lines:
            if len(val) == 0:
                continue
            ccb = wx.CheckBox(pnl, id=i, label=val, pos=(10, 20 * (i + 1)), size=(len(val) * 10, 20))
            if val[0] != "#":
                ccb.SetValue(True)

            self.cb.append(ccb)
            i = i + 1

        self.Bind(wx.EVT_CHECKBOX, self.onChecked)

        save = wx.Button(pnl, id=i, label="Save", pos=(self.w - 10 - 100, 20 * (i + 1)))
        save.Bind(wx.EVT_BUTTON, self.save)

        self.Centre()
        self.Show(True)

    def onChecked(self, e):
        cb = e.GetEventObject()

        if cb.GetValue():
            a = cb.GetLabel().strip('#').strip(' ')
            cb.SetLabel(a)
            print(cb.GetLabel(), ' is clicked', cb.GetValue())
        else:
            a = '#' + cb.GetLabel()
            cb.SetLabel(a)
            print(cb.GetLabel(), ' is clicked', cb.GetValue())
        self.lines[cb.GetId()] = cb.GetLabel()
        print(self.lines);

    def save(self, e):
        with open('/etc/hosts', 'w') as f:
            for item in self.lines:
                print >> f, item

ex = wx.App()
Hostel(None, 'Hostel')
ex.MainLoop()
