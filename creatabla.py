#!/usr/bin/python
import MySQLdb
bd = MySQLdb.connect("localhost","serverlog","serverlogvirtualbox","serverlog")
cursor = bd.cursor()
sql = "CREATE TABLE REGISTRO (INSTANTE TIMESTAMP NOT NULL, DISPOSITIVO CHAR(20) NOT NULL, PRIORIDAD INT, VALOR CHAR(15), USUARIO CHAR(20))"

try:
	cursor.execute(sql)
	data = cursor.fetchone()
	print "Tabla creada correctamente"
except:
	bd.rollback()

bd.close()
