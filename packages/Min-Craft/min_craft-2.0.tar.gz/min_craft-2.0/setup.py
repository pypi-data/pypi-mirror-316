from setuptools import setup, find_packages

setup(
    name='Min-Craft',
    version='2.0',
    author='Bowser2077',
    author_email='no@gmail.com',
    description='Say E, You Die.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bowser-2077/MIN-CRAFT/',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition>=3.12.0',
        'mcrcon>=0.7.0',
        'PyAudio>=0.2.14'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
