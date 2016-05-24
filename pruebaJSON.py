import json
json_input = '{"_dev":"admin","_prio":1,"_value":"auto ac mode"}'
try:
	decoded = json.loads(json_input)
	print json.dumps(decoded, sort_keys=True, indent=4)
except (ValueError, KeyError, TypeError):
	print "Json error"
