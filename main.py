import json
import os
import random
import shutil
import threading
import time
import tkinter as tk

import music_tag
import requests
from PIL import Image, ImageTk
from pydub import AudioSegment
from pytube import Playlist
from pytube import YouTube

from constants import *

with open("resources/loading_messages.json", encoding="UTF-8") as f:
    downloading_messages = json.load(f)

exited = False
lever_clicks = 0

root = tk.Tk()
root.title("youtube to mp3/mp4 for cryo uwu")
root.geometry("500x500")
root.resizable(False, False)
root["bg"] = "black"

try:
    root.iconbitmap(r"resources/icon.ico")
except Exception:
    pass

toggle_amount_button = None
selected_mp3 = True
selected_video = True

img = ImageTk.PhotoImage(Image.open("resources/Huntergruden.png"))

canvas = tk.Canvas(root, height=500, width=500)
canvas.pack(expand=tk.YES, fill=tk.BOTH)

canvas.create_image(0, 0, anchor=tk.NW, image=img)

toppadding_for_input = tk.LabelFrame(canvas, bg="#72D0FF", height=60)
toppadding_for_input.pack()

best_font = ("Comic Sans MS", 15, "bold")

url_input = tk.Entry(canvas, font=best_font, bg="#72D0FF", fg="pink", width=15)
url_input.pack()

bottom_uwu_padding_for_input = tk.LabelFrame(canvas, bg="#72D0FF", height=60)
bottom_uwu_padding_for_input.pack()


def loading_animation():
    while not exited:
        output_label["text"] = random.choice(downloading_messages)
        time.sleep(3)


def handle_download_video(url, playlist=None):
    video = YouTube(url)

    if selected_mp3:
        file_name = download_mp3(video, playlist)
    else:
        file_name = download_mp4(video, playlist)

    return file_name


def download_mp3(video, playlist):
    stream = video.streams.get_audio_only()

    file_name = stream.default_filename[:-4]

    stream.download(output_path=f"./temp/")

    given_audio = AudioSegment.from_file(f"./temp/{stream.default_filename}", format="mp4")

    if playlist:

        if not os.path.exists(f"./output/mp3/{playlist}"):
            os.makedirs(f"./output/mp3/{playlist}")

        given_audio.export(f"./output/mp3/{playlist}/{file_name}.mp3", format="mp3")
        file_path = f"./output/mp3/{playlist}/{file_name}.mp3"

    else:
        given_audio.export(f"./output/mp3/{file_name}.mp3", format="mp3")
        file_path = f"./output/mp3/{file_name}.mp3"

    res = requests.get(video.thumbnail_url, stream=True)

    with open(f"./temp/{file_name}.png", 'wb') as f:
        shutil.copyfileobj(res.raw, f)

    music_file = music_tag.load_file(file_path)

    music_file["title"] = video.title

    if playlist:
        music_file["album"] = playlist

    if video.captions["a.en"]:
        music_file["lyrics"] = video.captions["a.en"]

    music_file["artist"] = video.author

    music_file["artwork"] = open(f"./temp/{file_name}.png", "rb").read()

    music_file.save()

    shutil.rmtree("temp")
    os.makedirs("temp")

    return file_name


def download_mp4(video, playlist):
    stream = video.streams.get_highest_resolution()

    file_name = stream.default_filename[:-4]

    if playlist:
        stream.download(output_path=f"./output/mp4/{playlist}")
    else:
        stream.download(output_path=f"./output/mp4")

    return file_name


def setup_download():
    global exited
    exited = False

    t2 = threading.Thread(target=loading_animation)
    t2.start()

    url_from_input = url_input.get()

    if not selected_video:
        playlist = Playlist(url_from_input)

        if len(playlist.video_urls) != 0:
            for video in playlist.video_urls:
                handle_download_video(video, playlist.title)
            output_name = playlist.title
        else:
            output_name = handle_download_video(url_from_input)

    else:
        output_name = handle_download_video(url_from_input)

    exited = True

    display_name = output_name
    for counter, character in enumerate(output_name):
        if counter % 35 == 0:
            display_name = display_name[:counter] + "\n" + display_name[counter:]
    output_label["text"] = f"downlaoded {display_name}"


def starting_setup_download():
    t1 = threading.Thread(target=setup_download)
    t1.start()


def toggle_mp3_mp4():
    global selected_mp3, lever_clicks, toggle_amount_button

    if selected_mp3:
        toggle_format_button["image"] = right_btn_img
    else:
        toggle_format_button["image"] = left_btn_img
    selected_mp3 = not selected_mp3

    lever_clicks += 1
    if lever_clicks == CLICKS_TO_UNLOCK:
        fromat_lable = tk.Label(settings_canvas, font=best_font, bg="#72D0FF", fg="pink", text="video         playlist")
        fromat_lable.grid(row=0, column=1)

        toggle_amount_button = tk.Button(settings_canvas, command=toggle_video_playlist, image=left_btn_img)
        toggle_amount_button.grid(row=1, column=1)


def toggle_video_playlist():
    global selected_video
    if selected_video:
        toggle_amount_button["image"] = right_btn_img
    else:
        toggle_amount_button["image"] = left_btn_img
    selected_video = not selected_video


btn_img = tk.PhotoImage(file="./resources/downlaod.png")

right_btn_img = tk.PhotoImage(file="resources/right.png")

left_btn_img = tk.PhotoImage(file="resources/left.png")

entry_button = tk.Button(canvas, command=starting_setup_download, image=btn_img)
entry_button.pack()

output_label = tk.Label(canvas, font=best_font, bg="#72D0FF", fg="pink")
output_label.pack()

toppadding_for_toggle_format_button = tk.LabelFrame(canvas, bg="#72D0FF", height=20)
toppadding_for_toggle_format_button.pack()

settings_canvas = tk.Canvas(canvas, bg="#72D0FF", highlightbackground="#72D0FF")
settings_canvas.pack()

fromat_lable = tk.Label(settings_canvas, font=best_font, bg="#72D0FF", fg="pink", text="mp3          mp4")
fromat_lable.grid(row=0, column=0)

toggle_format_button = tk.Button(settings_canvas, command=toggle_mp3_mp4, image=left_btn_img)
toggle_format_button.grid(row=1, column=0)

root.mainloop()
