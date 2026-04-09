from pathlib import Path
from utils import normalize
import shutil

others_keywork = "others"

def get_image_extensions() -> tuple:
    return 'JPEG', 'PNG', 'JPG', 'SVG'

def get_video_extensions() -> tuple:
    return 'AVI', 'MP4', 'MOV', 'MKV'

def get_doc_extensions() -> tuple:
    return 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'

def get_audio_extensions() -> tuple:
    return 'MP3', 'OGG', 'WAV', 'AMR'

def get_archive_extensions() -> tuple:
    return 'ZIP', 'GZ', 'TAR'


def get_groups() -> dict:
    return {
        **{ext: "images" for ext in get_image_extensions()},
        **{ext: "video" for ext in get_video_extensions()},
        **{ext: "documents" for ext in get_doc_extensions()},
        **{ext: "audio" for ext in get_audio_extensions()},
        **{ext: "archives" for ext in get_archive_extensions()},
        others_keywork: "other"
    }

def get_group_func():
    return {
        "images": process_image,
        "video": process_video,
        "documents": process_doc,
        "audio": process_audio,
        "archives": process_archive,
        "other": process_unknown
    }


def process_archive(file: Path, extension_group: str, root_folder: Path):
    destination = (root_folder.absolute() / extension_group / file.stem)
    print(f"{file.absolute()} -> {destination}/*")
    shutil.unpack_archive(file, destination, file.suffix.replace(".", ""))
    pass

def process_image(file: Path, extension_group: str, root_folder: Path):
    process_basic(**locals())

def process_video(file: Path, extension_group: str, root_folder: Path):
    process_basic(**locals())

def process_doc(file: Path, extension_group: str, root_folder: Path):
    process_basic(**locals())

def process_audio(file: Path, extension_group: str, root_folder: Path):
    process_basic(**locals())

def process_unknown(file: Path, extension_group: str, root_folder: Path):
    process_basic(**locals())

def process_basic(file: Path, extension_group: str, root_folder: Path):
    destination_folder = root_folder.absolute() / extension_group
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination = destination_folder / (normalize(file.stem) + file.suffix)
    print(f"{file.absolute()} -> {destination}")
    file.rename(destination)