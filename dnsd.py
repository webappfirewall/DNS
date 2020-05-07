import socket
import urllib.parse
import threading
from pymongo import MongoClient

b1 = bytearray(b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00')
b2 = bytearray(b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xff\x00\x04')


def analyzeRqt(s_udp, data, addr):
    usr = urllib.parse.quote_plus('@dm1n')
    pwd = urllib.parse.quote_plus('Qw3rt&.12345')
    client = MongoClient('mongodb://%s:%s@192.168.17.146' % (usr, pwd))
    db = client['waf']
    collection = db['sites']
    id = data[:2]
    query = data[12:]
    url = extractURL(query)
    print('URL: ', url)

    doc = collection.find_one({"url": url})

    if doc is not None:
        response = bytearray()
        ip = doc['ip'].split('.')

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

        s_udp.sendto(response, addr)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp2:
            s_udp2.sendto(data, ('8.8.8.8', 53))
            data2, addr2 = s_udp2.recvfrom(1024)
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

        print("***** DNS Server *****")
        while True:
            data, addr = s_udp.recvfrom(1024)
            t = threading.Thread(target=analyzeRqt, args=(s_udp, data, addr))
            t.start()


if __name__ == '__main__':
    initDNS()
