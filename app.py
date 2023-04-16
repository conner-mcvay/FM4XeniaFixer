import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import gc

root = tk.Tk()
root.withdraw()

message = "It is CRITICAL that you back up your RenderScenarios folder as well as your tracks folder before proceeding."
title = "WARNING"
response = messagebox.askokcancel(title=title, message=message)

# Destroy the window
root.destroy()

if response:
    tracks_path = filedialog.askdirectory(title="Select your FM4 Media/tracks folder")
    #patch tracks
    for root, dirs, files in os.walk(tracks_path):
        for filename in files:
            if filename == "TrackSettings.xml" or filename == "TrackSettings1.xml":
                file_path = os.path.join(root, filename)
                with open(file_path, "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if '<DetailBlurMPHForMaxBlur value="' in line:
                            line = '  <DetailBlurMPHForMaxBlur value="9999999960.000000"/>\n'
                        file.write(line)
                    file.truncate()
                    file.close()

    #patch cars
    cars_path = filedialog.askdirectory(title="Select your FM4 Media/RenderScenarios folder")
    for root, dirs, files in os.walk(cars_path):
        for filename in files:
            if "car" in filename.lower() and filename.endswith(".xml"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    for i, line in enumerate(lines):
                        if i == len(lines)-2:
                            file.write('  <SkipshadowMapUnlessCockpit value="1"/>\n')
                            if not line.endswith('\n'):
                                file.write('\n')
                        file.write(line)
                    file.truncate()
                    file.close()
    else:
        exit(0)
gc.collect()