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

def get_words(config):
    if config["words_file"] == "":
        assert config["links_file"] != "", "At least one of words_file, links_file should be non empty"
        return []
    else:
        fname = config["words_file"]    
        with open(fname, "r") as f:
            words = [x[:-1] for x in f.readlines()]
        return words    

def extract_mp4(L):
    from bs4 import BeautifulSoup as bs
    soup = bs(requests.get(L).content)
    return "https://www.handspeak.com" + soup.find_all("video", {"class": "v-asl"})[0].get("src")

def get_links(words, config):
    links = {}
    for word in words:
        w = word.split(" ")[0].lower()
        if w[-1]==",":
            w = w[:-1]
        links[word] = f"http://www.handspeak.com/word/{w[0]}/{w[:3]}/{w}.mp4"
    if config["links_file"] != "":
        fname = config["links_file"]    
        with open(fname, "r") as f:
            l = json.loads(f.read())
            for w in l.keys():
                links[w] = extract_mp4(l[w])
    return links    

def dl_gifs(links):
    gifs = {}
    fname = config["words_file"] + config["links_file"]
    directory = f"./.{fname}_output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for word in links:    
        link = links[word]
        with open(f"{directory}/{slugify(word)}.mp4", "wb") as f:
            f.write(requests.get(link).content)
        mp4 = VC(f"{directory}/{slugify(word)}.mp4")
        mp4.write_gif(f"{directory}/{slugify(word)}.gif", fps=10,program='imageio', verbose = False, logger = None)
        gifs[word] = f"{slugify(word)}.gif"
        os.remove(f"{directory}/{slugify(word)}.mp4")
    return directory, gifs

def make_deck(gifs, direc, config):
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
    for word in gifs:
        gif = gifs[word]
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
    package.media_files = [f"{direc}/{gifs[word]}" for word in gifs]
    return package

words = get_words(config)
links = get_links(words, config)
direc, gifs  = dl_gifs(links)
package = make_deck(gifs, direc, config)
package.write_to_file(f"{config['output_name']}.apkg")

for f in os.listdir(direc):
    os.remove(f"{direc}/{f}")
os.rmdir(direc)
