import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from object_tracker import main as tracker
from absl import app
import sys

# Creating the default menu window
root = tk.Tk()
root.configure(background="#DCDAD5")
root.title("Menu")
style = ttk.Style(root)
style.theme_use("clam")
outputData = "/results"

# Creating features within the menu window
count = tk.IntVar()
count_checkbox = ttk.Checkbutton(
    root, text="count all objects", variable=count)
total_class = tk.BooleanVar()
total_class_checkbox = ttk.Checkbutton(
    root, text="count objects by class", variable=total_class)
count_dir = tk.BooleanVar()
count_dir_checkbox = ttk.Checkbutton(
    root, text="count by direction", variable=count_dir)
count_dir_class = tk.BooleanVar()
count_dir_class_checkbox = ttk.Checkbutton(
    root, text="count direction per class", variable=count_dir_class)
trail = tk.BooleanVar()
trail_checkbox = ttk.Checkbutton(root, text="show trail", variable=trail)
trail_radius_label = ttk.Label(root, text="trail radius: ", anchor="center")
trail_rad = tk.IntVar()
trail_rad_spinbox = ttk.Spinbox(
    root,  textvariable=trail_rad, from_=0, to=10, increment=1, state=tk.DISABLED)
show_video = tk.BooleanVar()
show_video_checkbox = ttk.Checkbutton(
    root, text="show video output", variable=show_video)
min_hits = tk.IntVar()
min_hits_spinbox = ttk.Spinbox(root, textvariable=min_hits, from_=1, to=10, width=60)
min_hits_label = ttk.Label(root, text="minimum appearances: ", anchor="center")
title = ttk.Label(root, text="OPTIONS: ", anchor="center",font=28)

# Setting the location of features within the menu window
title.grid(row=1, column=1, sticky="ew")
min_hits_spinbox.grid(row=6, column=2, sticky="ew")
trail_rad_spinbox.grid(row=5, column=2, sticky="ew")
count_checkbox.grid(row=3, sticky="ew")
total_class_checkbox.grid(row=4, sticky="ew")
count_dir_checkbox.grid(row=6, sticky="ew")
count_dir_class_checkbox.grid(row=7, sticky="ew")
trail_checkbox.grid(row=5, sticky="ew")
trail_radius_label.grid(row=5, column=1, sticky="ew")
show_video_checkbox.grid(row=2, sticky="ew")
min_hits_label.grid(row=6, column=1, sticky="ew")


# If user requests trail radius, allow a value to be inputted for the radius otherwise hide option
def trail_radius_state():
    if trail.get() == 1:
        trail_rad_spinbox.config(state=tk.NORMAL)
    else:
        trail_rad_spinbox.config(state=tk.DISABLED)


trail_checkbox.config(command=trail_radius_state)


# Allows for the selection of a video file by default showing mp4 files
def c_open_video_file():
    videoFile = filedialog.askopenfilenames(
        parent=root,
        initialdir='/',
        filetypes=[
            ("MP4", "*.mp4"),
            ("All files", "*")])
    try:

        global input_file
        input_file = videoFile[0]
        ttk.Label(root, text=input_file).grid(
            row=2, column=2, padx=4, pady=4, sticky='ew')
    except:
        print("No file exists")


# Allows the location the output video will be saved to to be defined
def save_video_location():
    videoSaveLocation = filedialog.asksaveasfilename(
        initialdir="/", title="Select file", filetypes=(("all files", "*.*"),("mp4 files","*.mp4")))
    try:
        global output
        output = videoSaveLocation+".mp4"
        ttk.Label(root, text=output).grid(
            row=3, column=2, padx=4, pady=4, sticky='ew')
    except:
        print("No file exists")


# Allows the location data will be saved to to be defined
def save_data_location():
    dataSaveLocation = filedialog.asksaveasfilename(
        initialdir="/", title="Select file", filetypes=(("all files", "*.*"),("json files","*.json")))
    try:
        global outputData
        outputData = dataSaveLocation
        ttk.Label(root, text=outputData).grid(
            row=4, column=2, padx=4, pady=4, sticky='ew')
    except:
        print("No file exists")


