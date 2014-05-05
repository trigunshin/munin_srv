from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/munin/template')
def generate_template():
    nodes = [n for n in client.munin.nodes.find()]
    return render_template('munin.conf', nodes=nodes)

# curl --data "hostname=myhost.name&ip=127.0.0.1" http://ec2-54-86-100-14.compute-1.amazonaws.com:5000/munin/node
@app.route('/munin/node', methods=['POST'])
def add_node():
    hostname = request.values.get('hostname', None)
    ip = request.values.get('ip', None)
    if not (ip and hostname):
        return
    obj = {
        'ip': ip,
        'hostname': hostname
    }
    result = client.munin.nodes.update(
        spec={'hostname': hostname},
        document=obj,
        upsert=True,
        multi=False)
    return 'maybe_my_ip'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
