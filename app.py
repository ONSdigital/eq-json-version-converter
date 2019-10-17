import os

from app.converter import Converter

if __name__ == '__main__':

    path = 'schemas/to_convert'
    dirs = os.listdir(path)
    converter = Converter()

    for file in dirs:
        converter(file)
