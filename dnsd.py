import socket
import urllib.parse
import threading
from pymongo import MongoClient


def analyzeRqt(s_udp, **param):
    usr = urllib.parse.quote_plus('@dm1n')
    pwd = urllib.parse.quote_plus('Qw3rt&.12345')
    client = MongoClient('mongodb://%s:%s@192.168.17.146' % (usr, pwd))
    # client = MongoClient('mongodb://localhost:27017')
    db = client['waf']
    collection = db['sites']

    response = bytearray()

    data = param['data']
    addr = param['addr']
    id = data[:2]
    query = data[12:]

    url = extractURL(query)

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
        s_udp.sendto(response, addr)
        response = bytearray()
    else:
        s_udp.sendto(data, ('8.8.8.8', 53))
        data2, addr2 = s_udp.recvfrom(1024)
        s_udp.sendto(data2, addr)
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
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
        s_udp.bind(('192.168.17.147', 53))
        # print(" ***** DNS Server by waf *****")

        while True:
            data, addr = s_udp.recvfrom(1024)
            t = threading.Thread(target=analyzeRqt,
                                 args=(s_udp, ),
                                 kwargs={'data': data, 'addr': addr})
            t.start()
            t.join()


if __name__ == '__main__':
    initDNS()
