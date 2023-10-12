# OBSUSBSwitcher

A tool to switch scenes in OBS over WebSockets.

A keypad that outputs gamepad buttons 0-9 is required.

This can be run as a standalone Python script, or built with PyInstaller to make an executable.

Connection variables for the OBS host are on lines 9, 10 & 11.

To run this on a Windows machine, download this repository, install Python, install dependencies, and run the script:

```powershell
winget install python
cd "C:\Users\your-user\download-location\"
pip3 install -r requirements.txt
python3 OBSUSBSwitcher.py
```

This should run the script, and you'll get a simple interface with some output if you're not on the right network.

