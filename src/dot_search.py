from pathlib import Path
import csv
from typing import List, Tuple
from PIL import Image
import matplotlib.pyplot as plt


def check_dots_inline(lines: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
    # search for points and look if afterwards is captial if not write into name and gt into list
    not_captial_after_dot = []
    exceptions = ['"', '.']
    for path_gt in lines:
        line = path_gt[2]
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

        if next_letter.isupper() or next_letter in exceptions or next_letter.isnumeric():
            continue
        not_captial_after_dot.append(path_gt)

    return not_captial_after_dot


def get_gt_lines(path: Path, split: str) -> List[Tuple[str, str, str]]:
    lines = []
    if split != "test":
        with (path / split / 'gt-full.tsv').open('r', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='"')
            lines.extend([(Path(split) / r[0], r[0], r[1]) for r in reader])
    else:
        for s in ['frequent', 'non_frequent']:
            with (path / 'test' / s / 'gt-full.tsv').open('r', encoding="utf-8") as f:
                reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='"')
                lines.extend([(str(Path('test') / s / r[0]), r[0], r[1]) for r in reader])

    return lines


def show(path: str):
    with open(path, mode='rb') as f:
        img = Image.open(f)
        plt.imshow(img)
        plt.show()


def _save_month_captialization(samples: List[Tuple[str, str, str]], word_to_check_list: List[str], output_path: Path,
                               split: str):
    to_check = []
    for gt_line in samples:
        for word in word_to_check_list:
            if word.lower() in gt_line[2]:
                to_check.append(gt_line[1] + "\n")
    print(f'{len(to_check)=} from {split}')
    with (output_path / f"changed_gt_{split}.txt").open("w") as f:
        f.writelines(to_check)


def _save_candidates(samples: List[Tuple[str, str, str]], output_path: Path, split: str):
    candidates = check_dots_inline(samples)
    print(f'{len(samples)=} from {split}')
    with (output_path / f"candidates_gt_{split}.txt").open("w") as f:
        f.writelines([s[0] + "\t" + s[2] + '\n' for s in candidates])


if __name__ == '__main__':
    bullinger_path = Path("/HOME/voegtlil/datasets/bullinger-full-ocr")
    write_capitals_path = Path("write_captial.txt").absolute()
    output_folder = Path("../anna/").absolute()

    gt_lines_train = get_gt_lines(bullinger_path, split='train')
    gt_lines_validation = get_gt_lines(bullinger_path, split='validation')
    gt_lines_test = get_gt_lines(bullinger_path, split='test')

    # res = iter(check_dots_inline(gt_lines_test))
    #
    # elem = next(res)
    # print(elem[1])
    # print(elem[2])
    # show(elem[0])

    # create a txt file with the file names (folder/language/filename) of test and train/validation
    captial_list = []
    with write_capitals_path.open('r') as f:
        for line in f.readlines():
            captial_list.append(line.replace("\n", ""))

    _save_month_captialization(samples=gt_lines_test, word_to_check_list=captial_list, output_path=output_folder,
                               split='test')
    _save_month_captialization(samples=gt_lines_train, word_to_check_list=captial_list, output_path=output_folder,
                               split='train')
    _save_month_captialization(samples=gt_lines_validation, word_to_check_list=captial_list, output_path=output_folder,
                               split='validation')

    # _save_candidates(samples=gt_lines_train, output_path=output_folder, split='train')
    # _save_candidates(samples=gt_lines_validation, output_path=output_folder, split='validation')
    # _save_candidates(samples=gt_lines_test, output_path=output_folder, split='test')
