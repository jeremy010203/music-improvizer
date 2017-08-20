from mido import MidiFile
import sys, os, pickle

ngrams = {}

def parse_midi_ngram(mid):
    for i, track in enumerate(mid.tracks):
        l = [msg.note for msg in track if msg.type == 'note_on']
        if len(l) > 0:
            for i in range(len(l) - 1):
                if not (l[i], l[i + 1]) in ngrams:
                    ngrams[(l[i], l[i + 1])] = 1
                else:
                    ngrams[(l[i], l[i + 1])] = ngrams[(l[i], l[i + 1])] + 1

nb_files = 0
for root, dirs, files in os.walk(sys.argv[1]):
    path = root.split(os.sep)
    for file in files:
        full_path = os.path.join(root, file)
        if os.path.isfile(full_path):
            nb_files = nb_files + 1

nb_error = 0
count = 0
print("{} files detected...".format(nb_files))
for root, dirs, files in os.walk(sys.argv[1]):
    path = root.split(os.sep)
    for file in files:
        full_path = os.path.join(root, file)
        if os.path.isfile(full_path):
            count = count + 1
            nb_files = nb_files - 1
            print("Still {} files to parse ({} bad files format detected)".format(nb_files, nb_error), end='\r', flush=True)
            try:
                parse_midi_ngram(MidiFile(full_path))
            except Exception as e:
                nb_error = nb_error + 1

            if count % 10000 == 0:
                pickle.dump(ngrams, open("ngrams{}.p".format(count), "wb"))


pickle.dump(ngrams, open("ngrams_final.p".format(count), "wb"))
