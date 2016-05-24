import json
import bottle
import urllib, urllib2
import httplib
from bottle import route, run , request, abort
import paho.mqtt.client as mqtt

client=mqtt.Client()
client.connect("192.168.1.132",11883,60)

@route('/acmode',method='POST')
def put_event():
	data=str(request.body.readline()).strip('[]').decode('utf-8-sig')
	print data
	if not data:
		abort(400,'No data recived')
	entity = json.load(request.body)

	if not entity.has_key('_mode') or not entity.has_key('_user') or not entity.has_key('_password'):
		abort(400,'No mode specified or user or password empty')
	if entity['_user'] != 'admin' or entity['_password'] != 'adminIOTsystem':
		abort(401,'User unathorized')
	if entity['_mode']=="man":
		event = json.JSONEncoder().encode({"_dev":entity['_user'],"_prio":str(1),"_value":' '.join((str(entity['_mode']),',',str(entity['_temp']),'ac mode'))})
	else:
		event = json.JSONEncoder().encode({"_dev":entity['_user'],"_prio":str(1),"_value":' '.join((str(entity['_mode']),'ac mode'))})
	print event
	h = {'Content-type':'application/json'}
	url = "http://localhost:8081/newEvent"
	req=urllib2.Request(url,event,h)
	resp=urllib2.urlopen(req)
	print resp.read()
	client.connect("192.168.1.132",11883,60)
	if entity.has_key('_temp'):
		client.publish("/acmode",' '.join((str(entity['_mode']),',',str(entity['_temp']))))
	else:
		client.publish("/acmode",entity['_mode'])
	client.disconnect()

@route('/rele',method='POST')
def put_event():
	data=request.body.readline()
	print data
	if not data:
		abort(400,'No data recived')
	entity = json.loads(data)

	if not entity.has_key('_mode') or not entity.has_key('_user') or not entity.has_key('_password'):
		abort(400,'No mode specified or user or password empty')
	if entity['_user'] != 'admin' or entity['_password'] != 'adminIOTsystem':
		abort(401,'User unathorized')

	event = json.JSONEncoder().encode({"_dev":entity['_user'],"_prio":str(1),"_value":' '.join((str(entity['_mode']),'rele'))})
	print event
	h = {'Content-type':'application/json'}
	url = "http://localhost:8081/newEvent"
	req=urllib2.Request(url,event,h)
	resp=urllib2.urlopen(req)
	print resp.read()
	client.connect("192.168.1.132",11883,60)
	client.publish("/rele",entity['_mode'])
	client.disconnect()


@route('/listEvents', method = 'GET')
def get_events():
	address="http://localhost:8081/listEvents"
	url=urllib2.urlopen(address)
	data=url.read()
	return data
			

run(host='192.168.1.142',port=8080)

