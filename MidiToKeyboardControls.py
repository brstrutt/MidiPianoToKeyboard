import DirectXOutput
import pygame
import pygame.midi
import time
from pathlib import Path
from numpy import empty
from pandas import read_table, isnull
from pynput.keyboard import Key, Controller

def device_selection():
    print(pygame.midi.get_count(), " midi input devices found.")
    id = int(pygame.midi.get_default_input_id())
    if id not in range(pygame.midi.get_count()):
        print("Default input ID not in pygame midi device list")

    print("Use Midi Device:", id)

    return id

def profile_selection():
    print('Profiles: ')

    entries = Path('profiles')

    nfiles = 0
    for entry in entries.iterdir():
        nfiles = nfiles + 1

    files = empty(nfiles, dtype = 'object')

    n = 0
    for entry in entries.iterdir():
        files[n] = entry.name
        print(n, entry.name)
        n = n + 1

    print("Picking the alphabetically FIRST entry because im lazy")
    profile = 0

    print("Chosen profile: ", files[profile])

    if not profile in range(n):
        print("No Profiles? Woe is me.")

    raw_profile = read_table('profiles/' + files[profile], header = 0, usecols = [1], comment = '/')
    lst = [''] * len(raw_profile.index)

    print(raw_profile)
    print(len(lst))

    for n in range(0, len(raw_profile.index)):
        if isnull(raw_profile.iloc[n][0]) is True:
            lst[n] = ''
        else:
            lst[n] = raw_profile.iloc[n][0]
    return lst

def create_togglelist(size):
    list = empty(size, dtype = 'bool')

    for n in range(0, size):
        list[n] = False

    return list

pygame.midi.init()

for n in range(pygame.midi.get_count()):
    print("Device ", n, ".......", pygame.midi.get_device_info(n))

try:
    device = pygame.midi.Input(device_selection())
except:
    print("Device selection failed.")

output = pygame.midi.Output(pygame.midi.get_default_output_id())

profile = profile_selection()

toggleList = create_togglelist(len(profile))

print("Detecting Inputs")

note_nr = 0
output.set_instrument(0)

note_offset = 36 # Offset the notes so I can start text files at the left of my keyboard
while True:
    if device.poll():
        event = device.read(1)[0]
        data = event[0]
        note_nr = data[1]
        velocity = data[2]

        if note_nr != 0:
            note_nr = note_nr - note_offset

            toggleList[note_nr] = not toggleList[note_nr]

            if(toggleList[note_nr]):
                output.note_on(note_nr + note_offset, velocity)
                if not profile[note_nr] == '':
                    DirectXOutput.PressKey(profile[note_nr])

            if not toggleList[note_nr]:
                output.note_off(note_nr + note_offset)
                if not profile[note_nr] == '':
                    DirectXOutput.ReleaseKey(profile[note_nr])

