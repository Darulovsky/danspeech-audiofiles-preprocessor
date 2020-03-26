import argparse
import os

from preprocessor.preprocessor import Preprocessor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocessor arguments.')
    path = os.getcwd()
    parser.add_argument('-p', '--path', dest='path', default='data',
                        help='the location of directory with raw audio and json files', type=str)
    parser.add_argument('-g', '--gender', dest='gender', default='mand',
                        help='the gender of the speaker')
    parser.add_argument('-a', '--age', dest='age', default=25,
                        help='the age of the speaker', type=int)
    parser.add_argument('-t', '--validation-size', dest='test_size', default=0.33,
                        help='the size of the training set', type=float)

    args = parser.parse_args()

    preprocessor = Preprocessor('{}/{}'.format(path, args.path))
    preprocessor.convert_files()
    preprocessor.parse_json_to_csv(args.gender, args.age)
    preprocessor.split_set(args.test_size)