# Runs detection with selected options when requested
def run_detection():
    args = [None, "--model", "yolov4"]
    if "input_file" in globals():
        args.append("--video")
        args.append(input_file)
    if "output" in globals():
        args.append("--output")
        args.append(output)
    if "outputData" in globals():
        args.append("--tracked_objects_names")
        args.append(outputData)
    if count.get() == 1:
        args.append("--count")
    if total_class.get() == 1:
        args.append("--total_class")
    if count_dir.get() == 1:
        args.append("--total_dir")
    if count_dir_class.get() == 1:
        args.append("--total_dir_class")
    if trail.get() == 1:
        args.append("--trail")
    if trail_rad_spinbox.state() == tk.NORMAL and trail_rad_spinbox.get() != 0:
        args.append("--trail_radius ")
        args.append(str(trail_rad_spinbox.get()))
    if min_hits.get() != 0:
        args.append("--min_hits")
        args.append(str(min_hits.get()))
    if show_video.get() == 0:
        args.append("--dont_show")
    # Stops the program from closing when detection is run
    try:
        app.run(tracker, args)
    except SystemExit as exit_obj:
        if exit_obj.code is not None:
            raise exit_obj
        open_result_window()

# Creates results window when analysis is complete    
def open_result_window():
    resultWindow = tk.Toplevel(root)
    resultWindow.title("Results")
    title = ttk.Label(resultWindow, text="RESULTS:", anchor="center", font=28)
    title.grid(row=1, sticky="ew")

    # Populates results window with analysis results
    with open(outputData + '.txt', 'r') as stored_data:
        file_contents = stored_data.read()
    file_contents = file_contents.replace("{","\n").replace("}, ","\n").replace("\"","").replace("}","")
    if file_contents == "":
        file_contents = "The results file is empty"
    results = ttk.Label(resultWindow, text=file_contents)
    results.grid(row=2, sticky="ew")

# Creates help window with guidelines within
def help_window():
    helpWindow = tk.Toplevel(root)
    helpWindow.title("Help")
    title = ttk.Label(helpWindow, text="HELP", font=28, anchor="center")
    title.grid(row=1, sticky="ew")
    show_trail = ttk.Label(helpWindow, text="Show trail will apply a breadcrumb trail following each detected object to the video.")
    show_trail.grid(row=2, sticky="ew")
    trail_radius = ttk.Label(helpWindow, text="Selecting show trail will give the option to change the rail radius. This value references the radius of the trail in pixels. ")
    trail_radius.grid(row=3, sticky="ew")
    video_output = ttk.Label(helpWindow, text="Show video output specifies whether the created video should be outputted.")
    video_output.grid(row=4, sticky="ew")
    minimum_appearances = ttk.Label(helpWindow, text="Minimum appearances specifies the number of frames an object should be detected in before it is counted in calculations.")
    minimum_appearances.grid(row=5, sticky="ew")
    count_objects = ttk.Label(helpWindow, text="Count all objects specifies whether the count of the number of each object class detected should be displayed over the video.")
    count_objects.grid(row=6, sticky="ew")
    count_objects_class = ttk.Label(helpWindow, text="Count objects by class specifies whether the total number of objects detected per class should be calculated on completion of analysis.")
    count_objects_class.grid(row=7, sticky="ew")
    count_direction = ttk.Label(helpWindow, text="Count by direction specifies whether the total number of objects travelling in each direction should be calculated.")
    count_direction.grid(row=8, sticky="ew")
    count_direction_class = ttk.Label(helpWindow, text="Count direction per class specifies whether for each class the number of objects travelling in each direction should be calculated.")
    count_direction_class.grid(row=9, sticky="ew")
    select_video = ttk.Label(helpWindow, text="Select video file allows the video file to be analysed to be selected.")
    select_video.grid(row=10, sticky="ew")
    select_video_save = ttk.Label(helpWindow, text="Select video save location allows the location and name of the output video to be selected.")
    select_video_save.grid(row=11, sticky="ew")
    select_data_save = ttk.Label(helpWindow, text="select data save location allows the location and name of the saved data to be selected.")
    select_data_save.grid(row=12, sticky="ew")
    


# Creates buttons that call functions
ttk.Button(root, text="Select video file", command=c_open_video_file).grid(
    row=2, column=1, padx=4, pady=4, sticky='ew')
ttk.Button(root, text="Select video save location", command=save_video_location).grid(
    row=3, column=1, padx=4, pady=4, sticky='ew')
ttk.Button(root, text="Select data save location", command=save_data_location).grid(
    row=4, column=1, padx=4, pady=4, sticky='ew')
ttk.Button(root, text="Run tracking", command=run_detection).grid(
    row=8, column=1, padx=4, pady=4, sticky='ew')
ttk.Button(root, text="Help (f1)", command=help_window).grid(
    row=7, column=1, padx=4, pady=4, sticky='ew')

# Displays help window when f1 key is pressed
root.bind("<F1>", lambda event:help_window())

root.mainloop()
