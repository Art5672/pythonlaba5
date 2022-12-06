import socket
import os
import pathlib
import threading

BASE_DIR = pathlib.Path(__file__).parent.resolve()
HOST = 'localhost'
PORT = 8081
SIZE = 1024
UTF8 = 'utf-8'
UPLOAD = 'upload'
DOWNLOAD = 'download'


def sends_file(filename):
    sock = socket.socket()
    sock.connect((HOST, PORT))

    try:
        sock.sendall(f'{UPLOAD}: {filename}\r\n'.encode(UTF8))

        if sock.recv(SIZE) == b'filename received':
            path = os.path.join(BASE_DIR, 'test_files', filename)
            with open(path, 'rb') as f:
                data = f.read(SIZE)
                while data:
                    data = f.read(SIZE)
    finally:
        print('Finished.')
        sock.close()


def downloads_file(filename):
    sock = socket.socket()
    sock.connect((HOST, PORT))

    try:
        sock.sendall(f'{DOWNLOAD}: {filename}\r\n'.encode(UTF8))

        if sock.recv(SIZE) == b'filename received':
            path = os.path.join(BASE_DIR, 'downloaded', filename)
            with open(path, 'ab') as f:
                data = sock.recv(SIZE)
                while data:
                    f.write(data)
                    data = sock.recv(SIZE)
    finally:
        print('Finished.')
        sock.close()


def sends_files():
    filename1 = 'photo1.jpg'
    filename2 = 'photo2.jpg'
    th1 = threading.Thread(target=sends_file, args=(filename1,))
    th2 = threading.Thread(target=sends_file, args=(filename2,))

    th1.start()
    th2.start()

    th1.join()
    th2.join()


def downloads_files():
    filename1 = 'photo1.jpg'
    filename2 = 'photo2.jpg'
    thread1 = threading.Thread(target=downloads_file, args=(filename1,))
    thread2 = threading.Thread(target=downloads_file, args=(filename2,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


if __name__ == '__main__':
    sends_files()
    downloads_files()
