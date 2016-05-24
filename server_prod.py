#!/usr/bin/python

import time, os, binascii
import bottle
from bottle import response, request, static_file, template, abort
import paho.mqtt.client as mqtt

correct_users={"javi":"1234","alec":"2039"}
correct_tokens={}
client = mqtt.Client()

primer_inicio = 1;
estado="off";
canal=1;
volumen=0;

class SSLWebServer(bottle.ServerAdapter):
	def run(self, handler):
        	from wsgiref.simple_server import make_server
        	import ssl
        	srv = make_server(self.host, self.port, handler, **self.options)
        	srv.socket = ssl.wrap_socket(
                	srv.socket, server_side=True,
                	certfile='cert.crt',
                	keyfile='private.key')
		
        	srv.serve_forever()

@bottle.route('/', method='GET')
@bottle.route('/index', method='GET')
@bottle.route('/index.html', method='GET')
def root():
	print "Recibo peticion"
	return template("index.html")

@bottle.route('/login', method='GET')
def principal():
	token=request.get_cookie('Token_auth')
        usr=request.get_cookie('User_name')
        print "Estos son el token y el user de la cookie"
        print token
        print usr
        if usr in correct_tokens and token==correct_tokens[usr]:
                return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))
        else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')
	
@bottle.route('/<filename:path>')
def send_Static(filename):
	return static_file(filename, root='./')

@bottle.route('/login', method='POST')
def login():
        print "Entro a comprobar usuario y contrasena"
	user = request.forms.get("user")
	passwd = request.forms.get("passwd")
	print "Usuario y contrasena: "
	print user
	print passwd
	if user in correct_users and correct_users[user]==passwd:
		print "Usuario correcto"
		token=binascii.b2a_hex(os.urandom(15))
		correct_tokens[user]=token
		print "Guardo el token"
		print token
		response.set_cookie('Token_auth',token,path='/')
		response.set_cookie('User_name',user,path='/')
		print (response)
		return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))
	else:
		return template("error.html")		

@bottle.route('/estado', method='GET')
def getState():
	print "Entro a consultar el estado de la cadena"
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr
	if usr in correct_tokens and token==correct_tokens[usr]:
		return estado
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/estado', method='POST')
def setState():
	print "Entro a la funcion start/stop"
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr

	if usr in correct_tokens and token==correct_tokens[usr]:
		global estado
		global primer_inicio

		if estado=="on":
			print "Apago cadena"
			client.connect("localhost",11883,60)
			client.publish("/estado","off")
			estado="off"
		else:
			if estado=="off":
				print "Enciendo cadena"
				client.connect("localhost",11883,60)
				client.publish("/estado","on")
				if primer_inicio:
					print "Es el primer inicio"
					time.sleep(5)		
					client.publish("/reset","reset")
					time.sleep(3)
					primer_inicio=0
				estado="on"
                return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))

	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/volumen', method='POST')
def setVolume():
	print "Entro a la funcion para actualizar volumen"
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr

	if usr in correct_tokens and token==correct_tokens[usr]:
		global volumen
		vol=request.forms.get("vol")
		print vol
		client.connect("localhost",11883,60)
		if vol=="up":
			print "Subo volumen"
			if volumen<30:
				client.publish("/volumen",vol)
				volumen=volumen+1
				print "el nuevo volumen es"
				print volumen
		else:
			if vol=="down":
				print "Bajo volumen"
				if volumen>0:
					client.publish("/volumen",vol)
					volumen=volumen-1
					print "el nuevo volumen es"
					print volumen

                return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))

	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/volumen', method='GET')
def getVolume():
	print "Entro en la funcion para saber el estado del volume"
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr
	if usr in correct_tokens and token==correct_tokens[usr]:
		return str(volumen)
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/canal',method='GET')
def getChanel():
	print "Entro en la funcion para saber el canal"
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr
	if usr in correct_tokens and token==correct_tokens[usr]:
		return str(canal)
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/canal', method='POST')
def setChanel():
	print "Entro en la funcion para cambiar el canal"

	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr
	if usr in correct_tokens and token==correct_tokens[usr]:
		global canal
		can=request.forms.get("can")
		client.connect("localhost",11883,60)
		client.publish("/canal",can)
		if can=='up':
			print "Entro a subir canal"
			if canal==13:
				print "Como el canal ya es 13 pasa a ser 1"
				canal=1
			else:
				print "Como el canal no es 13, canal++"
				canal=canal+1
		else:
			if can=='down':
				print "Entro a bajar canal"
				if canal==1:
					print "Como el canal ya es 13, pongo 13"
					canal=13
				else:
					print "Como el canal no es 1, canal --"
					canal=canal-1
                return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))

	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

srv = SSLWebServer(host='192.168.1.141', port=4443)
bottle.run(server=srv)
