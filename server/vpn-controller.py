import subprocess
import flask
import json

app = flask.Flask(__name__)

@app.route("/")
def hello():
	return "Hello World"

# ---------------- vpn-list ----------------

@app.route("/vpn-list")
def get_vpn_list_handler():
	try:
		return construct_vpn_list_response(parse_vpn_list(get_vpn_data()))
	except:
		return construct_error_response('Error while getting vpn list')

def parse_vpn_list(vpn_list_data):
	vpn_pairs = vpn_list_data.split(';')
	vpn_map = {}
	for vpn_pair in vpn_pairs:
		if vpn_pair == '':
			continue
		vpn_pair_chunks = vpn_pair.split(',')
		vpn_map[vpn_pair_chunks[0]] = int(vpn_pair_chunks[1])
	return vpn_map

def construct_vpn_list_response(vpn_map):
	vpn_list = []
	for vpn_name, is_running in vpn_map.iteritems():
		vpn_list.append({'name': vpn_name, 'is_running': is_running})
	return construct_response('vpn_list', vpn_list)

# ---------------- switch-vpn ----------------

@app.route("/switch-vpn/<vpn_name>")
def switch_vpn_handler(vpn_name):
	try:
		if not vpn_exists(vpn_name):
			error_message = 'VPN \'%s\' does not exist' % vpn_name
			return construct_error_response(error_message)
		else:
			# Perform switch, query new data and construct response
			perform_vpn_switch(vpn_name)
			return construct_vpn_list_response(parse_vpn_list(get_vpn_data()))
	except:
		return construct_error_response('Error while switching vpn')

def perform_vpn_switch(vpn_name):
	stop_all_vpn()
	switch_vpn(vpn_name)

# ---------------- utils ----------------

def vpn_exists(vpn):
	vpn_map = parse_vpn_list(get_vpn_data())
	for vpn_name, is_running in vpn_map.iteritems():
		if vpn == vpn_name:
			return True
	return False

# ---------------- os integration ----------------

def get_vpn_data():
	return subprocess.check_output('sh scripts/parse-vpn-list.sh', shell=True)

def stop_all_vpn():
	subprocess.check_output('sh scripts/stop-vpn.sh', shell=True)

def switch_vpn(vpn_name):
	command = 'sh scripts/start-vpn.sh %s' % vpn_name
	subprocess.check_output(command, shell=True)

# ---------------- responses ----------------

def construct_response(data_name, data):
	json_response = {}
	json_response['ok'] = 1
	json_response[data_name] = data
	return flask.Response(json.dumps(json_response), mimetype='application/json')

def construct_error_response(error_message):
	return flask.Response(json.dumps({'ok': 0, 'error': error_message}), mimetype='application/json')

# -----------------

if __name__ == "__main__":
	app.run(debug=True);