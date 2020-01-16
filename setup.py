import os
import imp
from setuptools import setup, find_packages
import io

version = imp.load_source('openl3.version', os.path.join('openl3', 'version.py'))

with io.open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='openl3',
    version=version.version,
    description='Deep audio and image embeddings, based on Look, Listen, and Learn approach',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marl/openl3',
    author='Jason Cramer, Ho-Hsiang Wu, and Justin Salamon',
    author_email='jtcramer@nyu.edu',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['openl3=openl3.cli:main'],
    },
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='deep audio embeddings machine listening learning tensorflow keras',
    project_urls={
        'Source': 'https://github.com/marl/openl3',
        'Tracker': 'https://github.com/marl/openl3/issues',
        'Documentation': 'https://readthedocs.org/projects/openl3/'
    },
    install_requires=[
        'keras>=2.0.9',
        'numpy>=1.13.0',
        'scipy>=0.19.1',
        'kapre>=0.1.4',
        'PySoundFile>=0.9.0.post1',
        'resampy>=0.2.1,<0.3.0',
        'h5py>=2.7.0,<3.0.0',
    ],
    extras_require={
        'docs': [
                'sphinx==1.2.3',  # autodoc was broken in 1.3.1
                'sphinxcontrib-napoleon',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
        'tests': []
    },
    # package_data={
    #     'openl3': weight_files
    # },
)
