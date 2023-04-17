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
    tracks_path = ""
    while "tracks" not in tracks_path.lower():
        tracks_path = filedialog.askdirectory(title="Select your FM4 Media/tracks folder")
        if not tracks_path:
            # User clicked cancel or closed the dialog
            exit(0)
        if "tracks" not in tracks_path.lower():
            messagebox.showerror(title="Error",
                                 message="Not a valid tracks folder.")

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
    messagebox.showinfo(title="Success", message="Successfully patched tracks folder.")

    #patch cars
    cars_path = ""
    while "renderscenarios" not in cars_path.lower():
        cars_path = filedialog.askdirectory(title="Select your FM4 Media/RenderScenarios folder")
        if not cars_path:
            # User clicked cancel or closed the dialog
            exit(0)
        if "renderscenarios" not in cars_path.lower():
            messagebox.showerror(title="Error",
                                 message="Not a valid RenderScenarios folder.")

    for root, dirs, files in os.walk(cars_path):
        for filename in files:
            if "car" in filename.lower() and filename.endswith(".xml"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    for i, line in enumerate(lines):
                        if i == len(lines)-1:
                            file.write('  <SkipShadowMapUnlessCockpit value="1"/>\n')
                            if not line.endswith('\n'):
                                file.write('\n')
                        file.write(line)
                    file.truncate()
                    file.close()
        messagebox.showinfo(title="Success", message="Successfully patched RenderScenarios folder.")

gc.collect()
os._exit(0)
