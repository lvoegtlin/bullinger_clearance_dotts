from pathlib import Path
import csv
import re

if __name__ == '__main__':
    bullinger_path = Path("/HOME/voegtlil/datasets/bullinger-full-ocr")

    splits = ['train', 'validation']
    writers = ['frequent', 'non_frequent']

    gt_lines = []
    for split in splits:
        with (bullinger_path / split / 'gt.tsv').open('r') as f:
            reader = csv.reader(f, delimiter='\t')
            gt_lines.extend([r for r in reader])

    for s in ['frequent', 'non_frequent']:
        with (bullinger_path / 'test' / s / 'gt.tsv').open('r') as f:
            reader = csv.reader(f, delimiter='\t')
            gt_lines.extend([r for r in reader])
    print(gt_lines)

    # search for points and look if afterwards is captial if not write into name and gt into list
    not_captial_after_dot = []
    exceptions = ['"', '.']

    for path_gt in gt_lines:
        line = path_gt[1]
        line = line.strip()
        try:
            idx = line.index('.')
        except ValueError:
            continue
        if idx + 1 == len(line):
            continue
        next_letter = ""
        i = 1

        while line[idx + i] == ' ':
            i = i + 1
        else:
            next_letter = line[idx + i]

        if next_letter.isupper() or next_letter in exceptions:
            continue
        not_captial_after_dot.append(path_gt)
