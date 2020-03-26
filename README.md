# Introduction
This script allows handling the [DanSpeech recordings](https://github.com/Rasmusafj/danspeech_webap) more efficiently. It consists of three steps:
1. Get all .webm files and convert them to .wav files,
1. Retrieve file names and transcripts from db.json Django database dump file,
1. Split all the files into the training set and validation set.

# Requirements
* ffmpeg — [download](https://www.ffmpeg.org/download.html), [brew](https://formulae.brew.sh/formula/ffmpeg)

# How to run
### Example
```shell script
 python3.7 /danspeech_preprocessor/main.py -p ./data -t 0.2 -g mand -a 25
``` 

### Arguments
```shell script
> python3.7 main.py --help                                                                                                      
usage: main.py [-h] [-p PATH] [-g GENDER] [-a AGE] [-t TEST_SIZE]

Preprocessor arguments.

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  the location of directory with raw audio and json
                        files
  -g GENDER, --gender GENDER
                        the gender of the speaker
  -a AGE, --age AGE     the age of the speaker
  -t TEST_SIZE, --validation-size TEST_SIZE
                        the size of the training set
```
