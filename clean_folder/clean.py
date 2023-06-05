import platform
import sys
from pathlib import Path
import shutil
import re


def main():
    # Get folder name from second command-line argument
    full_path = " ".join(sys.argv[1:])
    print("full_path", full_path)
    # Verify operating system
    if platform.system() == "Windows":
        if len(full_path.split(":")[0]) > 1:
            # Get current working directory
            current_dir = Path.cwd()
            # Create full path
            full_path = current_dir / full_path

    unrem_dir = dict(images=['JPEG', 'PNG', 'JPG', 'SVG'], documents=['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                     audio=['MP3', 'OGG', 'WAV', 'AMR'], video=['AVI', 'MP4', 'MOV', 'MKV'],
                     archives=['ZIP', 'GZ', 'TAR'],
                     unknown='')

    #############################################
    # Make dict for translate
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    trans = {}

    for c, t in zip(cyrillic_symbols, translation):
        trans[ord(c)] = t
        trans[ord(c.upper())] = t.upper()

    def normalize(name):
        name = re.sub(r'\W', "_", name)
        return name.translate(trans)

    ##############################################
    # Get path and create new folders for files
    print(full_path)
    p = Path(full_path)
    for k, v in unrem_dir.items():
        try:
            new_dir = p / k
            new_dir.mkdir()
        except FileExistsError:
            print(f"{p / k} already exists")
        for j in v:
            try:
                new_format = p / k / j.lower()
                new_format.mkdir()
            except FileExistsError:
                print(f"{p / k / j.lower()} already exists")

    ###############################################

    def start_iter(p):
        for i in p.iterdir():
            # we start if the file or folder is not named as one of the unrem_dir keys
            # or file location is not as a full_path
            if i.name not in unrem_dir.keys() or full_path != i.resolve():
                # if the selected item is a file, we start with that file
                if i.is_file():
                    suf = i.suffix
                    file_name = i.name[:-len(suf)]

                    for k, v in unrem_dir.items():
                        # if we find a file with a suffix like in unrem_dir, we move that file
                        if suf[1:].upper() in v:
                            # if the file is an archive - unpack this file then delete the archive
                            # after found, interrupt this iteration and start a new one
                            if k == "archives":
                                shutil.unpack_archive(i, f"{full_path}/{k}/{suf[1:].upper()}/{normalize(file_name)}")
                                i.unlink()
                                break
                            else:
                                # print(f"{folder_path}\\{k}\\{suf[1:].upper()}\\{normalize(file_name)}{suf}")
                                shutil.move(i, f"{full_path}/{k}/{suf[1:].upper()}/{normalize(file_name)}{suf}")
                                break

                    else:
                        # print(f"{folder_path}\\unknown\\{normalize(file_name)}{suf}")
                        shutil.move(i, f"{full_path}/unknown/{normalize(file_name)}{suf}")

                else:
                    if i.iterdir():
                        start_iter(i)
                    else:
                        i.rmdir()

    def delete_empty_folders(p):
        for i in p.iterdir():
            if i.is_dir():
                delete_empty_folders(i)
                try:
                    i.rmdir()
                except OSError:
                    # Skip if the folder is not empty
                    continue

    start_iter(p)
    delete_empty_folders(p)

if __name__ == '__main__':
    main()
