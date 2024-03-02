import genanki
import os
import requests 
from slugify import slugify
from moviepy.editor import VideoFileClip as VC
from sys import argv
import json

config = argv[1]
with open(config, "r") as f:
    config = json.loads(f.read())
fname = config["word_list_file_name"]    
with open(fname, "r") as f:
    words = [x[:-1] for x in f.readlines()]

gifs = []

for word in words:
    w = word.split(" ")[0].lower()
    uri = f"http://www.handspeak.com/word/{w[0]}/{w[:3]}/{w}.mp4"
    directory = f"./.{fname}_output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{slugify(word)}.mp4", "wb") as f:
        f.write(requests.get(uri).content)
    mp4 = VC(f"{directory}/{slugify(word)}.mp4")
    mp4.write_gif(f"{directory}/{slugify(word)}.gif", fps=10,program='imageio', verbose = False, logger = None)
    gifs.append(f"{slugify(word)}.gif")
    os.remove(f"{directory}/{slugify(word)}.mp4")

card = genanki.Model(
  1380120062,
  'card',
  fields=[
    {'name': 'front'},
    {'name': 'back'},
  ],
  templates=[
    {
      'name': 'Card',
      'qfmt': '<div class="center">{{front}}</div>',
      'afmt': """<div class="center">{{FrontSide}}</div> <hr id="answer"> <div class="center">{{back}}</div>""",
    }],
  css = """
    .center{
        width : fit-content;
        margin : auto;
        min-height : 100px;
    }
  """
  )

deck = genanki.Deck(
  2059400192,
  config["deck_name"])


for word, gif in zip(words, gifs):
    if config["eng_to_asl"].lower() == "true":
        note = genanki.Note(
          model=card,
          fields=[word, f"<img src='{gif}'/>"],
          tags = ["eng_to_asl"])
        deck.add_note(note)
    if config["asl_to_eng"].lower() == "true":
        note = genanki.Note(
          model=card,
          fields=[f"<img src='{gif}'/>", word],
          tags = ["asl_to_eng"])
        deck.add_note(note)

package = genanki.Package(deck)
package.media_files = [f"{directory}/{gif}" for gif in gifs]
package.write_to_file(f"{config['output_name']}.apkg")
for f in os.listdir(directory):
    os.remove(f"{directory}/{f}")
os.rmdir(directory)
