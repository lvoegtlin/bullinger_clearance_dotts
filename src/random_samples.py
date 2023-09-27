import csv
from pathlib import Path
import numpy as np

if __name__ == '__main__':
    path_full = Path('/HOME/voegtlil/datasets/bullinger-full-ocr/train/gt-full.tsv')
    path_random = Path('/HOME/voegtlil/datasets/bullinger-full-ocr/train/random.tsv')

    gt_lines = []
    with path_full.open('r') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='"')
        gt_lines = list(reader)

    random = np.random.choice(np.arange(0, 109627), size=89285, replace=False)

    with path_random.open('w') as f:
        for l in np.asarray(gt_lines)[random]:
            f.write(f'{l[0]}\t{l[1]}\n')
