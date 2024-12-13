import socket
import json

# AF_INET 表示使用IPv4, SOCK_DGRAM 则表明数据将是数据报(datagrams)
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_msg = {"msg": 'Hello udp server.'}
client_msg = json.dumps(client_msg)
udp_client.sendto(client_msg.encode('utf8'), ('127.0.0.1', 8888))

while True:
    rec_msg, addr = udp_client.recvfrom(1024)
    print('msg form server:', rec_msg.decode('utf8'))
