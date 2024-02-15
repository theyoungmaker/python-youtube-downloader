import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
from check_youtube_url import is_valid_url
from moviepy.editor import *
import os

def download_video():
    url = url_entry.get()
    save_path = folder_path.get()
    if not is_valid_url(url):
        messagebox.showerror("Error", "Invalid YouTube URL")
        return
    if not save_path:
        messagebox.showerror("Error", "Please select a folder to save the video")
        return

    try:
        yt = YouTube(url)
        
        # Download MP4
        if mp4_var.get():
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if video_stream:
                video_stream.download(save_path)
        
        # Download MP3
        if mp3_var.get():
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream:
                out_file = audio_stream.download(output_path=save_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                # Convert audio to MP3
                audio_clip = AudioFileClip(out_file)
                audio_clip.write_audiofile(new_file)
                # Remove the original download if desired
                os.remove(out_file)
                
        messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

# Initialize Tkinter
root = tk.Tk()
root.title("YouTube Video Downloader")

# Define variables
folder_path = tk.StringVar()
mp3_var = tk.BooleanVar()
mp4_var = tk.BooleanVar()

# Create UI components
url_label = tk.Label(root, text="YouTube URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()
mp4_checkbox = tk.Checkbutton(root, text="Download MP4", variable=mp4_var)
mp4_checkbox.pack()
mp3_checkbox = tk.Checkbutton(root, text="Download MP3", variable=mp3_var)
mp3_checkbox.pack()
folder_label = tk.Button(root, text="Choose Folder", command=select_folder)
folder_label.pack()
folder_entry = tk.Entry(root, textvariable=folder_path, width=50)
folder_entry.pack()
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack()

# Run the application
root.mainloop()
