import json
import os
from os import walk
from os.path import join

tmp_csharp = """using UnityEngine;

[System.Serializable]
public class %s
{
%s
}
"""

tmp_python = """from pydantic import BaseModel, Field


class %s(BaseModel):
%s
"""

"""
class UserModel(BaseModel):
    username: str = Field('user', example='')
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


def _save(data: str, filename: str, path_folder_result):
    with open(join(path_folder_result, filename), 'w') as f:
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
    return tmp_csharp % (class_name, ''.join(lines))

def generate_python(data: dict, filename: str):
    # %s: %s = Field('%s', example='%s')
    class_name = f'{filename.split(".")[0].capitalize()}Model'
    lines = []
    for k, v in data.items():
        t = 'None'
        if isinstance(v, int):
            t = 'int'
        elif isinstance(v, float):
            t = 'float'
        elif isinstance(v, str):
            t = 'str'
        lines.append(f"\t{k}: {t} = Field('{v}')\n")
    # remove last character
    lines[-1] = lines[-1][:-1]
    return tmp_python % (class_name, ''.join(lines))


def run(source_folder: str, result_folder: str):
    for file, data in gen_data(get_source_files(source_folder)):
        generate_cs_class = generate_csharp(data, file)
        _save(generate_cs_class, f"{file.split('.')[0]}_model.cs", result_folder)
        generate_py_class = generate_python(data, file)
        _save(generate_py_class, f"{file.split('.')[0]}_model.py", result_folder)
