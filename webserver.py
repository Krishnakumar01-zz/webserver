import socket
import os,os.path,time
def server():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	port=5555
	s.bind(('',port))
	s.listen(5)
	while True:
		client,client_addr=s.accept()
		new=os.fork()
		if new==0:
			s.close()
			handler(client)
			client.close()
			os._exit(0)
		else:
			client.close()

def handler(client):
	request=client.recv(1024)
	head_type={'pdf':'application/pdf',
		   'jpg':'image/jpg',
		   'jpeg':'image/jpeg',
		   'png':'image/png',
		   'gif':'image/gif',
		   'txt':'text/plain'}
	l=request.split()
	fname=l[1].split('/')[1]
	if fname.split('.')[-1] in head_type.keys():
		flag=True
		c=head_type[fname.split('.')[-1]]
		if fname.split('.')[-1]=='txt':
			time.sleep(30)
		if os.path.isfile(fname):
			f=open(fname,'rb')
			d=f.read()
		else:
			flag=False
	else:
		flag=False
	if flag:
        	client.send('HTTP/1.1 200 OK\r\n') 
            	client.send('Accept-Ranges: bytes\r\n')
            	client.send('Content-Type: '+c+'\r\n')
            	client.send('Content-Length:'+str(len(d))+'\r\n\r\n')
            	client.send(d)
            	f.close()
            	client.close()
        else:
        	d='''HTTP/1.1 404 File Not Found\r\n\r\n
                <html><body><h1> Error 404 File not found<body><html>'''
            	client.send(d)
		client.close()
server()
