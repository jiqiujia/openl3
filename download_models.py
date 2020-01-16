# -*- coding: utf-8 -*-
import urllib
from itertools import product
import os
import sys
import gzip

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

proxy = urllib.request.ProxyHandler({'http': 'dev-proxy.oa.com:8080', 'https': 'dev-proxy.oa.com:8080'})
# construct a new opener using your proxy settings
opener = urllib.request.build_opener(proxy)
# install the openen on the module-level
urllib.request.install_opener(opener)

module_dir = 'pretrained_models'
modalities = ['audio', 'image']
input_reprs = ['linear', 'mel128', 'mel256']
content_type = ['music', 'env']
model_version_str = 'v0_2_0'
weight_files = ['openl3_{}_{}_{}.h5'.format(*tup)
                for tup in product(modalities, input_reprs, content_type)]
base_url = 'https://github.com/marl/openl3/raw/models/'

if len(sys.argv) > 1 and sys.argv[1] == 'sdist':
    # exclude the weight files in sdist
    weight_files = []
else:
    # in all other cases, decompress the weights file if necessary
    for weight_file in weight_files:
        weight_path = os.path.join(module_dir, weight_file)
        if not os.path.isfile(weight_path):
            weight_fname = os.path.splitext(weight_file)[0]
            compressed_file = '{}-{}.h5.gz'.format(weight_fname, model_version_str)
            compressed_path = os.path.join(module_dir, compressed_file)
            if not os.path.isfile(compressed_file):
                print('Downloading weight file {} ...'.format(compressed_file))
                urlretrieve(base_url + compressed_file, compressed_path)
            print('Decompressing ...')
            with gzip.open(compressed_path, 'rb') as source:
                with open(weight_path, 'wb') as target:
                    target.write(source.read())
            print('Decompression complete')
            os.remove(compressed_path)
            print('Removing compressed file')