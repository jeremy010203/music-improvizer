import pickle
from mido import Message, MidiFile, MidiTrack
import random
import numpy

ngrams = pickle.load(open("ngrams_final.p", "rb"))
cur_note = -1

def add_note(track, note):
    track.append(Message('note_on', note=note, velocity=64, time=64))
    track.append(Message('note_off', note=note, velocity=64, time=64))

def get_next_note(track):
    global cur_note
    if cur_note == -1:
        cur_note = random.randint(1, 127)
        add_note(track, cur_note)
    else:
        notes = [msg for msg in list(ngrams.items()) if msg[0][0] == cur_note]
        notes = sorted(notes, key=lambda x: x[1], reverse=True)
        s = sum([val[1] for val in notes])
        notes = [(val[0][1], val[1]/s) for val in notes]
        cur_note = numpy.random.choice([val[0] for val in notes], p=[val[1] for val in notes])
        add_note(track, cur_note)

mid = MidiFile()
mid.type = 0
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=0, time=0))
for i in range(100):
    get_next_note(track)

mid.save('new_song.mid')
