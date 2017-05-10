from mutagen.easyid3 import EasyID3
from pathlib import Path
from tkinter.filedialog import askdirectory
import re, os, asyncio

REGEXP = r'(\S+)(\d{2,3})(?:\S+)(.mp3)$'
GROUPS = r'\1\2\3'
SOURCE = '/Users/gniu/dd'

SHOW_DIALOG = True

TAG_INFO = {'genre': '', 'date': '', 'composer': '', 'albumartist': 'yekki', 'artist': '周建龙'}


async def attach_tag(path, regex=None):
    if os.path.isfile(path):
        new_path = path
        if regex:
            new_path = Path(path.parent) / re.sub(REGEXP, GROUPS, path.name)
            path.rename(new_path)

        audio = EasyID3(str(new_path))
        audio['title'] = new_path.stem
        audio['album'] = new_path.parent.parts[-1]
        audio['composer'] = TAG_INFO.get('composer', '')
        audio['artist'] = TAG_INFO.get('artist', '')
        audio['genre'] = TAG_INFO.get('genre', '')
        audio['date'] = TAG_INFO.get('date', '')
        audio['albumartist'] = TAG_INFO.get('albumartist', '')
        audio.save()


def main():
    dir = askdirectory() if SHOW_DIALOG else SOURCE
    files = [f for f in Path(dir).glob('**/*.mp3') if f.is_file()]
    tasks = [asyncio.ensure_future(attach_tag(f)) for f in files]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    print(f'Finished to attach tags on {len(tasks)} files.')


if __name__ == '__main__':
    main()