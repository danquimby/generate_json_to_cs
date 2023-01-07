import argparse

from generator import path_source, path_result, run

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='GeneratorCsClass',
        description='generate cs class from json package',
    )
    parser.add_argument('-s', '--source', default=path_source, help='source folder')
    parser.add_argument('-r', '--result', default=path_result, help='result folder')
    args = parser.parse_args()
    run(args.source, args.result)
