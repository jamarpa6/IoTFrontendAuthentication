#!/usr/bin/python
import MySQLdb
import socket

UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

listen_addr = ("",15001)
UDPSock.bind(listen_addr)

while True:
	data, addr = UDPSock.recvfrom(1024)
	if data != "":
		print data
		values = data.strip().split(",",2)
		print values
		print values[0]
		print values[1]
		print values[2]
		bd = MySQLdb.connect("localhost","serverlog","serverlogvirtualbox","serverlog")
		cursor = bd.cursor()
		sql="INSERT INTO LOGS (DISPOSITIVO, PRIORIDAD, VALOR) VALUES ('"+values[0]+"',"+values[1]+",'"+values[2]+"')"
		try:
			cursor.execute(sql)
			bd.commit()
			print "Hecho"
		except:
			bd.rollback()
			print "Ha ocurrido un error"

		bd.close()
