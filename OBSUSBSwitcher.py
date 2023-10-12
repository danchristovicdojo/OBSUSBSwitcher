import obsws_python as obs
import threading
import time
import hid
import wx

mapping = {
    b'\x07\x01\x00': 0,
    b'\x07\x02\x00': 1,
    b'\x07\x04\x00': 2,
    b'\x07\x08\x00': 3,
    b'\x07\x10\x00': 4,
    b'\x07 \x00': 5,
    b'\x07@\x00': 6,
    b'\x07\x80\x00': 7,
    b'\x07\x00\x01': 8,
}

vid = 0xf055	# Change it for your device
pid = 0x3534	# Change it for your device

class HidWatcher():
    def __init__(self, vid, pid, gui):
        self.vid = vid
        self.pid = pid
        self.gui = gui
    
    def start(self):
        threading.Thread(target=self.watch).start()

    def updateGui(self, num):
        if type(num) != int:
            return
        if num in range(0, len(scenes)):
            print(f"Switching to scene {scenes[num]}")
            cl.set_current_program_scene(scenes[num])
            wx.CallAfter(self.gui.boxes[num].SetBackgroundColour, "blue")
            wx.CallAfter(self.gui.boxes[num].Refresh)
            if num == self.gui.previousActiveScene:
                return    
            wx.CallAfter(self.gui.boxes[self.gui.previousActiveScene].SetBackgroundColour, "white")
            wx.CallAfter(self.gui.boxes[self.gui.previousActiveScene].Refresh)
            self.gui.previousActiveScene = num

    def watch(self):
        while True:
            try:
                wx.CallAfter(gui.show_usb_message, f"Trying to connect to USB Device {self.vid} {self.pid}")
                with hid.Device(self.vid, self.pid) as h:
                    wx.CallAfter(gui.show_usb_message, f"Connected to USB Controller")
                    while True:
                        report = h.read(64)
                        if report in mapping:
                            self.updateGui(mapping[report])
            except hid.HIDException:
                wx.CallAfter(gui.show_usb_message, f"USB Device {self.vid} {self.pid} not connected.")
                time.sleep(0.5)




# pass conn info if not in config.toml

host = "192.168.23.58"
port = 4455
password = ""
def connect_obs():
    global cl, cl_events, scenes, activeScene
    cl = obs.ReqClient(host=host, port=port, password=password, timeout=3)
    cl_events = obs.EventClient(host=host, port=port, password=password)
    scenesRaw = cl.get_scene_list().scenes
    activeScene = cl.get_current_program_scene().current_program_scene_name
    scenes = []
    for scene in scenesRaw:
        scenes.insert(0, scene["sceneName"])

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,400))
        self.previousActiveScene = 0
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetFocus()
        self.boxes = []
        self.connection_message = wx.StaticText(
            self.panel,
            id=-1,
            pos=(0, 300),
            label="",
            size=(300, 100)
            )
        self.usb_message = wx.StaticText(
            self.panel,
            id=-1,
            pos=(0, 320),
            label="",
            size=(300, 100)
            )
        
        
        self.Show(True)
    def create_boxes(self):
        for i, scene in enumerate(reversed(scenes)):
            i = (len(scenes)+1)%3 + i
            row = i//3
            pos = (100*(2-i%3), 100*row)
            if activeScene == scene:
                colour = "gray"
                self.previousActiveScene = scenes.index(scene)
            else:
                colour = "white"
            self.boxes.insert(0,wx.StaticBox(
                self.panel,
                i,
                label = scene,
                pos = pos, size = (100, 100),
            ))
            self.boxes[0].SetBackgroundColour(colour)
    def show_connection_message(self, e):
        self.connection_message.SetLabel(str(e))
    def show_usb_message(self, e):
        self.usb_message.SetLabel(str(e))
    # def OnKeyDown(self, event=None):


if __name__ == "__main__":
    app = wx.App(False)
    gui = MainWindow(None, "OBS Switcher")
    gui.show_connection_message(f"Connecting to OBS on {host}:{port}, {password}")
    count = 1
    while True:
        try:
            connect_obs()
            gui.create_boxes()
            gui.show_connection_message(f"Connected to OBS on {host}:{port}")
            break
        except Exception as e:
            e = f"We encountered an error connecting to OBS: {e}.\nRetrying in 3s... (retry {count})"
            gui.show_connection_message(str(e))
            count += 1
        time.sleep(1)
    pad = HidWatcher(vid=vid, pid=pid, gui=gui)
    pad.start()
    app.MainLoop()
    
    
