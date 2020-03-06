import socket
import urllib.parse
from pymongo import MongoClient

ip = "127.0.0.1"
port = 53
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
passwor = urllib.parse.quote_plus('Qw3rt&.12345')
client = MongoClient('mongodb://%s:%s@10.0.2.4' % (username, passwor))
db = client['waf']

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_udp:
	socket_udp.bind((ip, port))

	while True:
		data, address = socket_udp.recvfrom(1024)

		id = int(data[:2].hex(), 16)
		flags =  int(data[2:4].hex(), 16)
		quest = int(data[4:6].hex(), 16)
		ans = int(data[6:8].hex(), 16)
		auth = int(data[8:10].hex(), 16)
		add = int(data[10:12].hex(), 16)
		query = data[12:]
		type = query[-1]
		query_class = query[-3]

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
		print(url[:-3])
		url = ''
