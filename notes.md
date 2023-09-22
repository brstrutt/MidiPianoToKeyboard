So a while ago I got an electronic Keyboard, because music is good and I thought it might be fun to learn to play.
Anyway it didn't get as much use as I planned, probably my fault for repeatedly trying to play music that I liked, rather than looking for music I would be able to play.
So new idea, what if I could get my hands used to using the keyboard, get to know the position of the keys and get used to using both hands simultaneously, by using it for something other than playing music?

So this page is describing how I went about setting up my midi keyboard to work as an alternative controller for playing games.

Firstly, I did a big ol' google to see how to do it, found some software which claimed to do it, looked into some scripts for autohotkey that claim to achieve it, but in the end the first thing I found that actually worked was a Python script written by one BenOS on youtube (https://www.youtube.com/watch?v=R-pcY65_HDg).
This script basically works by using pygame's midi interface to listen for inputs from the midi keyboard, mapping each midi note to a keyboard button (alphanumeric keys only), then using pynput's keyboard interface to output the appropriate keypress in response to the mapped midi note being pressed on the piano.

Unfortunately I found that whilst this let me type into notepad, and even set the keybindings in the settings menu, it didn't actually translate into movement/actions ingame.
As a result I did some digging and found an alternative to the pynput method of virtually pressing keys. I dont fully understand it but it seems to involve some directX C interface and using Python bindings to that (https://pythonprogramming.net/direct-input-game-python-plays-gta-v/).

Anyway so I took this DirectX interface, created a dictionary of all valid DirectX keys and their counterparts by using Regex find and replace on the C defines that originally describe which key is represented by which value, and then modified the midi->keyboard bindings to use these key names rather than the alphanumeric literals that were being used before.

This new system was tested on Dark Souls (because of course I needed to make more mistakes this month) and ended up working pretty well.

I intend to put more work into this at some point to allow chords to be bound to keys, maybe allow for key press depth/severity to translate into some kind of analgue input such as a joystick or mouse movement. But for now, this gives me an excuse to USE my midi piano, even if it's not quite for its intended purpose.