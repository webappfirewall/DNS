import socket
import urllib.parse
from pymongo import MongoClient

id = ''
flags = ''
quest = ''
ans = ''
auth = ''
add = ''
query = ''
url = ''
type = ''
query_class = ''

username = urllib.parse.quote_plus('@dm1n')
password = urllib.parse.quote_plus('Qw3rt&.12345')
client = MongoClient('mongodb://%s:%s@10.0.2.4' % (username, password))
db = client['waf']
collection = db['sites']

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_udp:
    socket_udp.bind(("52.191.249.108", 53))
    print("DNS Server by waf")

    while True:
        data, address = socket_udp.recvfrom(1024)
        id = data[:2].hex()
        print("id: ", id)
        flags = data[2:4].hex()
        print("flags: ", flags)
        quest = data[4:6].hex()
        print("quest: ", quest)
        ans = data[6:8].hex()
        print("ans: ", ans)
        auth = data[8:10].hex()
        print("auth: ", auth)
        add = data[10:12].hex()
        print("add: ", add)
        query = data[12:]
        print("query: ", query)
        type = query[-1]
        print("type: ", type)
        query_class = query[-3]
        print("query_class: ", query_class)

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

        doc = collection.find_one({"url": url})

        if doc is not None:
            print(doc['ip'])
        print(url)
        url = ''
