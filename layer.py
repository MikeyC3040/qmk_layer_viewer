import wx, wx.adv
import hid
import sys
import threading

icons = ['./ico/Letter-Q.ico','./ico/Letter-C.ico','./ico/Letter-M.ico']
hover_text = "Keyboard Layers"

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

def init_hid():
    for d in hid.enumerate():
        if d['usage_page']== 65329:
            path = d['path']
    try:
        print("Opening the device")
        h = hid.device()
        h.open_path(path)
        return h
    except:
        e = sys.exc_info()
        print(e)
        print("You probably don't have the right device plugged in")
        h = None
    return h

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.h = init_hid()
        if self.h:
            self.running = True
            self.frame = frame
            super(TaskBarIcon, self).__init__()
            self.set_icon(0)
            self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.CreatePopupMenu)
            self.background()
        else:
            exit()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Restart', self.on_restart)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def on_restart(self,event):
        self.h = init_hid()

    def background(self):
        t = threading.Thread(target=self._run)
        if self.running:
            t.start()

    def _run(self):
        try:
            d = self.h.read(64,25)
            if d:
                text = ""
                for x in d:
                    text += chr(x)
                text = text.split(':')
                text = [text[0],text[1].split('\n')[0]]
                if text[0]=='layer':
                    if text[1] == "Default": icon = 0
                    elif text[1] == "Calc": icon = 1
                    elif text[1] == "Media": icon = 2
                wx.CallAfter(self.set_icon,icon)
            else:
                pass
        except OSError:
            pass
        except:
            print("Unexpected error:", sys.exc_info())
            pass
        self.background()

    def set_icon(self, index):
        icon = wx.Icon(icons[index])
        self.SetIcon(icon, hover_text)

    def on_exit(self, event):
        if self.h: self.h.close()
        self.running = False
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()

if __name__ == '__main__':
    main()