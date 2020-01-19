# -*- coding: utf-8 -*-
import os
import glob
import sys
import io

import numpy as np
import openl3 as l3
import soundfile as sdf
import librosa

import multiprocessing as mp

model_dir = sys.argv[1]
data_dir = sys.argv[2]
out_file = sys.argv[3]
secs = int(sys.argv[4])
hop_size = float(sys.argv[5])
shard_num = int(sys.argv[6])
processed_file_name = sys.argv[7]


def monkeyfix_glib():
    """
    Fixes some stupid bugs such that SIGINT is not working.
    This is used by audioread, and indirectly by librosa for loading audio.
    https://stackoverflow.com/questions/16410852/
    """
    try:
        import gi
    except ImportError:
        return
    try:
        from gi.repository import GLib
    except ImportError:
        from gi.overrides import GLib
    # Do nothing.
    # The original behavior would install a SIGINT handler which calls GLib.MainLoop.quit(),
    # and then reraise a KeyboardInterrupt in that thread.
    # However, we want and expect to get the KeyboardInterrupt in the main thread.
    GLib.MainLoop.__init__ = lambda *args, **kwargs: None


def monkeypatch_audioread():
    """
    audioread does not behave optimal in some cases.
    E.g. each call to _ca_available() takes quite long because of the ctypes.util.find_library usage.
    We will patch this.
    """
    try:
        import audioread
    except ImportError:
        return
    res = audioread._ca_available()
    audioread._ca_available = lambda: res

monkeyfix_glib()
monkeypatch_audioread()

def readAudio(files):
    for fn in files:
        yield sdf.read(fn)

input_repr = 'mel256'
content_type='music'
embedding_size=6144

# python gen_embeddings.py ../data/openl3/pretrained_models/ tests/data/audio/*.wav audio_embeds.txt 5 0.5 2
if __name__ == '__main__':

    processed_files = set()
    # with io.open(processed_file_name, encoding='utf-8') as fin:
    #     for fn in fin:
    #         processed_files.add(fn.strip())

    files = glob.glob(data_dir)
    file_num = len(files)
    # print(f"file num {file_num}")
    segs = np.linspace(0, file_num, shard_num + 1, dtype=np.int32)
    print(segs)
    cnt = 0

    model = l3.load_embedding_model(input_repr, content_type, embedding_size, model_dir)

    for i in range(shard_num):
        with io.open(out_file + "_" + str(i), 'w+', encoding='utf-8') as fout, \
                io.open(processed_file_name, 'a+', encoding='utf-8') as fout2:
            part_files = files[segs[i]: segs[i + 1]]
            file_idx = 0
            # for audio_data, samplerate in readAudio(part_files):
            #    fn = part_files[file_idx]
            for fn in part_files:
                audio_data, samplerate = librosa.load(fn)  # sdf.read(fn)
                file_idx += 1
                tmp = fn.split("/")[-1]
                print('file %d: %s' % (cnt, tmp))
                if tmp in processed_files:
                    continue
                embeds, _ = l3.get_embedding(audio_data, samplerate, model=model, hop_size=hop_size)
                embed = np.mean(embeds[:int(secs / hop_size)], axis=0)

                # fout.write(tmp + ' ' + ' '.join('%.3f' % v for v in embed) + '\n')
                # fout2.write(tmp + '\n')
                cnt += 1
