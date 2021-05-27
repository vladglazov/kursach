from telethon.sync import TelegramClient
from telethon import events
from telethon import types
import threading
import tempfile
import asyncio
import os

tmppath = '{}/{}'.format(tempfile.gettempdir(), 'vk_DB_bot')
tmppath_download = '{}/{}'.format(tmppath, 'download')
media = []

if not os.path.exists(tmppath_download):
    if not os.path.exists(tmppath):
        os.mkdir(tmppath)
    os.mkdir(tmppath_download)
secret_data = [line.rstrip('\n') for line in open('api_id_hash.secret')]
(api_id, api_hash) = (int(secret_data[0]), secret_data[1])


def download_media(client: TelegramClient, message: types.Message):
    def bytes_to_string(byte_count):
        """Converts a byte count to a string (in KB, MB...)"""
        suffix_index = 0
        while byte_count >= 1024:
            byte_count /= 1024
            suffix_index += 1

        return '{:.2f}{}'.format(
            byte_count, [' bytes', 'KB', 'MB', 'GB', 'TB'][suffix_index]
        )

    def download_progress_callback(downloaded_bytes, total_bytes):
        print_progress(
            'Downloaded', downloaded_bytes, total_bytes
        )

    def print_progress(progress_type, downloaded_bytes, total_bytes):
        print('\r{} {} out of {} ({:.2%})  '.format(
            progress_type, bytes_to_string(downloaded_bytes),
            bytes_to_string(total_bytes), downloaded_bytes / total_bytes), end='', flush=True
        )

    if message.file:
        print('save...')
        path = message.download_media('{}/download'.format(tmppath), progress_callback=download_progress_callback)
        newpath = path.replace('/download', '')
        os.rename(path, newpath)
        print('\nFile saved to', newpath)  # printed after download is done
        return newpath
    else:
        print('not file')
        return None


def getFileIterator():
    print('iintend')
    with TelegramClient('iintend', api_id, api_hash) as client_iintend:
        for message in client_iintend.iter_messages('vk_DB_bot'):
            print('iintend', message.id, message.text, message.chat.title)
            if message.file:
                path = download_media(client_iintend, message)
                if path is not None:
                    yield path
                    os.remove(path)


def main():
    for file in getFileIterator():
        print('ok:', file)
    else:
        print('bad')


if __name__ == '__main__':
    main()
