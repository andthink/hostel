import sys
from shutil import copyfile
import subprocess
import wx


class Hostel(wx.Frame):

    def __init__(self, parent, title):
        self.timer = None
        self.w = 700
        self.h = 600
        self.output = None
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

        self.output = wx.StaticText(pnl, id=i+1, label="", pos=(50, 20 * (i + 2)))
        self.output.SetForegroundColour((255, 0, 0))  # set text color

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
        pnl = wx.Panel(self)

        with open('/tmp/writehosts', 'w') as f:
            for item in self.lines:
                print >> f, item
        bash_command = "pkexec env DISPLAY=:0 XAUTHORITY=/run/user/1000/gdm/Xauthority cp /tmp/writehosts /etc/hosts"

        error = None
        try:
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        except OSError as e:
            wx.MessageBox("Error while overwriting host file: " + e.strerror, 'Error', wx.OK)
        if error != '':
            self.output.SetLabel('Hosts successfully saved')
            self.timer = wx.Timer(self, 999)
            self.Bind(wx.EVT_TIMER, self.delete)
            self.timer.Start(3000)  # 3 second interval

    def delete(self, event):
        self.output.SetLabel('')


ex = wx.App()
Hostel(None, 'Hostel')
ex.MainLoop()
