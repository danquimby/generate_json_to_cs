import json
import os
from os import walk
from os.path import join

tmp = """using UnityEngine;

[System.Serializable]
public class %s
{
%s
}
"""

path_dir = os.path.abspath(os.path.dirname(__file__))
path_source = join(path_dir, 'source')
path_result = join(path_dir, 'result')


def get_source_files(path_source):
    return next(walk(path_source), (None, None, []))[2]


def gen_data(files: str):
    for file in files:
        with open(join(path_source, file)) as f:
            yield (file, json.loads(f.read()))


def save_csharp(data: str, filename: str, path_folder_result):
    cs_filename = f"{filename.split('.')[0]}_model.cs"
    with open(join(path_folder_result, cs_filename), 'w') as f:
        f.write(data)


def generate_csharp(data: dict, filename: str):
    class_name = f'{filename.split(".")[0].capitalize()}Model'
    lines = []
    for k, v in data.items():
        t = ''
        if isinstance(v, int):
            t = 'int'
        elif isinstance(v, float):
            t = 'float'
        elif isinstance(v, str):
            t = 'string'

        lines.append(f'\tpublic {t} {k}; //example {v} \n')
    # remove last character
    lines[-1] = lines[-1][:-1]
    return tmp % (class_name, ''.join(lines))


def run(source_folder: str, result_folder: str):
    for file, data in gen_data(get_source_files(source_folder)):
        get_class = generate_csharp(data, file)
        save_csharp(get_class, file, result_folder)
