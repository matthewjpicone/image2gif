# -*- coding: utf-8 -*-
"""
Image 2 GIF Conversion Tool

This module provides a graphical user interface (GUI) for creating animated GIFs from a collection of PNG images.
It allows users to select a source directory containing PNG images and a destination directory to save the resulting
GIF. The tool sorts the images alphabetically and sequentially compiles them into a single animated GIF file. It also
features a preview function to display the created GIF within the GUI.

Example
-------
To run this program, execute the following command:

    $ python image2gif.py

Attributes
----------
None

Author : matthewpicone
Date   : 3/12/2023
"""

import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence
import imageio

def create_gif():
    """
    Create an animated GIF from PNG images in a specified source folder.

    This function reads PNG files from the source folder, sorts them, and
    compiles them into an animated GIF. The resulting GIF is saved in the
    destination folder. It updates the GUI status label based on the success
    or failure of the GIF creation process.

    Raises
    ------
    Exception
        If an error occurs during GIF creation.
    """
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()

    if not os.path.isdir(source_folder) or not os.path.isdir(destination_folder):
        status_label.config(text="Please select valid source and destination folders.", fg="red")
        return

    try:
        files = os.listdir(source_folder)
        files = [f for f in files if f.lower().endswith('.png')]
        files.sort()

        if not files:
            status_label.config(text="No PNG files found in the source folder.", fg="red")
            return

        with imageio.get_writer(f'{destination_folder}/output.gif', mode='I') as writer:
            for image in files:
                img = Image.open(os.path.join(source_folder, image))
                writer.append_data(imageio.core.asarray(img))

        status_label.config(text="GIF created successfully!", fg="green")
        display_animated_gif(f'{destination_folder}/output.gif')
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

def display_animated_gif(gif_path):
    """
    Display an animated GIF in the GUI.

    Parameters
    ----------
    gif_path : str
        The file path of the GIF to be displayed.

    Notes
    -----
    This function loads an animated GIF, extracts its frames, and sets up
    a loop to display these frames in sequence on the GUI.
    """
    gif = Image.open(gif_path)

    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

    def update_label(index):
        frame = frames[index]
        preview_label.config(image=frame)
        preview_label.image = frame
        root.after(100, update_label, (index + 1) % len(frames))

    preview_label.config(image=frames[0])
    preview_label.image = frames[0]

    root.after(0, update_label, 1)

def select_source_folder(event):
    """
    Handle the event for selecting a source folder.

    Parameters
    ----------
    event : Event
        The event that triggered this function.

    Notes
    -----
    This function opens a dialog to select a directory and updates the
    source folder entry in the GUI with the chosen path.
    """
    source_folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_folder)

def select_destination_folder(event):
    """
    Handle the event for selecting a destination folder.

    Parameters
    ----------
    event : Event
        The event that triggered this function.

    Notes
    -----
    This function opens a dialog to select a directory and updates the
    destination folder entry in the GUI with the chosen path.
    """
    destination_folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_folder)

# GUI setup code
root = tk.Tk()
root.title("Image 2 GIF")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 1200
window_height = 1000
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

source_label = tk.Label(root, text="Source Folder:")
source_label.pack()

source_entry = tk.Entry(root, width=50)
source_entry.pack()

source_button = tk.Button(root, text="Browse")
source_button.pack()

destination_label = tk.Label(root, text="Destination Folder:")
destination_label.pack()

destination_entry = tk.Entry(root, width=50)
destination_entry.pack()

destination_button = tk.Button(root, text="Browse")
destination_button.pack()

preview_label = tk.Label(root)
preview_label.pack()

create_button = tk.Button(root, text="Create GIF", command=create_gif)
create_button.pack()

status_label = tk.Label(root, text="", fg="black")
status_label.pack()

source_button.bind("<Button-1>", select_source_folder)
destination_button.bind("<Button-1>", select_destination_folder)

root.mainloop()
