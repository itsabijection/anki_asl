This lets you programmatically create Anki cards from HANDSPEAK. There are broadly two ways to use it:

# Completely automated
Fill a file with a list of words, one word per line. Set the ```words_file``` field in config.json to this file name. Set the ```links_file``` to ''. Run ```python3 asl_to_anki.py config.json```. Expect some words not to be able to be found. This brings us to the next way.
# With manual replacements
If ```links_file``` is not set to "", the code will use the link provided to find the gif for the word provided. This overwrites the link that the program guesses at when a link is not manually provided, so if you have many errors you can add the correct links and restart to avoid manually merging decks.

# Other parameters
- ```deck_name```: what the deck appears as in Anki
- ```output_name```: the name of the ```.apkg``` file
- ```eng_to_asl```: set to ```True``` if you want cards where the front is english and the back is ASL
- ```asl_to_eng```: the opposite
The last two options are **NOT** mutually exclusive.
