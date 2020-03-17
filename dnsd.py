import socket
import urllib.parse
from pymongo import MongoClient

id = bytearray(2)
flags = bytearray(2)
quest = bytearray(2)
ans = bytearray(2)
auth = bytearray(2)
add = bytearray(2)
query = bytearray(2)
url = ''
type = bytearray(2)
query_class = bytearray(2)
response = bytearray()

username = urllib.parse.quote_plus('@dm1n')
password = urllib.parse.quote_plus('Qw3rt&.12345')
client = MongoClient('mongodb://%s:%s@192.168.17.146' % (username, password))
# client = MongoClient('mongodb://localhost:27017')
db = client['waf']
collection = db['sites']

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_udp:
    socket_udp.bind(('192.168.17.147', 53))
    # socket_udp.bind(('', 53))
    print(" ***** DNS Server by waf *****")

    while True:
        data, address = socket_udp.recvfrom(1024)
        id = data[:2]
        print("id: ", int(id.hex(), 16))
        flags = data[2:4]
        # print("flags: ", flags)
        quest = data[4:6]
        # print("quest: ", quest)
        ans = data[6:8]
        # print("ans: ", ans)
        auth = data[8:10]
        # print("auth: ", auth)
        add = data[10:12]
        # print("add: ", add)
        query = data[12:]
        # print("query: ", query)
        type = query[-2:]
        # print("type: ", type)
        query_class = query[-4]
        # print("query_class: ", query_class)

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
        url = url[:-3]
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
            response.append(0)
            response.append(6)
            socket_udp.sendto(response, address)
            print('***** DNS response *****')
            response = bytearray()
        else:
            socket_udp.sendto(data, ('8.8.8.8', 53))
            data2, address2 = socket_udp.recvfrom(1024)
            socket_udp.sendto(data2, address)
            print('* DNS Google response *')
        url = ''
