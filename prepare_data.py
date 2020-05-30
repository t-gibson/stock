import argparse
import csv
import os
import re

parser = argparse.ArgumentParser(description="Process Southpark data")
parser.add_argument("input_csv", type=str, help="The raw input CSV")
parser.add_argument("output_csv", type=str, help="The location to store the processed file")


def read_data(input_csv: str, output_csv: str) -> None:
    """
    Read in the `input_csv` file of the southpark scripts,
    cleans input, and writes the result to `output_csv`.
    The resulting rows have format `name! line`.

    The `input_csv` is expecting a file with the same structure as
    the `All-seasons.csv`.
    """
    _min_sent_len = 3
    _max_sent_len = 64
    punct_chars = ['!', '.', '?', '։', '؟', '۔', '܀', '܁', '܂', '‼', '‽', '⁇', '⁈', '⁉', '⸮', '﹖', '﹗',
                   '！', '．', '？', '｡', '。']
    _slit_pat = re.compile('([{0}])+([^{0}])'.format(''.join(punct_chars)))
    _replace_pat = re.compile('{}'.format(punct_chars))

    doc_list = []
    character_set = set()
    with open(input_csv, 'r') as f:
        f_h = csv.reader(f)
        for _idx, l in enumerate(f_h, start=1):
            _, _, name, line = l
            line = line.strip('"')
            sents_str = _slit_pat.sub(r'\1\n\2', '{}\n'.format(line))
            sents_str = sents_str.rstrip('\n')
            sents = [s.strip() for s in sents_str.split('\n') if _min_sent_len <= len(s.strip()) <= _max_sent_len]
            character_set.add(name)
            name = _replace_pat.sub(r'', name)
            for s in sents:
                doc_list.append('{}! {}'.format(name, s))
    doc_list = list(frozenset(doc_list))
    print('num characters: {}'.format(len(character_set)))
    print('documents: {}'.format(len(doc_list)))
    with open(output_csv, 'w') as f:
        f.write('\n'.join(doc_list))


if __name__ == '__main__':
    args = parser.parse_args()
    read_data(args.input_csv, args.output_csv)