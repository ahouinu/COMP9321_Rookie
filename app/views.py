'''

Author: @TC
Flask Application User Interface

'''
import os

from flask import request, render_template, Flask, redirect, url_for, send_from_directory
from flask import Blueprint
from flask_restful import reqparse
# from app.glue import routes as glue_routes
from app.models import Suburb
import app.glue as glue
import json
# import flask_restful
root = os.getcwd()
bp = Blueprint('app', __name__, url_prefix='', static_folder='/templates/')
# app = Flask(__name__)
# app.register_blueprint(bp)

# bp.add_url_rule(glue_routes['rule'],
#                 endpoint=glue_routes['endpoint'],
#                 view_func=glue_routes['view_func'],
#                 **glue_routes['options'])
GOOGLE_MAP_API_KEY = 'AIzaSyDbdgCBSoXfep6LvrUsPRciIDc6ov9KceA'


@bp.route('/', methods=['GET'])
def index():

    return render_template('app/index.html')


@bp.route('/suburb/<suburb_name>', methods=['GET'])
def show_results(suburb_name):
    '''
    render result html page
    :param suburb_name: a Suburb object containing all the information
    :return:
    '''
    if not Suburb.imported(suburb_name):
        return redirect(url_for('.index'))
    suburb = Suburb.get_instance(suburb_name)
    data = json.dumps(suburb.poi_locations)
    # occ = data.count('"')
    # data = data.replace(count=occ)
    return render_template('app/result.html', suburb=suburb, locations=data)


@bp.route('/search', methods=['POST'])
def search():
    # parser = re.RequestParser()
    # parser.add_argument('rt', type=str)
    # args = parser.parse_args()

    # postcode = re.form.get("postcode")
    suburb_name = request.form.get('suburb')
    suburb_name = suburb_name.replace('+', ' ')
    if Suburb.imported(suburb_name):
        return redirect(url_for('.show_results', suburb_name=suburb_name))
    if not glue.check_input(suburb_name):
        # correction = glue.correct_input(suburb_name)
        return redirect(url_for('.suburb_not_found', origin=suburb_name))

    suburb_obj = glue.get_suburb_obj(suburb_name)

    return redirect(url_for('.show_results', suburb_name=suburb_name))


@bp.route('/error', methods=['GET'])
def suburb_not_found():
    parser = reqparse.RequestParser()
    parser.add_argument('origin')
    # parser.add_argument('correction')
    args = parser.parse_args()

    origin = args.get('origin')
    # correction = args.get('correction')
    correction = glue.correct_input(origin)

    return render_template('app/suburb_not_found.html', origin=origin, correction=correction)


@bp.route('/figures/<path:filename>', methods=['GET'])
def send_figure(filename):
    path = root + '/templates/static/figures'
    return send_from_directory(path, filename)
