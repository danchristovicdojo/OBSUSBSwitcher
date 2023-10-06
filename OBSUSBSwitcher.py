import obsws_python as obs
from pynput import keyboard

import wx

# pass conn info if not in config.toml
cl = obs.ReqClient(host='192.168.23.58', port=4455, password='', timeout=3)
cl_events = obs.EventClient(host='192.168.23.58', port=4455, password='')
scenesRaw = cl.get_scene_list().scenes
activeScene = cl.get_current_program_scene().current_program_scene_name
scenes = []
for scene in scenesRaw:
    scenes.insert(0, scene["sceneName"])


def on_press(key):
    try:
        k = key.char  # single-char keys
        int(k)
    except:
        return
    if int(k) in range(1, len(scenes)):  # keys of interest
        print(f"Switching to scene {scenes[int(k) - 1]}")
        cl.set_current_program_scene(scenes[int(k) - 1])


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300,400))
        self.previousActiveScene = 0
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panel.SetFocus()
        self.boxes = []
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

        self.Show(True)

    def OnKeyDown(self, event=None):
        try:
            int(event)
        except:
            event = int(event)
        if event in range(0, len(scenes)):
            cl.set_current_program_scene(scenes[event])
            self.boxes[event].SetBackgroundColour("gray")
            if event == self.previousActiveScene:
                return    
            self.boxes[self.previousActiveScene].SetBackgroundColour("white")
            self.previousActiveScene = event


if __name__ == "__main__":
    app = wx.App(False)
    gui = MainWindow(None, "OBS Switcher")
    listener = keyboard.Listener(on_press=gui.OnKeyDown)
    listener.start()  # start to listen on a separate thread
    print("Listening")
    app.MainLoop()
