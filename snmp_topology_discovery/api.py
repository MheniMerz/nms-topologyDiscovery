import flask
import topologyservice

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>HOME PAGE</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/nms/topology', methods=['GET'])
def graph():
    return topologyservice.run()

app.run(host="0.0.0.0", port=6556)
