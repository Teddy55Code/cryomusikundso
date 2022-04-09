import tkinter as tk
from PIL import Image,ImageTk
from pytube import YouTube
import re
import unicodedata
from pydub import AudioSegment
import threading
import random
import time
import shutil
import os
import json

with open("resources/loading_messages.json", encoding="UTF-8") as f:
    downloading_messages = json.load(f)

root = tk.Tk()
root.title("youtube to mp3/mp4 for cryo uwu")
root.geometry("500x500")
root.resizable(False, False)
root["bg"] = "black"

try:
    root.iconbitmap(r'resources/icon.ico')
except Exception:
    pass

download_mp3 = True

img= ImageTk.PhotoImage(Image.open("resources/Huntergruden.png"))

canvas = tk.Canvas(root, height=500, width=500)
canvas.pack(expand = tk.YES, fill = tk.BOTH)

canvas.create_image(0,0,anchor=tk.NW,image=img)

toppadding_for_input = tk.LabelFrame(canvas, bg='#72D0FF', height=60)
toppadding_for_input.pack()

best_font = ("Comic Sans MS", 15, "bold")

url_input = tk.Entry(canvas, font=best_font, bg='#72D0FF', fg="pink", width=15)
url_input.pack()

bottom_uwu_padding_for_input = tk.LabelFrame(canvas, bg='#72D0FF', height=60)
bottom_uwu_padding_for_input.pack()

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

def loading_animation():
    while not exited:
        output_label["text"] = random.choice(downloading_messages)
        time.sleep(3)


def download_audio():
    global exited
    exited = False

    t2 = threading.Thread(target=loading_animation)
    t2.start()

    url1 = url_input.get()
    yt = YouTube(url1)

    if download_mp3:

        stream = yt.streams.get_audio_only()

        file_name = stream.default_filename[:-4]

        stream.download(output_path=f"./temp/")

        given_audio = AudioSegment.from_file(f"./temp/{stream.default_filename}", format="mp4")

        given_audio.export(f"./output/mp3/{file_name}.mp3", format="mp3")

        shutil.rmtree('temp')
        os.makedirs('temp')

    else:
        stream = yt.streams.get_highest_resolution()

        file_name = stream.default_filename[:-4]

        stream.download(output_path=f"./output/mp4")

    exited = True

    display_name = file_name
    for counter, character in enumerate(file_name):
        if counter % 35 == 0:
            display_name = display_name[:counter] + "\n" + display_name[counter:]
    output_label["text"] = f"downlaoded {display_name}"

def start_download_audio():
    t1 = threading.Thread(target=download_audio)
    t1.start()

def toggle_mp3_mp4():
    global download_mp3
    if download_mp3:
        toggle_format_button["image"] = mp4_btn_img
    else:
        toggle_format_button["image"] = mp3_btn_img
    download_mp3 = not download_mp3

btn_img = tk.PhotoImage(file='./resources/downlaod.png')

mp4_btn_img = tk.PhotoImage(file='./resources/mp4.png')

mp3_btn_img = tk.PhotoImage(file='./resources/mp3.png')

entry_button = tk.Button(canvas, command=start_download_audio, image=btn_img)
entry_button.pack()

output_label = tk.Label(canvas, font=best_font, bg='#72D0FF', fg="pink")
output_label.pack()

toppadding_for_toggle_format_button = tk.LabelFrame(canvas, bg='#72D0FF', height=20)
toppadding_for_toggle_format_button.pack()

fromat_lable = tk.Label(canvas, font=best_font, bg='#72D0FF', fg="pink", text="mp3          mp4")
fromat_lable.pack()

toggle_format_button = tk.Button(canvas, command=toggle_mp3_mp4, image=mp3_btn_img)
toggle_format_button.pack()

root.mainloop()
