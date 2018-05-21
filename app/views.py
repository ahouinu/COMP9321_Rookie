'''
Author: @TC
Flask application user interface
'''

from flask import request, render_template, Flask, redirect, url_for, make_response
from flask import Blueprint
import flask_restful

bp = Blueprint('app', __name__, url_prefix='')
# app = Flask(__name__)
# app.register_blueprint(bp)


@bp.route('/', methods=['GET'])
def index():

    return render_template('app/index.html')


@bp.route('/search', methods=['POST'])
def search():
    # TODO: This function should be implemented in glue.py, expected to receive a form param, val=suburb_name
    pass


@bp.route('/suburb/<suburb>', methods=['GET'])
def show_results(suburb):
    '''
    render result html page
    :param suburb: a Suburb object containing all the information
    :return:
    '''
    return render_template('app/result.html', suburb=suburb)


