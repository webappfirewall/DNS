import socket
import urllib.parse
import threading
from pymongo import MongoClient

b1 = bytearray(b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00')
b2 = bytearray(b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xff\x00\x04')


def analyzeRqt(conn, addr):
    usr = urllib.parse.quote_plus('@dm1n')
    pwd = urllib.parse.quote_plus('Qw3rt&.12345')
    client = MongoClient('mongodb://%s:%s@192.168.17.146' % (usr, pwd))
    db = client['waf']
    collection = db['sites']

    with conn:
        data = conn.recv(1024)
        id = data[2:4]
        query = data[14:]

        url = extractURL(query)
        print('URL: ', url)

        doc = collection.find_one({"url": url})

        if doc is not None:
            response = bytearray()
            length = bytearray(b'\x00')
            print(len(b1))
            print(len(b2))
            print(len(query))
            size = len(b1) + len(b2) + len(query) + 4
            print(size)
            length.append(size)

            ip = doc['ip'].split('.')

            for byte in length:
                response.append(byte)
            for byte in id:
                response.append(byte)
            for byte in b1:
                response.append(byte)
            for byte in query:
                response.append(byte)
            for byte in b2:
                response.append(byte)
            for byte in ip:
                response.append(int(byte))

            conn.sendall(response)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp2:
                s_tcp2.connect(('8.8.8.8', 53))
                s_tcp2.sendall(data)
                data2 = s_tcp2.recv(1024)
                s_tcp2.sendall(data2)
        url = ''


def extractURL(query):
    url = ''
    i = 0

    for c in query:
        if i == 0:
            pos = c + 1
        elif i == pos:
            url += '.'
            pos = c + i + 1
        elif c == 0:
            break
        elif chr(c).isalpha():
            url += chr(c)
        i += 1

    return url[:-3]


def initDNS():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp:
        s_tcp.bind(('192.168.17.147', 53))
        s_tcp.listen()

        print("***** DNS Server *****")
        while True:
            conn, addr = s_tcp.accept()
            t = threading.Thread(target=analyzeRqt, args=(conn, addr))
            t.start()
            t.join()


if __name__ == '__main__':
    initDNS()
