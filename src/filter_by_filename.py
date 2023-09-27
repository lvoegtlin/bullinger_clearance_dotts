from pathlib import Path
import csv

from dot_search import get_gt_lines

if __name__ == '__main__':
    bullinger_path = Path("/HOME/voegtlil/datasets/bullinger-full-ocr")
    filter_result_path = Path("/HOME/voegtlil/datasets/bullinger-full-ocr/test/gt-new-split-old-gt.tsv")
    new_gt_path = Path("/HOME/voegtlil/datasets/bullinger-full-ocr/test/gt.tsv")

    old_gt = get_gt_lines(bullinger_path, split='test')

    new_gt = []
    with new_gt_path.open("r") as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='"')
        new_gt = [(l[0], l[1]) for l in reader]
    new_gt_filename = ["test/" + l[0] for l in new_gt]

    old_gt_filtered = filter(lambda a: a[0] in new_gt_filename, old_gt)
    old_gt_filtered = ((l[0][5:], l[2]) for l in old_gt_filtered)

    with filter_result_path.open('w') as f:
        for l in old_gt_filtered:
            f.write(f"{l[0]}\t{l[1]}\n")

