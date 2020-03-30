import glob
import json
import os
import shutil
import subprocess
from pathlib import Path


class Preprocessor:
    def __init__(self, local_path):
        self.path = local_path

    def convert_files(self):
        path = os.path.join(self.path.replace(' ', r'\ '), '*.webm')
        command = 'for file in {}; do ffmpeg -y -i "$file" -acodec pcm_s16le -ac 1 -ar 16000 -f wav "$file.wav"; done'.format(path)

        subprocess.call(command, shell=True)

        files = glob.glob(os.path.join(self.path, '*.webm.wav'))

        for file in files:
            os.rename(file, file.replace('.webm', ''))

    def parse_json_to_csv(self, gender, age):
        # @author: tuethomsen28

        with open(os.path.join(self.path, 'db.json')) as json_file:
            data = json.load(json_file)

        with open(os.path.join(self.path, 'overview.csv'), 'w', newline='') as csv_file:
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
        with open(os.path.join(self.path, 'overview.csv'), 'r') as overview_file:
            lines = overview_file.readlines()
            test_size = int((len(lines) - 1) * test_size)

            self.__create_split_directory('validation', lines[-test_size:])
            self.__create_split_directory('training', lines[1:-test_size])

    def __create_split_directory(self, directory, lines):
        try:
            shutil.rmtree(os.path.join(self.path, directory))
        except FileNotFoundError:
            pass

        Path(os.path.join(self.path, directory)).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(self.path, directory, '{}.csv'.format(directory)), 'w') as file:
            file.write('file,trans,gender,age\n')

            for line in lines:
                file.write(line)

                old_path = os.path.join(self.path, line.split(',')[0])
                new_path = os.path.join(self.path, directory, line.split(',')[0])
                os.rename(old_path, new_path)
