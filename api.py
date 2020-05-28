import data

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

api_data = data.Data()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Pathfinder 2e API</h1><p>This is an API for the Second Edition of the Pathfinder TTRPG. All data comes from the official SRD <a href=\"http://2e.aonprd.com/\">Archives of Nethys</a>.</p>"

# @app.route('/actions', methods=['GET'])

@app.route('/api/v1/ancestries', methods=['GET'])
def ancestries_router():
    params = request.args
    name = params.get('name')
    return jsonify(api_data.get_ancestries(name=name))

# @app.route('/archetypes', methods=['GET'])

@app.route('/api/v1/backgrounds', methods=['GET'])
def backgrounds_router():
    params = request.args
    name = params.get('name')
    # return jsonify(api_data.get_backgrounds(name=name))
    return str(api_data.get_backgrounds(name=name))

# @app.route('/classes', methods=['GET'])
# @app.route('/conditions', methods=['GET'])
# @app.route('/equipment', methods=['GET'])
# @app.route('/feats', methods=['GET'])
# @app.route('/hazards', methods=['GET'])
# @app.route('/monsters', methods=['GET'])
# @app.route('/skills', methods=['GET'])
# @app.route('/spells', methods=['GET'])

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()