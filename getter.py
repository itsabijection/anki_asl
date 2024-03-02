import os
import requests 
from slugify import slugify
from moviepy.editor import VideoFileClip as VC
from sys import argv

fname = argv[1]
with open(fname, "r") as f:
    words = [x[:-1] for x in f.readlines()]

for word in words:
    try:
        w = word.split(" ")[0].lower()
        uri = f"http://www.handspeak.com/word/{w[0]}/{w[:3]}/{w}.mp4"
        directory = f"./{fname}_output"
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(f"{directory}/{slugify(word)}.mp4", "wb") as f:
            f.write(requests.get(uri).content)
        mp4 = VC(f"{directory}/{slugify(word)}.mp4")
        mp4.write_gif(f"{directory}/{slugify(word)}.gif", fps=10,program='imageio')
        remove(f"{directory}/{slugify(word)}.mp4")
    except:
        print(f"Couldn't get {word}")
