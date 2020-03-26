import glob
import json
import os
import shutil
import subprocess
from pathlib import Path


class Preprocessor:
    def __init__(self, local_path):
        self.path = local_path
        self.sets = {}

    def convert_files(self):
        command = 'for file in "{}"/*.webm; do ffmpeg -y -i "$file" -acodec pcm_s16le -ac 1 -ar 16000 -f wav "$file.wav"; done'.format(self.path)
        subprocess.call(command, shell=True)

        files = glob.glob('{}/*.webm.wav'.format(self.path))

        for file in files:
            os.rename(file, file.replace('.webm', ''))

    def parse_json_to_csv(self, gender, age):
        # @author: tuethomsen28

        with open('{}/db.json'.format(self.path)) as json_file:
            data = json.load(json_file)

        with open('{}/overview.csv'.format(self.path), 'w', newline='') as csv_file:
            csv_file.write('file,trans,gender,age\n')
            for j in data:
                try:
                    file = j['fields']['recorded_file'][:-5] + '.wav'
                    transcription = j['fields']['transcription']
                    line = ','.join(map(str, [file, transcription, gender, age]))
                    line = '{}\n'.format(line)
                    csv_file.write(line)

                except KeyError:
                    pass

    def split_set(self, test_size):
        with open('{}/overview.csv'.format(self.path), 'r') as overview_file:
            lines = overview_file.readlines()
            test_size = int((len(lines) - 1) * test_size)

            self.__create_split_directory('validation', lines[-test_size:])
            self.__create_split_directory('training', lines[1:-test_size])

    def __create_split_directory(self, directory, lines):
        try:
            shutil.rmtree('{}/{}'.format(self.path, directory))
        except FileNotFoundError:
            pass

        Path('{}/{}'.format(self.path, directory)).mkdir(parents=True, exist_ok=True)

        with open('{0}/{1}/{1}.csv'.format(self.path, directory), 'w') as file:
            file.write('file,trans,gender,age\n')

            for line in lines:
                file.write(line)

                old_path = '{}/{}'.format(self.path, line.split(',')[0])
                new_path = '{}/{}/{}'.format(self.path, directory, line.split(',')[0])
                os.rename(old_path, new_path)
