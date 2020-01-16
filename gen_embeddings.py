# -*- coding: utf-8 -*-
import os
import glob
import sys
import io

import numpy as np
import openl3 as l3
import soundfile as sdf

model_dir = sys.argv[1]
data_dir = sys.argv[2]
out_file = sys.argv[3]
secs = int(sys.argv[4])
hop_size = float(sys.argv[5])

# python gen_embeddings.py ../data/openl3/pretrained_models/ tests/data/audio/chirp_44k.wav audio_embeds.txt 5 0.5
if __name__ == '__main__':
    files = glob.glob(data_dir)
    with io.open(out_file, 'w+', encoding='utf-8') as fout:
        for fn in files:
            print(fn)
            audio_data, samplerate = sdf.read(fn)
            embeds, _ = l3.get_embedding(audio_data, samplerate, model_dir=model_dir,
                                         input_repr='mel256', content_type='music',
                                         embedding_size=6144, hop_size=hop_size)
            embed = np.mean(embeds[:int(secs/hop_size)], axis=0)

            fn = fn.split("/")[-1]
            fout.write(fn + ' ' + ' '.join('%.3f' % v for v in embed) + '\n')
