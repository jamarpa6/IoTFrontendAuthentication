#!/usr/bin/python

#Web IoT interface to provide a secure managment panel with encryptation and user authoritation
#using Bottle Framework. The connection with internal IoT services are provided by Paho MQTT client for Pyton
#


#Import of modules used to create the webserver and the mqtt client
import time, os, binascii
import bottle
from bottle import response, request, static_file, template, abort
import paho.mqtt.client as mqtt

#List of correct users, it can be replace with a SQL connection to get the names and passwords
correct_users={"user":"pass"}
correct_tokens={}
client = mqtt.Client()

#Driving system to known state
primer_inicio = 1;
estado="off";
canal=1;
volumen=0;

#Using ssl server to provide encrypted connection
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

#############################################################
#Assignment between URI's REST resources and Python functions
#############################################################

#Index route
@bottle.route('/', method='GET')
@bottle.route('/index', method='GET')
@bottle.route('/index.html', method='GET')
def root():
	print "Recibo peticion"
	return template("index.html")

#Login service
@bottle.route('/login', method='GET')
def principal():
	#Analizing user cookie parameters
	token=request.get_cookie('Token_auth')
        usr=request.get_cookie('User_name')
        print "Estos son el token y el user de la cookie"
        print token
        print usr
	#Checking if the user has been autorized
        if usr in correct_tokens and token==correct_tokens[usr]:
                return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))
        #If user doesn't have a correct authoritation token, send error page
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')
	
@bottle.route('/<filename:path>')
def send_Static(filename):
	return static_file(filename, root='./')

#Authorize client first time for each one using cookies
@bottle.route('/login', method='POST')
def login():
	#Checking user and password parameters
        print "Entro a comprobar usuario y contrasena"
	user = request.forms.get("user")
	passwd = request.forms.get("passwd")
	print "Usuario y contrasena: "
	print user
	print passwd
	#If correct user, save and send an authorized token and load control panel
	if user in correct_users and correct_users[user]==passwd:
		print "Usuario correcto"
		#Generating raonom token for this user
		token=binascii.b2a_hex(os.urandom(15))
		#Storing token for the user in the dictionary
		correct_tokens[user]=token
		print "Guardo el token"
		print token
		#Set cookies with token and user for the browser
		response.set_cookie('Token_auth',token,path='/')
		response.set_cookie('User_name',user,path='/')
		print (response)
		#Return HTML page
		return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))
	#Else send html error page
	else:
		return template("error.html")		

#Get the state of the HI-FI sound system
@bottle.route('/estado', method='GET')
def getState():
	print "Entro a consultar el estado de la cadena"
	#Get credentials for the user
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr
	#If user is authenticated, let him/her acces
	if usr in correct_tokens and token==correct_tokens[usr]:
		return estado
	#Else, return error page
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

#Set new state to the HI-FI sound system
@bottle.route('/estado', method='POST')
def setState():
	print "Entro a la funcion start/stop"
	#Get credentials for the user
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr
	
	#If user is authenticated, let him/her acces
	if usr in correct_tokens and token==correct_tokens[usr]:
		#Internal global variables to control execution state and first start
		global estado
		global primer_inicio

		#If HI-FI is on, turn it off
		if estado=="on":
			print "Apago cadena"
			client.connect("localhost",11883,60)
			client.publish("/estado","off")
			estado="off"
		#If it is off, turn it on
		if estado=="off":
			print "Enciendo cadena"
			#Connect to MQTT server and publish in topic
			client.connect("localhost",11883,60)
			client.publish("/estado","on")
			#If this is the first start, set known values to HI-FI
			if primer_inicio:
				print "Es el primer inicio"
				time.sleep(5)		
				client.publish("/reset","reset")
				time.sleep(3)
				primer_inicio=0
			estado="on"
                return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))
	#Else reject acces
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/volumen', method='POST')
def setVolume():
	print "Entro a la funcion para actualizar volumen"
	#Get credentials for the user
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr

	#If user is authenticated, let him/her acces
	if usr in correct_tokens and token==correct_tokens[usr]:
		global volumen
		vol=request.forms.get("vol")
		print vol
		#Connect to MQTT server
		client.connect("localhost",11883,60)
		#If user wants to up volume
		if vol=="up":
			print "Subo volumen"
			#If volume is below max value
			if volumen<30:
				#Publish in topic
				client.publish("/volumen",vol)
				volumen=volumen+1
				print "el nuevo volumen es"
				print volumen
		else:
			if vol=="down":
				print "Bajo volumen"
				#If volume is over 0
				if volumen>0:
					#Publish in topic
					client.publish("/volumen",vol)
					volumen=volumen-1
					print "el nuevo volumen es"
					print volumen

                return template("panelsimplificado.tpl",volume=str(volumen),state=str(estado),channel=str(canal))
	
	#Else reject acces
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/volumen', method='GET')
def getVolume():
	print "Entro en la funcion para saber el estado del volume"
	#Get credentials for the user
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr
	if usr in correct_tokens and token==correct_tokens[usr]:
		return str(volumen)
	#Else reject acces
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/canal',method='GET')
def getChanel():
	print "Entro en la funcion para saber el canal"
	#Get credentials for the user
	token=request.get_cookie('Token_auth')
	usr=request.get_cookie('User_name')
	print "Estos son el token y el user de la cookie"
	print token
	print usr
	if usr in correct_tokens and token==correct_tokens[usr]:
		return str(canal)
	#Else reject acces
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')

@bottle.route('/canal', method='POST')
def setChanel():
	print "Entro en la funcion para cambiar el canal"
	#Get credentials for the user
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

	#Else reject acces
	else:
		return abort(401,'ACCION NO AUTORIZADA A ESTE USUARIO, VUELVA A LA PAGINA DE INICIO PARA REALIZAR EL LOGIN')
#Running the server
srv = SSLWebServer(host='ip', port=4443)
bottle.run(server=srv)
