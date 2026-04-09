import sys
from pathlib import Path, PosixPath

from sorting import get_groups, others_keywork, get_group_func


def get_provided_directory() -> Path:
    args = sys.argv[1:]
    if not len(args):
        print("No args provided. Please provide dir path")
        sys.exit(1)
    curr_dir = Path(args[0])
    if not curr_dir.exists():
        print("Can't locate provided path")
        sys.exit(1)
    if not curr_dir.is_file():
        print("Provided path is a file. Please provide path to a directory")
        sys.exit(1)
    return curr_dir

def get_files(curr_dir) -> list[PosixPath]:
    result = []
    for f in curr_dir.iterdir():
        if f.is_file():
            result.append(f.absolute())
        else:
            result += get_files(f)
    return result


if __name__ == '__main__':
    current_dir = get_provided_directory()
    groups = get_groups()
    files = get_files(current_dir)
    for current_file in files:
        file_extension = current_file.suffix.replace(".", "").upper()
        extension_group = groups.get(file_extension, groups.get(others_keywork))
        get_group_func().get(extension_group)(current_file, extension_group, current_dir)


