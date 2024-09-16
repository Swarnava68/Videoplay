import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

def open_video():
    global video_path, cap
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if video_path:
        cap = cv2.VideoCapture(video_path)
        play_button.config(state="normal")

def play_video():
    global playing
    playing = True
    while cap.isOpened() and playing:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)
            video_label.config(image=photo)
            root.update()
        else:
            break

def pause_video():
    global playing
    playing = False

def stop_video():
    global playing, cap
    playing = False
    cap.release()
    video_label.config(image="")

def save_video():
    if video_path:
        save_path = filedialog.asksaveasfilename(filetypes=[("Video Files", "*.mp4")])
        if save_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(save_path, fourcc, 20.0, (cap.get(3), cap.get(4)))
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    break
            out.release()
            cap.release()
            messagebox.showinfo("Success", "Video saved successfully!")
        else:
            messagebox.showwarning("Error", "Please choose a save path.")
    else:
        messagebox.showwarning("Error", "Please open a video first.")

root = tk.Tk()
root.title("Simple Video Editor")
root.geometry("800x600")

video_label = tk.Label(root)
video_label.pack(fill="both", expand=True)

open_button = tk.Button(root, text="Open Video", command=open_video)
open_button.pack(side="left")

play_button = tk.Button(root, text="Play", command=play_video, state="disabled")
play_button.pack(side="left")

pause_button = tk.Button(root, text="Pause", command=pause_video, state="disabled")
pause_button.pack(side="left")

stop_button = tk.Button(root, text="Stop", command=stop_video, state="disabled")
stop_button.pack(side="left")

save_button = tk.Button(root, text="Save", command=save_video, state="disabled")
save_button.pack(side="left")

root.mainloop()