import socket
import urllib.parse
import threading
from pymongo import MongoClient


def analyzeRqt(conn, addr):
    with conn:
        data = conn.recv(1024)

        usr = urllib.parse.quote_plus('@dm1n')
        pwd = urllib.parse.quote_plus('Qw3rt&.12345')
        client = MongoClient('mongodb://%s:%s@192.168.17.146' % (usr, pwd))
        # client = MongoClient('mongodb://localhost:27017')
        db = client['waf']
        collection = db['sites']

        response = bytearray()

        id = data[:2]
        query = data[12:]

        url = extractURL(query)
        print('URL: ', url)

        doc = collection.find_one({"url": url})

        if doc is not None:
            for i in id:
                response.append(i)
            response.append(129)
            response.append(128)
            response.append(0)
            response.append(1)
            response.append(0)
            response.append(1)
            response.append(0)
            response.append(0)
            response.append(0)
            response.append(0)
            for i in query:
                response.append(i)
            response.append(192)
            response.append(12)
            response.append(0)
            response.append(1)
            response.append(0)
            response.append(1)
            response.append(0)
            response.append(0)
            response.append(0)
            response.append(255)
            response.append(0)
            response.append(4)
            response.append(192)
            response.append(168)
            response.append(17)
            response.append(149)
            conn.sendall(response)
            response = bytearray()
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp2:
                s_tcp2.connect(('8.8.8.8', 53))
                s_tcp2.sendall(data)
                data2 = s_tcp2.recv(1024)
                conn.sendall(data2)
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
        s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_tcp.bind(('192.168.17.147', 53))
        s_tcp.listen()

        print("***** DNS Server *****")
        while True:
            conn, addr = s_tcp.accept()
            t = threading.Thread(target=analyzeRqt, args=(conn, addr))
            t.start()


if __name__ == '__main__':
    initDNS()
