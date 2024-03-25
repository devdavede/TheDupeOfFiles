# The Dupe 👑 of files #
import os
import subprocess
import magic
from PIL import Image

def is_image(file_path):
    mime = magic.Magic(mime=True)
    try:
        file_type = mime.from_file(file_path)
        return file_type.split('/')[0] == 'image'
    except magic.MagicException:
        return False

def is_image_corrupt(file_path):
    if not is_image(file_path):
        return False
    try:
        with Image.open(file_path) as img:
            img.load()
        return False
    except (IOError, OSError):
        return True

def add_labels(file_path):
    finder_script = '''
    tell application "Finder"
        set theFile to POSIX file "%s" as alias
        set label of theFile to "Privat"
    end tell
    ''' % file_path
    subprocess.run(['osascript', '-e', finder_script])
    xattr_command = ['xattr', '-w', 'com.apple.metadata:_kMDItemUserTags', b'6275696C6465723a303030303030303030303065', file_path]
    subprocess.run(xattr_command)

def find_and_tag_corrupt_images(directory):
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if is_image_corrupt(file_path):
                add_labels(file_path)
                print(f"Tagged: {file_path}")

directory = "path/to/your/directory"
find_and_tag_corrupt_images(directory)
