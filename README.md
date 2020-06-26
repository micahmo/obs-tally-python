# obs-tally-python
This Python plugin for OBS Studio allows you to light up an LED on an Arduino board to use as a tally light when one or more scenes is active.

![](https://i.imgur.com/N3YpPOq.png)

# Arduino Setup
First, download and install the [Arduino IDE](https://www.arduino.cc/en/main/software).

Download the latest version of [obs-tally.ino](https://github.com/micahmo/obs-tally-python/blob/master/obs-tally.ino). Load the .ino file into the Arduino IDE. Choose "Verify", and then with your Arduino plugged in, choose "Upload".

**Note: The code assumes that the the LED is plugged into terminal 13 and GRD. You can adjust the Arduino code if your LED is plugged in differently by changing the LED constant at the beginning.**

![](https://i.imgur.com/hPqjICD.png)

# Python Script Setup
### Initial Setup
Download and install Python 3.6+ (for example, [3.6.8](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe)). Be sure to choose the option that adds Python to the PATH environment variable.

Open a Command Prompt or PowerShell and type the following command to install the required dependency.

```
pip install pyserial
```

In OBS Studio, open Tools > Scripts > Python Settings, and enter the path to the Python installation directory.

![](https://i.imgur.com/hcOl2hj.png)

### Plugin Setup
Download the latest version of [obs-tally-python.py](https://github.com/micahmo/obs-tally-python/blob/master/obs-tally-python.py).

In OBS Studio, open Tools > Scripts, click the plus icon to add a script, and browse to the obs-tally-python.py file.

Populate the options as desired.
 - **Scene(s)**: This is a line-separated list of scene names that will make the tally light active. OBS uses names as globally unique identifiers, so be sure to type (or copy/paste) the desired scenes names exactly, one on each line.
 - **COM Port**: This is the port that the Arduino board is plugged in to. The dropdown list shows every COM port that was detected upon loading the script, and you must select the port that points to the Arduino board. Sometimes the port will automatically be identified as being connected to an Aruidno, and the the word "Arduino" will be in the list next to the COM port number. Other times, it will have a generic name, and you must discover which port the board is plugged in to. Check Device Manager or the Arduino IDE if you are not sure. If the COM port is not displayed (for example, if the board was plugged in after the OBS was started), you may need to reload the plugin. However, once the COM port is identified and saved to the plugin configuration, it is tolerant to the board being unplugged and plugged back in (to the same port) during the OBS session.
 - **Value when live / Value when not live**: These are the values that are written to the COM port by the script when the desired scenes are active or not. These values should correspond to the values expected by the Arduino board. If you use obs-tally.ino as written, the values should be 1 and 2, respectively.
---
Once you have configured the script with the desired scenes, the LED on the Arduino board should light up when one of the scenes is active and should turn off when none of the scenes are active.
