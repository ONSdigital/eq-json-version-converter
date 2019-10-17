import os

from app.converter import Converter

if __name__ == '__main__':

    path = 'schemas/to_convert'
    dirs = os.listdir(path)

    for file in dirs:
        schema_to_convert = Converter(file)
        schema_to_convert.convert_schema()
        schema_to_convert.save_json()
