from setuptools import setup, find_packages

setup(
    name='simple-transcription',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'SpeechRecognition',
        'deep-translator'
    ],
    entry_points={
        'console_scripts': [
            'simple-transcription=simple_transcription.simple_transcription:trascrivi_e_traduci',
        ],
    },
)
