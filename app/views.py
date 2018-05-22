'''
Author: @TC
Flask application user interface
'''

from flask import request, render_template, Flask, redirect, url_for, make_response
from flask import Blueprint
# from app.glue import routes as glue_routes
from app.models import Suburb
import app.glue as glue
# import flask_restful

bp = Blueprint('app', __name__, url_prefix='')
# app = Flask(__name__)
# app.register_blueprint(bp)

# bp.add_url_rule(glue_routes['rule'],
#                 endpoint=glue_routes['endpoint'],
#                 view_func=glue_routes['view_func'],
#                 **glue_routes['options'])


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
    suburb = Suburb.get_instance(suburb_name)
    return render_template('app/result.html', suburb=suburb)


@bp.route('/search', methods=['POST'])
def search():
    # parser = re.RequestParser()
    # parser.add_argument('rt', type=str)
    # args = parser.parse_args()

    # postcode = re.form.get("postcode")
    suburb_name = request.form.get('suburb')

    crime = glue.get_crime(suburb_name)
    acc = glue.get_accommodation(suburb_name)
    poi = glue.get_poi(suburb_name)
    suburb_obj = Suburb(suburb_name, crime, acc, poi)

    return redirect(url_for('.show_results', suburb_name=suburb_name))
