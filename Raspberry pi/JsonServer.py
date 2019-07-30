import socket
import json

sock = socket.socket()
sock.bind(('', 2500))
sock.listen(1)
print("데이터 대기 중...\n")
c_sock, r_port = sock.accept()
data = c_sock.recv(1024)
data = json.loads(data.decode())

print('방의 온도는 {:0.1f}도 이고 습도는 {:0.1f}  입니다'.format(data['room']['temperature'], data['room']['humidity']))
sock.close()